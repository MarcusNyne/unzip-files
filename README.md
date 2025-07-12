# Unzip Files

UnzipFiles is a demonstration of the [m9lib](https://github.com/MarcusNyne/m9lib) command-control framework.

## Summary

Searches a location for ZIP files and unzips all those files.  Upon success, the ZIP file is moved to a clean folder.
- Can be run as a configuration-driven batch process
- Can be run as a command-line process

## Installation

Installation is made easy by running "install_windows.bat".  This batch file creates a virtual environment in the project folder.

## Batch Execution

If "unzipfiles.py" is run without any command-line arguments, the the "unzip-files.ini" is used to drive execution.

The ini section `[UnzipFilesControl]` contains global configuration.
- **Logfile**: optional path to where to create a log file; when not specified, only prints to console
- **Execute**: a section id (or list of section ids) to execute; can also specify "UnzipFiles" to execute defined commands

Command sections are named `[UnzipFiles:<id>]`.  You may define as many command sections as you would like, with different ids.  Then, use **Execute** under `[UnzipFilesControl]` to select the commands to execute.
- **FolderPath**: folder to search for ZIP files
- **RecurseFolders**: when *True*, scan all subfolders under **FolderPath** to find ZIP files
- **ExtractFolder**: folder where to extract files.  Defaults to location of the ZIP file
- **CreateSubFolder**: when *True*, a subfolder with the name of the ZIP file is created before extracting files
- **CleanFolder**: folder where ZIP file will move after successfully extracting files.  If not specified, ZIP file is left in place

If "unzip-files.py" or "unzipfiles.bat" are called with a command section id as a single parameter, the configuration file will be used for execution, and the identified section id will be executed.  This overrides the "target" specified by **Execute**.

```ini
[UnzipFilesControl]
# This is the "control section"
# {YMD} is replaced with year month date
Logfile = logs\{YMD} UnZipFiles.log
# execute the section with an id of "run"
Execute = run

[*default:UnzipFiles]
# This is a default section.  CleanFolder will be used for all commands
# These defaults are only used when the value is not specified in the command section
CleanFolder =

[UnzipFiles:run]
# This is a "command section"
FolderPath = c:\input
RecurseFolders = False
CreateSubFolder = True
ExtractFolder = c:\output
```
See [uConfig](https://github.com/MarcusNyne/m9lib/blob/main/docs/config.md) documentation for more information.

## Command Line Execution

The batch file "unzipfiles.bat" has been set up to call "unzip-files.py" via the virtual environment, but any command-line arguments are passed directly to the python application.

Command line paramters map directly to command-section parameters.

If called with `-h` or no parameters, help text is displayed.  There are two modes of operation, described below.

`UnzipFiles -ini <ini_file> [-c <target>]`.
- **-ini ini_file**: An ini file to load configuration from
- **-c target**: The id of a command section to execute.  When not specified, uses [UnzipFilesControl].Execute

`UnzipFiles [-r] [-sf] [-cf <folder>] <source> [<output>]`.
- **-r**: RecurseFolders (default: *False*)
- **-sf**: CreateSubFolder (default: *False*)
- **-cf folder**: CleanFolder (default: do not use clean folder)
- **source**: FolderPath where ZIP files are to be found
- **output**: Folder where files will be extracted (default: use ZIP file folder)

No log is generated in this mode.

## Launch.json

Launch.json supports 4 modes of execution:
- **UnZip Files**: run with local ini file, using default target `unzip-files -ini unzip-files.ini`
- **Show Args**: run with no arguments, which causes help to be displayed `unzip-files`
- **Run Args**: an example using command line arguments `unzip-files test/source/zip_files -sf -r test/temp0/output`
- **Test Suite**: run a suite of 3 tests

It is normal to receive an error about "bad.zip" .. this is an intentionally bad file.

## m9lib Lessons

This section is provided to learn more about how to use the m9lib python library.  This library has a batch-based command-control framework, and other features which are more generally useful.

[Learn more about m9lib](https://github.com/MarcusNyne/m9lib)

### Console logging (in color)

There are four levels of messaging: *DETAILS*, *INFO*, *WARNING*, *ERROR*.

By default, the console logger only displays messages of *WARNING* or above, and does not display in color.

This behavior is changed in code to enable the display of *INFO* messages, and to print in color.

```python
    # this code is used for batch processing, when a configuration file is used for execution
    # in this case, the command uses a uFileLogger object from the control object
    control = uControl("UnzipFilesControl", "unzip-files.ini")
    control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.INFO, Color=True)
    control.Execute () # when a target is not specified, the Execute property is used

    # alternatively, the config file may be loaded before instantiating uControl
    config = uConfig(r"unzip-files.ini")
    control = uControl("UnzipFilesControl", config)
    control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.INFO, Color=True)
    control.Execute ("run") # when a target is specified, it is the id of a command section

    # this code is used for command-line execution, when a command is executed directly
    # in this case, a uLogger object is created and passed to the command
    # uLogger is different than uFileLogger in that it prints to console only (does not write to file)
    # note that use of a Control object or configuration can be avoided using direct execution
    log = uLogger(Print=True, PrintLevel=uLoggerLevel.INFO, PrintColor=True)
    com = uCommandRegistry.NewCommand("UnzipFiles")
    com.SetLogger(log)
    com.Execute({'FolderPath': r'c:\mypath', 'RecurseFolders':True})

    # this system command will enable interpretation of color codes in a command-line window
    # this is not required when viewing output in vscode
    os.system("color")

    # when logging, color can be applied by using color codes directly in strings
    # if color is not enabled, the color codes will be stripped out
    log.WriteLine("Example of [+RED]roses[+] and [+BLUE]berries[+].")
```

[Learn more about uConsoleColor colors](https://github.com/MarcusNyne/m9lib/blob/main/docs/color.md)
[Learn more about uLogger and uFileLogger](https://github.com/MarcusNyne/m9lib/blob/main/docs/logger.md)

### Configuration and parameters

This application shows many ways in which the configuration file is loaded.
- By passing the filepath to the control object (**uControl**)
- Loading directly into a **uConfig** object, and inspecting configuration before passing to the control object
- Loading with configuration parameters (**uConfigParameters**)

Configuration parameters are overrides that are specified at the time a configuration file is loaded.  Each parameter is a name-value pair which may contain a "section-specification" that identifies sections to apply the values to based on name or id.  In this example, the section name is used.  Here are some examples:
- `x=y`: apply x=y to all sections; this will override x if it exists, or add x if not
- `UnzipFiles.x=y`: apply x=y to sections named "UnzipFiles"
- `UnzipFiles:myid.x=y`: apply x=y to sections named "UnzipFiles" with the id "myid"
- `:myid.x=y`: apply x=y to sections with the id "myid"

```python
# load config by specifying the file
control = uControl("UnzipFilesControl", "unzip-files.ini")

# load a config object, then pass to control
config = uConfig("unzip-files.ini")
control = uControl(config, "unzip-files.ini")

# load a config file with parameters
config = uConfig("unzip-files.ini", [r'CleanFolder=c:\$clean'])

# load a config file with a list of parameters
params = uConfigParameters([r'UnzipFiles.CleanFolder=c:\$clean'])
config = uConfig("unzip-files.ini", params)

# load a config file with a parameter dict, augmented with a section specification
params = uConfigParameters({'CleanFolder':'c:\$clean'}, "UnzipFiles")
config = uConfig("unzip-files.ini", params)
```

[Learn more about uConfig](https://github.com/MarcusNyne/m9lib/blob/main/docs/config.md)

### Command implementation

Commands are implemented in three steps:
1. Define command result (**uCommandResult**)
2. Define command (**uCommand**)
3. Register command using **uCommandRegistry.RegisterCommand()**

A custom command result is not required.  If one is not specified, **uCommandResult** is used.  In this example, a custom command result is used in order to maintain a list of zip files and their status.
- It is important to call super().__init__()
- The result object is maintained by uControl, even after the command is executed
- Access from **uCommand** by calling **self.GetResult()**
- Access through **uControl** by calling **uControl.GetResults()** with a section specification (by name, id, etc)

Create a custom command object by deriving from **uCommand**.
- It is important to call super().__init__()
- The class name is significant, as it will match a command-section name in configuration
- Implement **imp_execute()**, returning True, "Success", or a failure string
- The command object is created by uControl before it is executed, and is destroyed after execution

The command must be registered using **uCommandRegistry.RegisterCommand()**.  In the example, custom classes are passed in for both the command and command result.  If you are not using a custom command result, only pass in the command class.

[Learn more about uCommand](https://github.com/MarcusNyne/m9lib/blob/main/docs/command.md)

### Control

In most cases, a custom **uControl** class is not required.  Use of a custom control class offers these benefits:
- Can specify additional steps for command initialization
- Run code before executing commands
- Run code after executing commands, and provide a "final result"

The first parameter of **uControl** is the control name, which will match the section name of the control-section in configuration.

Pass in a path to a configuration file, or a **uConfig** object.  If loading configuration, **uConfigParameters** can also be specified.

[Learn more about uControl](https://github.com/MarcusNyne/m9lib/blob/main/docs/control.md)
