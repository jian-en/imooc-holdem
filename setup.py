import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Hold'em",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["images"]}},
    executables = executables
    )
