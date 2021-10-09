#%%
from typing import Any
from PyQt5.QtCore import QObject
import ast
# import astpretty
from ast import Expr, Assign, Name, Call, Store, Attribute, Load, Constant, Expression, Module, Del, iter_child_nodes, walk
import cadquery.cqgi
from cadquery import Workplane
from cadquery.occ_impl.shapes import Shape
import cadquery as cq
from collections import OrderedDict
from graphviz.backend import command
from nales_alpha.utils import get_Workplane_operations, get_cq_topo_classes, get_cq_types, get_Wp_method_kwargs, get_shapes_classes_methods
from nales_alpha.NDS.ast_grapher import make_graph


     

def prepare_parent_childs(tree):
    """
    Adds parent and chils attributes to ast nodes
    """
    for node in ast.walk(tree):
        node.childs = []
        for child_node in ast.iter_child_nodes(node):
            node.childs.append(child_node)
            child_node.parent = node

class CQCallAnalyze(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.sub_cmd = Command()


class CommandAnalyzer(ast.NodeVisitor):
    def __init__(self, ns, ns_before_cmd) -> None:
        super().__init__()
        self._console_ns = ns
        self._console_ns_before_cmd = ns_before_cmd
        self.commands = []

    def visit_Module(self, mnode: Module) -> Any:
        for node in mnode.body:
            if isinstance(node, Assign):
                analyzer = CQAssignAnalyzer(self._console_ns, self._console_ns_before_cmd)        
                analyzer.visit(node)
                self.commands.append(analyzer.get_command())

class CQAssignAnalyzer(ast.NodeVisitor):
    def __init__(self, ns, ns_before_cmd) -> None:
        super().__init__()
        self._console_ns = ns
        self._console_ns_before_cmd = ns_before_cmd
        self._top_stack_node = None
        self.call_type = None
        self.call_stack = None
        self._cq_assign_type = None
        self.cmd = Command()
        


    def _get_root_node_from_Call(self, node: Call) -> Name:
        """
        Gets the root of a chain call
        for example 'p = a.b.c.d()' would isolate the Name node linked to 'a'
        """
        assert isinstance(node, Call)

        call_root = None

        for sub_node in walk(node):
            if isinstance(sub_node, Name):
                # This is needed if we have nested calls, for example :
                # u = cq.Edge.makeLine(cq.Vector(1,1,1), cq.Vector(1,1,2))
                # It makes sure to return the Name node bounded to cq.Edge and not to cq.Vector
                if call_root:
                    node_call = sub_node
                    while not isinstance(node_call, Call):
                        node_call = node_call.parent
                    if node_call is node:
                        call_root = sub_node
                        
                else:
                    call_root = sub_node
                


        return call_root

    def is_Workplane(self, var_name) -> bool:
        try:
            obj_type  = self._console_ns[var_name]          
        except KeyError:            
            return False
        if isinstance(obj_type,Workplane):
            return True
    

    def is_Shape(self, var_name) -> bool:
        try:
            obj_type  = self._console_ns[var_name]          
        except KeyError:            
            return False
        if isinstance(obj_type,Shape):
            return True
    
    def is_cq_obj(self, var_name: str) -> bool:
        cq_types = get_cq_types()
        try:
            obj  = self._console_ns[var_name]          
        except KeyError:            
            return False
        if type(obj) in cq_types:
            return True


            
    def is_cq_assign(self, node: Assign) -> bool:
        """
        Returns if an assignement value is made from a cq object or from cq class

        Also sets the value of `_cq_assign_type` parameter
        """

        if isinstance(node.value, Call):
            call_root = self._get_root_node_from_Call(node.value)
        elif isinstance(node.value, Name):
            call_root = node.value
        else:
            return False

        if call_root.id == "cq":
            if call_root.parent.attr in get_cq_topo_classes():
                self._cq_assign_type = "Shape"
            elif call_root.parent.attr == "Workplane":
                self._cq_assign_type = "Workplane"
            else:
                self._cq_assign_type = "Other"              
            return True 

        elif self.is_cq_obj(call_root.id):
            if self.is_Workplane(call_root.id):
                self._cq_assign_type = "Workplane"
            elif self.is_Shape(call_root.id):            
                self._cq_assign_type = "Shape"
            else:
                self._cq_assign_type = "Other"

        else:
            return False
            
            
        
        
    def get_command(self) -> "Command":
        cmd = self.cmd
        if cmd.type != "undefined":
            try:
                cmd.obj = self._console_ns[self.cmd.var]
            except KeyError:
                cmd.type = "undefined"
        if cmd.operations:
            cmd.operations = OrderedDict(reversed(list(cmd.operations.items())))
        else:
            cmd.operations = OrderedDict()
        return cmd 


    def visit_Assign(self, node):

        if self.is_cq_assign(node):
            # assign is something like :
            # part = cq.Workplane().box(1,1,1)
            # part = cq.Edge.makeEdge(v1,v2)          
            # part = aCqObj.sphere(5) 
            # vector = cq.Vector(0,0,1) 

            self.cmd.var = node.targets[0].id
            if self._cq_assign_type in ["Workplane, Shape"]:                 
                if isinstance(node.value, Call):    
                    self._top_stack_node = node.value
                    root_node = self._get_root_node_from_Call(node.value)
                    self.cmd.operations = self._get_call_stack(node.value)
                else:
                    #Node is a Name node referring to a cq object in memory
                    root_node = node                

                try:    
                    if root_node.id == "cq":
                        if root_node.parent.attr == "Workplane":
                            self.cmd.type = "new_part"

                        elif root_node.parent.attr in get_cq_topo_classes():
                            self.cmd.type = "new_shape"
                            self.cmd.topo_type = node.parent.attr
                            
                    elif root_node.id == self.cmd.var:
                        self.cmd.type = "part_edit"

                    elif self.is_Workplane(root_node.id):                    
                        self.cmd.type = "new_part"

                except AttributeError:
                    pass

            elif self._cq_assign_type == "Others":
                pass


            self.generic_visit(node)

        else:
            # The command is not cq related so we stop the parsing
            return 

    def _get_call_stack(self, node: Call):
        

        call_stack = OrderedDict()        

        for sub_node in ast.walk(node):
            if isinstance(sub_node, Call):
                method_name = sub_node.func.attr                
                kwargs = get_Wp_method_kwargs(method_name)
                for invoked_kw in sub_node.keywords:
                    kwargs[invoked_kw.arg] = invoked_kw.arg.value.value # override defaults kwargs by the ones passed
                try:
                    call_stack[method_name] = ([arg.value if hasattr(arg, "value") else arg.id for arg in sub_node.args ], kwargs)
                except AttributeError:
                    raise NotImplementedError(f"les arguments de types {arg} ne sont pas encore gérés")

        return call_stack

class ParentChildNodeTransformer(object):

    def visit(self, node):
        self._prepare_node(node)
        for field, value in ast.iter_fields(node):
            self._process_field(node, field, value)
        return node

    @staticmethod
    def _prepare_node(node):
        if not hasattr(node, 'parent'):
            node.parent = None
        if not hasattr(node, 'parents'):
            node.parents = []
        if not hasattr(node, 'childrens'):
            node.childrens = []

    def _process_field(self, node, field, value):
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, ast.AST):
                    self._process_child(item, node, field, index)
        elif isinstance(value, ast.AST):
            self._process_child(value, node, field)

    def _process_child(self, child, parent, field_name, index=None):
        self.visit(child)
        child.parent = parent
        child.parents.append(parent)
        child.parent_field = field_name
        child.parent_field_index = index
        child.parent.childrens.append(child)  

class Command():
    """
    This class is used to interface the GUI, the backend and the frontend
    Command object store information about how the application should be changed/updated

    It's designed to receive chode chunks and return information about what this code should do to the application
    It review code_chunks with ast nodes

    Command types are given below :
     - new_part
     - part_edit
     - part_override
     - new_shape
    """

    def __init__(self):
        self.type = "undefined"
        self.var = None 
        self.operations = None
        self.obj = None

class SubCommand():
    def __init__(self):
        self.type = "undefined"
        self.func_call = {}
        self.obj = None

if __name__ == "__main__":
    import astpretty
    import cadquery as cq
    from cadquery import cq
    from astmonkey import visitors, transformers
    debug = True
    cmd = "a = b.box(1,1,1).sphere(2)\nu = b"
    c=cq.Workplane().box(1,1,1).sphere(2)
    ns = {"cq":cadquery, "b":c}
    ns2 = {"a": 5,"cq":cadquery, "b":c}
    cmd_analyzer = CQAssignAnalyzer(ns2, ns) # call this line in the ipython window to view the graph

    ast_tree = ast.parse(cmd)
    from astmonkey import transformers, visitors
    import graphviz
    visitor = visitors.GraphNodeVisitor()
    node = ParentChildNodeTransformer().visit(ast_tree)
    visitor.visit(node)
    raw_dot = visitor.graph.to_string()
    graph = graphviz.Source(raw_dot)
    cmd_analyzer.visit(node)
    cmd = cmd_analyzer.get_command()
    print(cmd_analyzer.call_stack.items())
   
   
# %%
