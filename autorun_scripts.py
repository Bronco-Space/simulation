#GENERAL NOTE: This script is a registered text block inside Blender so,
# If you are editing this script remember there are effectively two versions of this script: one internal in the .blend file and one external .py file in the directory
# To save the internal version inside the .blend file you have to save the blender project with Ctrl + s. Otherwise closing Blender and reopening it will show you an old version.
# To save the external version either save the file in your IDE if applicable, or if you're editing the script from within blender use Text Editor > Text > Save.

# If you are editing the script from an external IDE and want to reload the version displayed in Blender go to Text Editor > Text > Reload. Again, this will not save that new version in the .blend file it will just display it. To save the script see above.

import bpy

#Locate scripts file and get contents. Each line of the text file should have the file name of the script to execute.
scripts_filepath = bpy.path.abspath("//scripts.txt")
with open(scripts_filepath, 'r') as scripts:
    contents = scripts.read().splitlines()

#Execute each script in scripts.txt
for line in contents:
    filepath = bpy.path.abspath(f"//{line}")
    exec(compile(open(filepath).read(), filepath, 'exec'))