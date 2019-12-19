
import bpy
import os
import math
import shutil
import glob
import sys
import argparse

#Passage en Cycles
bpy.context.scene.render.engine = 'CYCLES'




def Run():

    args = DefineArguments()
    # DEFINE THE OBJECTS AND TEXTURES TO BE IMPORTED
    obj_list = []
    obj_list.append(args.rootfolder)
    model = Import(obj_list)
    active_object = Select(model)
    # Applying the material to the object
    active_object.data.materials[0] = CreateMaterial(active_object, args.roughness_value, args.specular_value, args.diffuse_path, args.normal_path)
    Export(active_object, args.export_path, args.export_name)


class DefineArguments():
    argv = sys.argv[sys.argv.index("--") + 1:]
    parser = argparse.ArgumentParser()

    parser.add_argument("-np", "--newPath", help="path of the object to convert")
    parser.add_argument("-dp", "--diffusePath", help="path for the diffuse texture")
    parser.add_argument("-nop", "--normalPath", help="path for the normal texture")
    parser.add_argument("-ep", "--exportPath", help="path for the exported object")
    parser.add_argument("-en", "--exportName", help="export name")
    parser.add_argument("-dr", "--diffuseResolution", help="resolution of the diffuse texture")
    parser.add_argument("-nr", "--normalResolution", help="resolution of the normal texture")

    args = parser.parse_args(argv)

    rootfolder = args.newPath
    diffuse_path = args.diffusePath
    normal_path = args.normalPath
    export_path = args.exportPath
    export_name = args.exportName
    diffuse_resolution = args.diffuseResolution
    normal_resolution = args.normalResolution
    specular_value = 0.05
    roughness_value = 1.0



def Import(obj_list):
    model = None
    for item_path in obj_list:
        candidate_object= item_path
        bpy.ops.import_scene.obj(filepath = candidate_object)

    return model
    

def Select(object):
    ma_scene = bpy.context.scene
    for un_objet in ma_scene.objects:
        if un_objet.type == 'MESH':
            bpy.context.scene.objects.active = un_objet

    curr_object = bpy.context.active_object

    return curr_object


def CreateMaterial(object, roughness_value, specular_value, diffuse_path, normal_path):
    mat = bpy.data.materials.new( "coucou" )
    mat.use_nodes = True

    # Storing the variables of the tree node for them to be more accessible
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Creating the nodes I want
    BSDF = nodes.new( "ShaderNodeBsdfPrincipled" )
    Output = nodes.get( "Material Output" )
    Diffuse = nodes.get( "Diffuse BSDF" )

    # Removing the default diffuse bsdf
    diffnodes = mat.node_tree.nodes
    node = nodes["Diffuse BSDF"]
    nodes.remove( node )

    # Making the link between Principled Shader and Output
    links.new( BSDF.outputs[0], Output.inputs[0])

    # By default, we will consider the specular to be null in order to avoid the object to look like plastic. But in the future we ought to think about a condition that could somehow detect whether the object is supposed to be shiny or not.
    BSDF.inputs[5].default_value = specular_value

    # Same for roughness
    BSDF.inputs[7].default_value = roughness_value


    # On charge les images dans Blender et on les met dans des nodes qu'on connecte au shader
    loaded_diffuse = bpy.data.images.load(diffuse_path)
    diff_texture_node = nodes.new("ShaderNodeTexImage")
    diff_texture_node.image = loaded_diffuse
    norm_texture_node = None

    # On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
    Diffuse_fullname = loaded_diffuse.name
    Diffuse_splitname = os.path.splitext(Diffuse_fullname)
    loaded_diffuse.name = Diffuse_splitname[0]

    link_diffuse = links.new(diff_texture_node.outputs[0], BSDF.inputs[0])

    if normal_path is not None:
        loaded_normal = bpy.data.images.load(normal_path)
        norm_texture_node = nodes.new("ShaderNodeTexImage")
        norm_texture_node.image = loaded_normal
        norm_texture_node.color_space = 'NONE'

        # On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
        Normal_fullname = loaded_normal.name
        Normal_splitname = os.path.splitext(Normal_fullname)
        loaded_normal.name = Normal_splitname[0]

        link_normal = links.new(norm_texture_node.outputs[0], BSDF.inputs[17])

    # link_all= links.new(BSDF.outputs[0], nodes.get("Material Output").inputs[0])


    return mat


def Export(object, export_path, export_name):
    export_filepath = os.path.join(export_path, export_name)

    # export_filepath = os.path.join(export_folderpath, export_name)
    # print("HEYYY EXPORT FILE PATH IS " + export_folderpath)

    # # Note que dans les arguments on peut exporter en GLTF_SEPARATE, GLB ou GLTF_EMBEDDED
    bpy.ops.export_scene.gltf(filepath=export_filepath, export_format="GLB", export_selected=True)
    # # bpy.ops.object.delete()


        

Run()



