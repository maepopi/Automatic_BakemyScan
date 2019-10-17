import bpy
import sys
import bmesh
import os
import bmesh
from os import listdir
import shutil


def Run():
    scene = bpy.context.scene
    bpy.context.scene.render.engine = 'CYCLES'

    # GETTING THE VARIABLES SENT BY BATCH
    root_path = sys.argv[4]
    object_path = sys.argv[5]
    object_name = sys.argv[6]
    object_extension = sys.argv[7]
    image_extension = sys.argv[8]
    output_path = sys.argv[9]
    hasMultiTexture = sys.argv[10]
    texture_path = sys.argv[11]

    # DECLARING PYTHON VARIABLES
    # Change this resolution for a higher value if you have a better computer. But the higher the longer the object will be to process.
    bake_resolution = 2048

    # CHECK THE ARGUMENT LIST
    # Debug purposes, keep this commented otherwise
    CheckArgs()


    # IMPORT THE OBJECT
    model = Import(object_path, object_extension, object_name, scene)




def CheckArgs():
    print('HEYYYYYYYYYYYYYYYYYYYYYYYYYY')
    print('root_path is ' + sys.argv[4])
    print('object_path is ' + sys.argv[5])
    print('object_name is ' + sys.argv[6])
    print('object extension is ' + sys.argv[7])
    print('image_extension is ' + sys.argv[8])
    print('output_path is ' + sys.argv[9])
    print('hasMultiTexture is ' + sys.argv[10])
    print('texture_path is ' + sys.argv[11])


def Import(path, object_extension, name, scene):
    candidate_object = path
    model = None

    if object_extension == 'obj':
        bpy.ops.import_scene.obj(filepath=candidate_object)

    elif object_extension == 'fbx':
        bpy.ops.import_scene.fbx(filepath=candidate_object)

    elif object_extension == 'gltf' or object_extension == 'glb':
        bpy.ops.import_scene.gltf(filepath=candidate_object)

    elif object_extension == 'stl':
        bpy.ops.import_mesh.stl(filepath=candidate_object)

    elif object_extension == 'ply':
        bpy.ops.import_scene.ply(filepath=candidate_object)

    elif object_extension == '3ds':
        bpy.ops.import_scene.autodesk_3ds(filepath=candidate_object)

    elif object_extension == 'dae':
        bpy.ops.wm.collada_import(filepath=candidate_object)

    for object in scene.objects:
        if object.type == 'MESH' and object.name != 'RootNode':
            model = bpy.data.objects[object.name]

    # Select and make object active
    bpy.data.objects[model.name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[model.name]

    return model



Run()