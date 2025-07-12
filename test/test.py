from m9lib import uControl, uLoggerLevel

import unittest

import os,shutil

from c_unzip_files import *

class TestUnzipFiles(unittest.TestCase):

    def setUp(self):
        pass

    def test_unzip(self):
        self.initialize("test.log", "temp1", "source")
        self.initialize("test.log", "temp2", "source")
        self.initialize("test.log", "temp3", "source")

        control = uControl("UnzipFilesControl", r"test/test.ini")
        control.GetLogger().SetWriteLevel(Level=uLoggerLevel.DETAILS)
        control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.DETAILS, Color=True)        
        control.Execute ()

        # temp1 results
        result = control.GetResult("temp1")
        if result:
            self.assertEqual(len(result.GetZipResults()), 3)
            self.assertEqual(len(result.GetZipResults(True)), 2)
            self.assertEqual(len(result.GetZipResults(False)), 1)
            self.assertTrue(os.path.isdir(r"test\temp1\output\test\Root_Songs"))
            self.assertTrue(os.path.isdir(r"test\temp1\output\subtest\Root_Quote"))
            self.assertTrue(os.path.isfile(r"test\temp1\output\test\Root_Songs\Songs.txt"))
            self.assertTrue(os.path.isfile(r"test\temp1\output\subtest\Root_Quote\Quote.txt"))
            self.assertTrue(os.path.isfile(r"test\temp1\clean\UnzipFiles\test.zip"))
            self.assertTrue(os.path.isfile(r"test\temp1\clean\UnzipFiles\subtest.zip"))
            self.assertFalse(os.path.isdir(r"test\temp1\output\bad"))
            self.assertTrue(os.path.isfile(r"test\temp1\zip_files\subfolder\bad.zip"))

        # temp2 results
        result = control.GetResult("temp2")
        if result:
            self.assertEqual(len(result.GetZipResults()), 1)
            self.assertEqual(len(result.GetZipResults(True)), 1)
            self.assertEqual(len(result.GetZipResults(False)), 0)
            self.assertTrue(os.path.isdir(r"test\temp2\output\Root_Songs"))
            self.assertFalse(os.path.isdir(r"test\temp2\output\test\Root_Songs"))
            self.assertFalse(os.path.isdir(r"test\temp2\output\Root_Quote"))
            self.assertTrue(os.path.isfile(r"test\temp2\output\Root_Songs\Songs.txt"))
            self.assertFalse(os.path.isfile(r"test\temp2\output\Root_Quote\Quote.txt"))
            self.assertTrue(os.path.isfile(r"test\temp2\clean\UnzipFiles\test.zip"))
            self.assertFalse(os.path.isfile(r"test\temp2\clean\UnzipFiles\subtest.zip"))
            self.assertTrue(os.path.isfile(r"test\temp2\zip_files\subfolder\bad.zip"))

        # temp3 results
        result = control.GetResult("temp3")
        if result:
            self.assertEqual(len(result.GetZipResults()), 3)
            self.assertEqual(len(result.GetZipResults(True)), 2)
            self.assertEqual(len(result.GetZipResults(False)), 1)
            self.assertTrue(os.path.isdir(r"test\temp3\zip_files\Root_Songs"))
            self.assertTrue(os.path.isdir(r"test\temp3\zip_files\subfolder\Root_Quote"))
            self.assertTrue(os.path.isfile(r"test\temp3\zip_files\Root_Songs\Songs.txt"))
            self.assertTrue(os.path.isfile(r"test\temp3\zip_files\subfolder\Root_Quote\Quote.txt"))
            self.assertTrue(os.path.isfile(r"test\temp3\clean\UnzipFiles\test.zip"))
            self.assertTrue(os.path.isfile(r"test\temp3\clean\UnzipFiles\subtest.zip"))
            self.assertTrue(os.path.isfile(r"test\temp3\zip_files\subfolder\bad.zip"))

    def initialize(self, in_logfile, in_temp='temp', in_source='source'):
        if in_logfile is not None:
            logfile = r'test\{n}'.format(n=in_logfile)
            if os.path.exists(logfile):
                os.remove(logfile)

        if in_temp is not None:
            tempfolder = r'test\{n}'.format(n=in_temp)
            if in_temp is not None:
                if os.path.isdir(tempfolder):
                    shutil.rmtree(tempfolder)

            if in_source is not None:
                sourcefolder = r'test\{n}'.format(n=in_source)
                shutil.copytree(sourcefolder, tempfolder)

unittest.main(verbosity=1)