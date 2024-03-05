from cx_Freeze import setup, Executable

setup(
    name="JarWizzard",
    version="1.0",
    description="Description of your executable",
    executables=[Executable("./loader.py", base=None)],
    includes=["pynput.keyboard", "pynput.mouse"],
)
