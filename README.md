usage: pyls.py [-h] [-A] [-l] [-r] [-t] [-H] [--filter {file,dir}] [path]

List files and directories in JSON format similar to ls

positional arguments:
  path                  Path to the JSON file or directory (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  -A, --all             Do not ignore entries starting with .
  -l, --long            Use a long listing format
  -r, --reverse         Reverse order while sorting
  -t, --sort-by-time    Sort by modification time, newest first
  -H, --human-readable  With -l, print sizes in human readable format (e.g., 1K, 234M)
  --filter {file,dir}   Filter by type (file or dir)

Note : Install all required package using : pip install -r .\requirements.text

In this configuration:

The [tool.poetry.scripts] section specifies the mapping between the command name (pyls) and the Python script file that contains the main entry point of your program (pyls.py). Here, pyls:main means that the main function in pyls.py will be the entry point.

The [build-system] section specifies the build requirements for your project.

After setting up pyproject.toml, you can follow these steps:

Make sure you have Poetry installed. You can install it via pip: pip install poetry

Navigate to your project directory containing the pyproject.toml file.

Run the following command to install your project and add the pyls command to your system: pip install .
This will install your project along with its dependencies and add the pyls command to your system.

To use the pyls command, simply open a new terminal window or tab and type: pyls

This should execute your Python script, listing the files and directories specified in the pyls.py script. Make sure that the directory containing the pyls binary is added to your system's PATH variable so that the pyls command is accessible globally.
