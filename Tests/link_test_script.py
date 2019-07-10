import bpy

filepath= "E:\MaelysJob\LOCAL_GIT_PROJECTS\AUTOMATIC_BAKEMYSCAN\Automatic_BakemyScan\Blender\2.79\scripts\addons\io_scene_gltf2\glTF2.blend"
group_name = 'glTF Metallic Roughness'



link = True

bpy.data.libraries.load(filepath, link=link)
 

