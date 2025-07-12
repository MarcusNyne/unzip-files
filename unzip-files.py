from m9lib import uControl, uLoggerLevel, uArgs, uLogger, uConfig, uConfigParameters

from c_unzip_files import *

os.system("color")
args = uArgs([("recurse", "r"), ("subfolder", "sf"), ("cleanfolder", "cf", True), ("ini", None, True), ("c", None, True), ("help", "h")], ["source", "output"])

# execute in one of four modes
if args.NoArguments() or args.HasOption("help"):
    # display help
    log = uLogger(Print=True, PrintLevel=uLoggerLevel.INFO, PrintColor=True)
    log.WriteLine("[+LT_GREEN]UnzipFiles -ini <ini_file> [-c <target>][+]")
    log.WriteLine("[+CYAN]-ini[+]: run with ini file")
    log.WriteLine("[+CYAN]-c[+]: specify which command to run by id (otherwise, use Execute)")
    log.WriteLine("[+LT_GREEN]UnzipFiles [-r] [-sf] [-cf <folder>] <source> [<output>][+]")
    log.WriteLine("[+CYAN]-h -help[+]: display help")
    log.WriteLine("[+CYAN]-r -recurse[+]: recurse folders looking for zip files")
    log.WriteLine("[+CYAN]-sf -subfolder[+]: unzip files in a subfolder named after the zip file")
    log.WriteLine("[+CYAN]-cf -cleanfolder <folder>[+]: after unzipping, zip file moved to clean folder")
    log.WriteLine("[+CYAN]source[+]: folder to search for zip files")
    log.WriteLine("[+CYAN]output[+]: folder where files will be extracted (zip folder if not specified)")
else:
    dparams = {}
    ini_file = None
    ini_target = None
    if args.HasOption("ini"):
        ini_file = args.GetOption('ini')
        if args.HasOption("c"):
            ini_target = args.GetOption('c')
    else:
        if args.HasOption("recurse"):
            dparams['RecurseFolders'] = args.GetOption('recurse')
        if args.HasOption("subfolder"):
            dparams['CreateSubFolder'] = args.GetOption('subfolder')
        if args.HasOption("cleanfolder"):
            dparams['CleanFolder'] = args.GetOption('cleanfolder')
        if args.HasParam("source"):
            dparams['FolderPath'] = args.GetParam('source')
        if args.HasParam("output"):
            dparams['ExtractFolder'] = args.GetParam('output')

    if ini_file:
        # in this example, an ini file was specified
        # the command to run ("target") is optional .. when not specified, command to run comes from [UnzipFilesControl].Execute
        config = uConfig(ini_file)
        control = uControl("UnzipFilesControl", config)
        control.GetLogger().SetWriteLevel(Level=uLoggerLevel.DETAILS)
        control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.INFO, Color=True)        
        # ini_target is None when not specified
        control.Execute (ini_target)
    else:
        # in this example, command line parameters were specified
        # no Control is used .. this is considered direct command execution
        # the logger does not write to fine .. this is a console-only logger
        log = uLogger(Print=True, PrintLevel=uLoggerLevel.INFO, PrintColor=True)
        confirmed=True
        if 'FolderPath' not in dparams:
            log.WriteError("Source folder not specified")
            confirmed = False
        elif uFolder.ConfirmFolder(dparams['FolderPath'], False) is False:
            log.WriteError(f"Source folder not found: {dparams['FolderPath']}")
            confirmed = False
        if 'ExtractFolder' not in dparams:
            log.WriteError("Output folder not specified")
            confirmed = False

        if confirmed:
            com = uCommandRegistry.NewCommand("UnzipFiles")
            com.SetLogger(log)
            ret = com.Execute(dparams)
