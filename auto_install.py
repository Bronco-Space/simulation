import subprocess
import sys
import os

py_path = os.path.join(sys.prefix,'bin','python.exe')

print(f"Blender python path: {py_path}")

subprocess.call([py_path, '-m', 'ensurepip'])

# subprocess.call([py_path, "-m", "pip", "install", "--upgrade", "pip"])


local_pkg_dir = os.path.join(os.getcwd(),'packages')

subprocess.call([py_path, "-m", "pip", "install",f"--target={local_pkg_dir}","-r", os.path.join(os.getcwd(),'requirements.txt')])

if local_pkg_dir not in sys.path:
    sys.path.append(local_pkg_dir)
    print("Adding local package path to path")
else:
    print("Already registered local path")


print("\npip and packages updated...\n")