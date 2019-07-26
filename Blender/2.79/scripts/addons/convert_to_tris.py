import bpy
import bmesh
import os
import sys
import argparse

bpy.context.scene.render.engine = "CYCLES"



rootfolder=os.path.join(sys.argv[5])
extension=sys.argv[6]
print(rootfolder)
print(extension)
obj_list=[]
obj_list.append(rootfolder)

for item_path in obj_list:
    candidate_object=item_path

    if extension=="obj":
        bpy.ops.import_scene.obj(filepath=candidate_object)

    elif extension=="fbx":
        bpy.ops.import_scene.fbx( filepath=candidate_object)

    elif extension == "gltf" or "glb":
        bpy.ops.import_scene.gltf( filepath=candidate_object, filter_glob="*.glb;*.gltf")

    elif extension == "stl":
        bpy.ops.import_scene.stl( filepath=candidate_object)

    elif extension == "ply":
        bpy.ops.import_scene.stl( filepath=candidate_object)

    elif extension == "3ds":
        bpy.ops.import_scene.autodesk_3ds( filepath=candidate_object)


ma_scene = bpy.context.scene
for un_objet in ma_scene.objects:
    if un_objet.type == 'MESH':
        #je dit à chaque objet mesh que je rencontre (donc normalement un seul) d'être actif
        bpy.context.scene.objects.active = un_objet

        #je fous dans une variable ce qui doit normalementetre mon seul objet actif
curr_object = bpy.context.active_object

object = curr_object.data
bm=bmesh.new()
bm.from_mesh(object)

bmesh.ops.triangulate(bm, faces=bm.faces[:],quad_method=0,ngon_method=0)
bm.to_mesh(object)
bm.free()

export_filepath=rootfolder

bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)