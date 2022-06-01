# Runs Python outside the VirtualEnv. This is done using
# py.exe and specifying a version number. This file exists to
# ensure we always use the same version when setting things up
param(
    $PythonArgs
)

& py.exe -3.10 @PythonArgs
