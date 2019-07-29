import bpy
import bmesh
import os
import sys
import argparse
import shutil

bpy.context.scene.render.engine = "CYCLES"


rootfolder=os.path.join(sys.argv[5])
obj_path=os.path.join(sys.argv[6])
obj_extension=sys.argv[7]
image_extension=sys.argv[8]


obj_list=[]
obj_list.append(obj_path)

for item_path in obj_list:
    candidate_object=item_path

    if obj_extension=="obj":
        bpy.ops.import_scene.obj(filepath=candidate_object)

    elif obj_extension=="fbx":
        bpy.ops.import_scene.fbx( filepath=candidate_object)

    elif obj_extension == "gltf" or obj_extension == "glb":
        bpy.ops.import_scene.gltf(filepath=candidate_object)

    elif obj_extension == "stl":
        bpy.ops.import_scene.stl( filepath=candidate_object)

    elif obj_extension == "ply":
        bpy.ops.import_scene.ply( filepath=candidate_object)

    elif obj_extension == "3ds":
        bpy.ops.import_scene.autodesk_3ds( filepath=candidate_object)
        
    elif obj_extension == "dae":
        bpy.ops.wm.collada_import( filepath=candidate_object)

#### TRIANGULATION #######
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

export_filepath=os.path.join(sys.argv[9],sys.argv[10] + "_clean" + ".obj")

bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)


#### DUPLICATE AND EXPORT TEXTURES ###
image_path = "None"
destination_path = "None"

if obj_extension != "gltf":
    if image_extension == "jpg":
        image_path = os.path.join(sys.argv[5], sys.argv[10] + ".jpg")
        destination_path = os.path.join( sys.argv[9], sys.argv[10] + ".jpg" )

    elif image_extension == "jpeg":
        image_path = os.path.join( sys.argv[5], sys.argv[10] + ".jpeg")
        destination_path = os.path.join( sys.argv[9], sys.argv[10] + ".jpeg" )

    elif image_extension == "png":
        image_path = os.path.join( sys.argv[5], sys.argv[10] + ".png")
        destination_path = os.path.join( sys.argv[9], sys.argv[10] + ".png" )



    origin_path = image_path
    shutil.copy(origin_path, destination_path)


else:
    material = curr_object.data.materials[0]

    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    links = tree.links

    DiffuseNode = nodes.get("Principled BSDF")
    image_name = None

    if DiffuseNode is None:
        DiffuseNode = nodes.get("Diffuse BSDF")

    socket = DiffuseNode.inputs[0]

    link = next(link for link in links if link.to_node == DiffuseNode and link.to_socket == socket)

    imageNode = link.from_node

    if imageNode.type == 'TEX_IMAGE':
        image = imageNode.image
        image_name = image.name


    image.filepath_raw = os.path.join(sys.argv[9], sys.argv[10] + ".png")
    image.file_format = "PNG"

    image.save()

    # image_extension = ".png"
    # origin_path = image_export_filepath
    # destination_path = os.path.join(sys.argv[9], sys.argv[10] + image_extension )
    #
    # print("Origin path is  " + origin_path)
    # print("destination path is " + destination_path)
    #
    # shutil.copy(origin_path, destination_path)

