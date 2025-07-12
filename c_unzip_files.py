from m9lib import uCommand, uCommandResult, uFolder, uCommandRegistry
from zipfile import ZipFile

import os
import shutil

class UnzipFilesResult(uCommandResult):

    def __init__(self):
        super().__init__()

        # list of [filename, filepath, success]
        self.zipfiles = []

    def AddZipResult(self, in_filepath, in_success):
        self.zipfiles.append ((in_filepath, in_success))

    def GetZipResults(self, in_success=None):
        return [zip for zip in self.zipfiles if in_success is None or zip[1] is in_success]
        
class UnzipFiles(uCommand):
    
    def __init__(self):
        super().__init__()
        
    def imp_execute(self, in_preview):
        # read parameters
        self.p_folderpath = self.GetParam("FolderPath")
        self.p_recurse = self.GetBoolParam("RecurseFolders")
        self.p_extractfolder = self.GetParam("ExtractFolder")
        self.p_createsubfolder = self.GetBoolParam("CreateSubFolder")
        self.p_cleanfolder = self.GetParam("CleanFolder")
        if self.p_cleanfolder =="":
            self.p_cleanfolder = None
        if self.p_cleanfolder:
            self.p_cleanfolder = os.path.join(self.GetParam("CleanFolder"), self.GetClass())

        self.LogParam("FolderPath")
        self.LogParam("RecurseFolders")
        self.LogParam("ExtractFolder")
        self.LogParam("CreateSubFolder")
        self.LogParam("CleanFolder")
        self.GetLogger().WriteBlank()

        # some simple validations and folder creations
        init_error = "Failed Initialization"
        if uFolder.ConfirmFolder (self.p_folderpath, Create=False) is False:
            self.LogError("FolderPath doesn't exist: " + str(self.p_folderpath))
            return init_error

        if self.p_extractfolder is not None:
            if uFolder.ConfirmFolder(self.p_extractfolder) is False:
                self.LogError("Unable to access ExtractFolder: " + str(self.p_extractfolder))
                return init_error

        if self.p_cleanfolder is not None:
            if uFolder.ConfirmFolder(self.p_cleanfolder) is False:
                self.LogError("Unable to access CleanFolder: " + str(self.p_cleanfolder))
                return init_error

        # find the files
        zipfiles = uFolder.FindFiles(self.p_folderpath, Recurse=self.p_recurse, Match="*.zip")
        if len(zipfiles)==0:
            self.LogWarning("No zip files found")
            return "Nothing To Do"

        self.LogMessage("{c} zip files found.".format(c=len(zipfiles)))

        zipfiles = uFolder.OrganizeFilesByPath(zipfiles)

        # process files
        for pathlist in zipfiles:
            path = pathlist[0]
            for filename in pathlist[1]:
                filepath = os.path.join(path,filename)
                self.LogMessage(f">> {filepath}")
                ret = self.process_zip_file(filename, path)
                self.GetResult().AddZipResult(filepath, ret)

        return "Success"

    def process_zip_file(self, in_file, in_path):
        outfolder = self.p_extractfolder
        if outfolder is None:
            outfolder = in_path
        if self.p_createsubfolder is True:
            base = os.path.splitext(in_file)
            outfolder = os.path.join (outfolder, base[0])

        new_folder = uFolder.ConfirmFolder(outfolder, False)
        if uFolder.ConfirmFolder(outfolder) == False:
            return False

        zip_filepath = os.path.join(in_path, in_file)
        try:
            zip_ref = ZipFile(zip_filepath, 'r')
            zip_ref.extractall(outfolder)
            zip_ref.close()
        except:
            if new_folder is False:
                # delete folder we just created
                uFolder.DestroyFolder(outfolder)
            self.LogError("Unable to extract contents: "+zip_filepath)
            return False

        if self.p_cleanfolder is not None:
            shutil.move(zip_filepath, os.path.join (self.p_cleanfolder, in_file))

        return True

uCommandRegistry.RegisterCommand(UnzipFiles, UnzipFilesResult)
