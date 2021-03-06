from operator import rshift
from typing import Dict, List

from nales.NDS.interfaces import NPart
from nales.NDS.model import NModel
from nales.utils import DependencySolver


class FileWriter:
    def __init__(self) -> None:
        pass


class PythonFileWriter:
    def __init__(self, model: NModel, param_table) -> None:
        self.model = model
        self.param_table = param_table
        self.parts_data = []
        self.shapes_data = []
        self.others_data = []

        self._prepare_data()

    def _write_parameters(self, file_obj):
        params = self.param_table.parameters
        file_obj.write(
            f"#Paramsdef>> {len(params)}\n"
        )  # write the number of param lines
        for param in params:
            if param.type == "str":
                file_obj.write(f'{param.name} = "{param.value}" # {param.type}\n')
            else:
                file_obj.write(f"{param.name} = {param.value} # {param.type}\n")
        file_obj.write("\n")

    def _get_arg_data(self, narg):

        arg_data = {}

        arg_data["name"] = narg.name
        arg_data["linked"] = narg.is_linked()

        if narg.is_linked(by="param"):
            val = narg.linked_param
        elif narg.is_linked(by="obj"):
            val = narg.linked_node.name
        else:
            val = narg.value

        arg_data["value"] = val

        return arg_data

    def _get_operation_data(self, nop):

        op_data = {"name": None, "args": [], "linked": False}

        for arg in nop.childs:
            arg_data = self._get_arg_data(arg)
            op_data["args"].append(arg_data)

            if arg_data["linked"]:
                op_data["linked"] = True

        op_data["name"] = nop.name

        return op_data

    def _get_part_data(self, npart):

        part_data = {"name": None, "operations": [], "linked": False}

        for operation in npart.childs:
            op_data = self._get_operation_data(operation)
            part_data["operations"].append(op_data)

            if op_data["linked"]:
                part_data["linked"] = True

        part_data["name"] = npart.name

        return part_data

    def _sort_parts_data(self, nparts: List[NPart]) -> List[NPart]:
        """
        Sorts NParts that are linked in order to have valid python code
        (If NPart A depend on B, then A must be written before B in the file)
        """
        dep_solver = DependencySolver()

        for npart in nparts:
            deps = []
            for nop in npart.childs:
                for narg in nop.childs:
                    if narg.is_linked(by="obj"):
                        deps.append(narg.linked_node.name)
            dep_solver.add_relation(npart.name, set(deps))

        result = dep_solver.resolve()

        sorted_parts = sorted(nparts, key=lambda node: result.index(node.name))
        return sorted_parts

    def _prepare_parts_data(self):
        nparts = self.model.parts

        sorted_nparts = self._sort_parts_data(nparts)

        for npart in sorted_nparts:
            self.parts_data.append(self._get_part_data(npart))

    def _prepare_shapes_data(self):
        pass

    def _prepare_others_data(self):
        pass

    def _prepare_data(self):
        self._prepare_parts_data()
        self._prepare_shapes_data()
        self._prepare_others_data()

    def _arg_data_to_str(self, arg_data: Dict):
        if isinstance(arg_data["value"], str) and not arg_data["linked"]:
            value = f"\"{arg_data['value']}\""
        else:
            value = arg_data["value"]

        return f'{arg_data["name"]} = {value}'

    def _op_data_to_str(self, op_data: Dict):

        op_str = f"{op_data['name']}("
        for arg in op_data["args"]:
            op_str += self._arg_data_to_str(arg)
            if arg is not op_data["args"][-1]:
                op_str += ", "

        op_str += ")"
        return op_str

    def _get_part_header(self, pdata):
        name = pdata["name"]
        nb_ops = len(pdata["operations"])
        link = pdata["linked"]
        header = f"#Partdef>> {name} {nb_ops} {link}\n"
        return header

    def _part_data_to_str(self, part_data):

        part_str = f'{part_data["name"]} = cq.Workplane()\n'

        for op in part_data["operations"]:
            if op["name"] == "__init__":
                part_str = f'{part_data["name"]} = cq.Workplane{self._op_data_to_str(op).strip(op["name"])}\n'
            else:
                part_str += f'{part_data["name"]} = {part_data["name"]}.{self._op_data_to_str(op)}\n'

        return part_str

    def write_file(self, path):
        with open(path, "w") as py_file:

            py_file.write("# This file has been generated automatically by Nales\n")
            py_file.write(
                "# Don't modify this file unless you know what you are doing\n"
            )
            py_file.write("import cadquery as cq\n\n")

            self._write_parameters(py_file)

            for part in self.parts_data:
                py_file.write(self._get_part_header(part))
                py_file.write(self._part_data_to_str(part))
                py_file.write("\n")
