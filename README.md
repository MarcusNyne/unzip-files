# Unzip Files

UnzipFiles is a demonstration of the [m9lib](https://github.com/MarcusNyne/m9lib) command-control framework.

## Summary

Searches a location for ZIP files and unzips all those files.  Upon success, the ZIP file is moved to a clean folder.
- Can be run as a configuration-driven batch process
- Can be run as a command-line process

## Installation

Installation is made easy by running "install_windows.bat".  This batch file creates a virtual environment in the project folder.

## Configuration Parameters

**m9lib** applications are configuration-driven.  Supported parameters can be found in the ini file "unzip-files.ini".

The INI section `[UnzipFilesControl]` is called the *"control-section"* and contains application-level configuration.
- **Logfile**: optional path to where to create a log file; when not specified, only prints to console
- **Execute**: a command id (or list of command ids) to execute

Command sections are named `[UnzipFiles:<id>]`.  You may define as many command sections as you would like, then use **Execute** under `[UnzipFilesControl]` to select the commands to execute.
- **FolderPath**: folder to search for ZIP files
- **RecurseFolders**: when *True*, scan all subfolders under **FolderPath** to find ZIP files
- **ExtractFolder**: folder where to extract files.  Defaults to location of the ZIP file
- **CreateSubFolder**: when *True*, a subfolder with the name of the ZIP file is created before extracting files
- **CleanFolder**: folder where ZIP file will move after successfully extracting files.  If not specified, ZIP file is left in place

A `*default` section is provided that offers default settings for any section named `UnzipFiles`.  This setting is only used when it is not available in the command section being executed.

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
RecurseFolders = False

[UnzipFiles:run]
# This is a "command section"
FolderPath = c:\input
RecurseFolders = False
CreateSubFolder = True
ExtractFolder = c:\output
```

### Command execution

There are many options for running commands, and this application demonstrates two of them.

A command can be executed through Control by specifying a configuration file.
- Log file location will be read from configuration
- All command line parameters are in the configuration file (in a command section)
- A target command can be specified .. if not specified, it is read from the Execute property fo the control section

```python
    # "UnzipFilesControl" is the name of the control section in the ini file
    control = uControl("UnzipFilesControl", "unzip-files.ini")
    # execute commands based on Execute from the control section
    control.Execute ()
    # execute a command with the id "unzip3"
    control.Execute ("unzip3")

    # note that the name of the command section ("UnzipFiles") is used to find the command class to instantiate from the command registry
```

A command can be executed directly by specifying command parameters as a dict.
- No ini file is required
- If you want to use a logger, you will have to specify one: uLogger or uFileLogger

```python
    # create a console logger
    log = uLogger(Print=True, PrintLevel=uLoggerLevel.INFO, PrintColor=True)
    # instantiate a command class
    com = uCommandRegistry.NewCommand("UnzipFiles")
    # set the logger for the command
    com.SetLogger(log)
    # execute the command with dict parameters
    ret = com.Execute({'FolderPath': 'c:\input', RecurseFolders: True})
```

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
