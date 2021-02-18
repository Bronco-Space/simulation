#GENERAL NOTE: This script is a registered text block inside Blender so,
# If you are editing this script remember there are effectively two versions of this script: one internal in the .blend file and one external .py file in the directory
# To save the internal version inside the .blend file you have to save the blender project with Ctrl + s. Otherwise closing Blender and reopening it will show you an old version.
# To save the external version either save the file in your IDE if applicable, or if you're editing the script from within blender use Text Editor > Text > Save.

# If you are editing the script from an external IDE and want to reload the version displayed in Blender go to Text Editor > Text > Reload. Again, this will not save that new version in the .blend file it will just display it. To save the script see above.


#This script creates an operator which is the function that is called when the 'Reload Scripts' button is pressed on the UI panel
import bpy
import autorun_scripts

#This is the main execution of the script
def main(context):
    text = bpy.data.texts['autorun_scripts.py']   # Get the autorun script script
    ctx = bpy.context.copy()
    ctx['edit_text'] = text
    bpy.ops.text.run_script(ctx)    # Execute it


class operator_reload_scripts(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "myops.reload_scripts"
    bl_label = "Reload Scripts"

    #This function is called when the button is clicked
    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(operator_reload_scripts)


def unregister():
    bpy.utils.unregister_class(operator_reload_scripts)


if __name__ == "__main__":
    register()

