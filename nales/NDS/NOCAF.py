# Python implementation of OCAF library for Nalès

import OCP
from OCP.BinDrivers import BinDrivers
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDocStd import TDocStd_Application, TDocStd_Document
from OCP.TPrsStd import TPrsStd_AISViewer
from OCP.XmlDrivers import XmlDrivers


class Application(TDocStd_Application):
    def __init__(self, binary=False):
        super().__init__()
        if binary:
            BinDrivers.DefineFormat_s(self)
            self._file_extension = ".cbf"
            self.doc_format = "BinOcaf"
        else:
            XmlDrivers.DefineFormat_s(self)
            self._file_extension = ".xml"
            self.doc_format = "XmlOcaf"

        self.doc = TDocStd_Document(TCollection_ExtendedString(self.doc_format))

        self.NewDocument(TCollection_ExtendedString(self.doc_format), self.doc)

    def viewer_redraw(self):
        """
        Redraw the viewer (refresh the view even if the user isn't moving the view)
        """
        self._pres_viewer.Update()

    def init_viewer_presentation(self, context: OCP.AIS.AIS_InteractiveContext):
        self._pres_viewer = TPrsStd_AISViewer.New_s(self.doc.GetData().Root(), context)

    def save_as(self, path: str):
        """
        Saves the application document in the specified path.
        The file extension is automatically added by the :Application:
        """
        path += self._file_extension
        status = self.SaveAs(self.doc, TCollection_ExtendedString(path))

        if status != OCP.PCDM.PCDM_SS_OK:
            self.Close(self.doc)
            raise Exception("The document could not be saved !")

    def close(self):
        self.Close(self.document)
