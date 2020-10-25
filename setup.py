from cx_Freeze import setup, Executable
setup(
    name="SkyLoomi",
    version="0.1",
    description="exe file of SkyLoomi",
    executables=[Executable("SkyLoomi.py", base="Win32GUI")],
    )