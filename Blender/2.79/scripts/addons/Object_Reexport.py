
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

    # GET THE BATCH ARGUMENTS
    args = DefineArguments()
    # DEFINE THE OBJECTS AND TEXTURES TO BE IMPORTED
    obj_list = []
    obj_list.append(args.rootfolder)
    model = Import(obj_list)
    active_object = Select(model)
    # Applying the material to the object
    # I'm calling the class that will construct the material. See in the class for more comments
    current_material = Material(active_object, args.roughness_value, args.specular_value, args.diffuse_path, args.normal_path)
    active_object.data.materials[0] = current_material.mat
    Export(active_object, args.export_path, args.export_name)


class DefineArguments():
    rootfolder = None
    diffuse_path = None
    normal_path = None
    export_path = None
    export_name = None
    diffuse_resolution = None
    normal_resolution = None
    specular_value = None
    roughness_value = None
    argv = None
    parser = None
    args = None

    def __init__(self):
        self.GetBatchArgs()

        # We need to put "self" before the variables, because we want the variables of the class, not new variables specific to the function
        self.rootfolder = self.args.newPath
        self.diffuse_path = self.args.diffusePath
        self.normal_path = self.args.normalPath
        self.export_path = self.args.exportPath
        self.export_name = self.args.exportName
        self.diffuse_resolution = self.args.diffuseResolution
        self.normal_resolution = self.args.normalResolution
        self.specular_value = 0.05
        self.roughness_value = 1.0

    def GetBatchArgs(self):
        argv = sys.argv[sys.argv.index("--") + 1:]
        parser = argparse.ArgumentParser()

        parser.add_argument("-np", "--newPath", help="path of the object to convert")
        parser.add_argument("-dp", "--diffusePath", help="path for the diffuse texture")
        parser.add_argument("-nop", "--normalPath", help="path for the normal texture")
        parser.add_argument("-ep", "--exportPath", help="path for the exported object")
        parser.add_argument("-en", "--exportName", help="export name")
        parser.add_argument("-dr", "--diffuseResolution", help="resolution of the diffuse texture")
        parser.add_argument("-nr", "--normalResolution", help="resolution of the normal texture")

        self.args = parser.parse_args(argv)




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


class Material():
    # As in any other script, we need to define the variables that will be used in this class, even if they are not assigned to anything yet
    Output = None
    BSDF = None
    mat = None
    mat_object = None
    mat_roughness_value = None
    mat_specular_value = None
    mat_diffuse_path = None
    mat_normal_path = None

    # The constructor enables to create an instance of the class with specific arguments that will be passed into the class. Basically if you want to pass arguments
    # to your class, you need a constructor. The arguments of the class will be assigned to specific variables.
    def __init__(self, object, roughness_value, specular_value, diffuse_path, normal_path):
        # The word "self" refers to the object instantiated by the class. The operations of the class will be done on self. And as the self enters in the name of the variable, the variable
        # will always have to be called by that name.
        self.mat_object = object
        self.mat_roughness_value = roughness_value
        self.mat_specular_value = specular_value
        self.mat_diffuse_path = diffuse_path
        self.mat_normal_path = normal_path

        # You can already call the functions of the class inside the constructor, because the constructor initiates the object, so it can also be asked to modify it.
        self.CreateMaterial()
        self.LinkTextures()


    def CreateMaterial(self):
        # You need to put "self" before the variables that you want to access in all the functions of the class. It's roughly like a global.
        self.mat = bpy.data.materials.new( "FinalMaterial" )
        self.mat.use_nodes = True

        # Storing the variables of the tree node for them to be more accessible
        self.tree = self.mat.node_tree
        self.nodes = self.tree.nodes
        self.links = self.tree.links

        # Creating the nodes I want
        self.BSDF = self.nodes.new( "ShaderNodeBsdfPrincipled" )
        self.Output = self.nodes.get( "Material Output" )
        # Diffuse = nodes.get( "Diffuse BSDF" )

        # Removing the default diffuse bsdf
        # diffnodes = self.mat.node_tree.nodes
        node = self.nodes["Diffuse BSDF"]
        self.nodes.remove( node )

        # Making the link between Principled Shader and Output
        self.links.new( self.BSDF.outputs[0], self.Output.inputs[0])

        # By default, we will consider the specular to be null in order to avoid the object to look like plastic. But in the future we ought to think about a condition that could somehow detect whether the object is supposed to be shiny or not.
        self.BSDF.inputs[5].default_value = self.mat_specular_value

        # Same for roughness
        self.BSDF.inputs[7].default_value = self.mat_roughness_value




    def LinkTextures(self):
        # On charge les images dans Blender et on les met dans des nodes qu'on connecte au shader
        loaded_diffuse = bpy.data.images.load(self.mat_diffuse_path)
        diff_texture_node = self.nodes.new("ShaderNodeTexImage")
        diff_texture_node.image = loaded_diffuse
        norm_texture_node = None

        # On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
        Diffuse_fullname = loaded_diffuse.name
        Diffuse_splitname = os.path.splitext(Diffuse_fullname)
        loaded_diffuse.name = Diffuse_splitname[0]

        link_diffuse = self.links.new(diff_texture_node.outputs[0], self.BSDF.inputs[0])

        if self.mat_normal_path is not None:
            loaded_normal = bpy.data.images.load(self.mat_normal_path)
            norm_texture_node = self.nodes.new("ShaderNodeTexImage")
            norm_texture_node.image = loaded_normal
            norm_texture_node.color_space = 'NONE'

            # On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
            Normal_fullname = loaded_normal.name
            Normal_splitname = os.path.splitext(Normal_fullname)
            loaded_normal.name = Normal_splitname[0]

            link_normal = self.links.new(norm_texture_node.outputs[0], self.BSDF.inputs[17])

        # link_all= links.new(BSDF.outputs[0], nodes.get("Material Output").inputs[0])

def Export(object, export_path, export_name):
    export_filepath = os.path.join(export_path, export_name)


    # Note que dans les arguments on peut exporter en GLTF_SEPARATE, GLB ou GLTF_EMBEDDED
    bpy.ops.export_scene.gltf(filepath=export_filepath, export_format="GLB", export_selected=True)
    # bpy.ops.object.delete()


        

Run()



