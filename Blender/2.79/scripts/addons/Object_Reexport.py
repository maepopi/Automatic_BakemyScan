
import bpy
import os
import math
import shutil
import glob
import sys
import argparse




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
    original_object_path = None
    original_object_extension = None
    original_path = None
    args = None

    def __init__(self):
        self.GetBatchArgs()

        # We need to put "self" before the variables, because we want the variables of the class, not new variables specific to the function

        self.original_object_path = self.args.oldObjectPath
        self.original_path = self.args.oldPath
        self.decimated_object = self.args.newPath
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


        parser.add_argument("-op", "--oldPath", help='original rootpath')
        parser.add_argument("-oop", "--oldObjectPath", help="path of the original object without decimation")
        parser.add_argument("-np", "--newPath", help="path of the object to convert")
        parser.add_argument("-dp", "--diffusePath", help="path for the diffuse texture")
        parser.add_argument("-nop", "--normalPath", help="path for the normal texture")
        parser.add_argument("-ep", "--exportPath", help="path for the exported object")
        parser.add_argument("-en", "--exportName", help="export name")
        parser.add_argument("-dr", "--diffuseResolution", help="resolution of the diffuse texture")
        parser.add_argument("-nr", "--normalResolution", help="resolution of the normal texture")

        self.args = parser.parse_args(argv)

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



class ImportProcess():

    import_process_obj_list = []
    import_process_isAnimated = None
    import_process_animation_data_path = None
    import_process_original_path = None
    import_process_original_object_path = None
    import_process_decimated_path = None
    import_process_animated_object = []
    import_process_decimated_object = None

    def __init__(self, original_path, original_object_path, decimated_path):

        self.import_process_animated_object = []
        self.import_process_decimated_object = None
        self.import_process_decimated_path = decimated_path
        self.import_process_original_path = original_path
        self.import_process_original_object_path = original_object_path
        self.import_process_animation_data_path = os.path.join(original_path, 'animated.txt')


        self.import_process_isAnimated = self.CheckAnimation()

        if self.import_process_isAnimated:
            self.import_process_obj_list.append(self.import_process_decimated_path)
            self.import_process_decimated_object = self.Import_object()
            self.import_process_obj_list.clear()
            self.import_process_obj_list.append(self.import_process_original_object_path)
            self.import_process_animated_object = self.Import_object()



        # else :
        #     self.import_process_obj_list.append(self.import_process_decimated_path)
        #
        #     self.import_process_decimated_object = self.Import_object()
        #
        #     self.import_process_animated_object = None



    def CheckAnimation(self):
        if os.path.exists(self.import_process_animation_data_path):
            self.import_process_isAnimated = True

        else:
            self.import_process_isAnimated = False

        return self.import_process_isAnimated



    def Import_object(self):

        scene = bpy.context.scene
        list = self.import_process_obj_list
        model = []




        for item_path in list:
            candidate_object = item_path
            # We have to extract the extension from the name of candidate_object

            filename, file_extension = os.path.splitext(candidate_object)


            if file_extension == '.obj':
                bpy.ops.import_scene.obj(filepath=candidate_object)

            elif file_extension == '.fbx':
                bpy.ops.import_scene.fbx(filepath=candidate_object)

            elif file_extension == '.gltf' or file_extension == '.glb':
                bpy.ops.import_scene.gltf(filepath=candidate_object)

            elif file_extension == '.stl':
                bpy.ops.import_mesh.stl(filepath=candidate_object)

            elif file_extension == '.ply':
                bpy.ops.import_scene.ply(filepath=candidate_object)

            elif file_extension == '.3ds':
                bpy.ops.import_scene.autodesk_3ds(filepath=candidate_object)

            elif file_extension == '.dae':
                bpy.ops.wm.collada_import(filepath=candidate_object)


        # If the scene is empty, then we're importing the decimation object and we can directly add it to the model list
        if self.import_process_decimated_object is None:
            # print("HEYYY IVE JUST IMPORTED THE DECIMATED")
            for obj in scene.objects:
                if obj.type == 'MESH' and 'RootNode' not in obj.name:
                    model.append(bpy.data.objects[obj.name])
                    # print("HEYYY THE DECIMATED IS " + str(model))


        # If the scene is not empty, it means we're importing the animated object AFTER the decimated one, so we must ask to add only the objects
        # which are not already in the scene, that is to say the decimated object that was previously stored in the self.import_process_decimated_object variable
        else:
            # print("HEYYY IVE JUST IMPORTED THE ANIMATED")
            for obj in scene.objects:
                if obj.type == 'MESH' and 'RootNode' not in obj.name and obj not in self.import_process_decimated_object:
                    model.append(bpy.data.objects[obj.name])

            # print("HEYYY THE ANIMATED LIST Is " + str(model))





        return model


class BuildAnimation():
    decimated_object = None
    animated_objects = []
    final_animated_object = None
    decimated_mesh_data = None
    animated_mesh_data = None

    def __init__(self, decimated, animated):

        self.decimated_object = decimated

        for i in animated:
            self.animated_objects.append(i)


        # Now we need to delete all the animated objects except the armature of course AND one object (no matter which)
        self.final_animated_object = self.CleanAnimated()


        # We just need to get the decimated mesh data in order to replace the animated mesh's data
        self.SwapData()



    def CleanAnimated (self) :
        scene = bpy.context.scene
        list = self.animated_objects
        clean_animated = None

        for i in range (len(list) - 1):
            if list[i].type is not "ARMATURE":
                bpy.ops.object.select_all(action="DESELECT")
                bpy.data.objects[list[i].name].select = True
                bpy.ops.object.delete()

        for obj in scene.objects:
            if obj.type == "MESH" and obj not in self.decimated_object:
                clean_animated = bpy.data.objects[obj.name]
                print("HEYYY CLEAN ANIMATED IS " + str(clean_animated))

        return clean_animated


    def SwapData (self) :
        decimate = self.decimated_object[0]
        animated = self.final_animated_object

        # print("HEYYYYY DECIMATE IS" + str(decimate))
        # print("HEYYYYY ANIMATE IS" + str(animated))


        decimated_mesh_data = decimate.data
        animated.data = decimated_mesh_data
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects[decimate.name].select = True
        bpy.ops.object.delete()


def Select(object):
    ma_scene = bpy.context.scene
    for un_objet in ma_scene.objects:
        if un_objet.type == 'MESH':
            bpy.context.scene.objects.active = un_objet

    curr_object = bpy.context.active_object

    return curr_object


def Export(object, export_path, export_name):
    export_filepath = os.path.join(export_path, export_name)


    # Note que dans les arguments on peut exporter en GLTF_SEPARATE, GLB ou GLTF_EMBEDDED
    bpy.ops.export_scene.gltf(filepath=export_filepath, export_format="GLB", export_selected=True)
    # bpy.ops.object.delete()


def Run():
    decimated_object = None
    animated_object = []
    length = None
    object = None

    # Passage en Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    # GET THE BATCH ARGUMENTS
    args = DefineArguments()
    # DEFINE THE OBJECTS AND TEXTURES TO BE IMPORTED
    obj_list = []

    # THIS IS WHERE WE CHECK IF THE OBJECT IS ANIMATED, AND THUS HOW MANY OBJECTS WE HAVE TO IMPORT
    import_process = ImportProcess(args.original_path, args.original_object_path, args.decimated_object)
    decimated_object = import_process.import_process_decimated_object

    #  # We iterate through the list of objects we got from the class. So [i] each time represents an object.
    # for i in import_process.import_process_animated_object:
    #     animated_object.append(i)
    #
    #
    # build_animation = BuildAnimation(decimated_object, animated_object)
    # animated_object = build_animation.final_animated_object

    # # if isAnimated :
    # #     obj_list.append(args.rootfolder, args.original_object_path)
    # #
    # # else:
    # #     obj_list.append(args.rootfolder)
    # #
    # #
    # # model = Import(obj_list)
    #
    # active_object = Select(model)
    # # Applying the material to the object
    # # I'm calling the class that will construct the material. See in the class for more comments
    # current_material = Material(active_object, args.roughness_value, args.specular_value, args.diffuse_path, args.normal_path)
    # active_object.data.materials[0] = current_material.mat
    #
    # # We now need to restore the animation of the object if there was one
    #
    #
    #
    # Export(active_object, args.export_path, args.export_name)

        

Run()



