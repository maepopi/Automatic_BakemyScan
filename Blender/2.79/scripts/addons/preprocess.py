import bpy
import sys
import bmesh
import os
import bmesh
from os import listdir
import shutil
import argparse


class DefineArguments():
        root_path = None
        object_path = None
        object_name = None
        object_extension = None
        image_extension = None
        output_path = None
        multitexture = None
        texture_path = None
        args = None

        def __init__(self):
            self.GetBatchArgs()
            self.root_path = self.args.inputFullPath
            self.object_path = self.args.processedInputPath
            self.object_name = self.args.name
            self.object_extension = self.args.objectExtension
            self.image_extension = self.args.imageExtension
            self.output_path = self.args.preprocessOutputPath
            self.multitexture = self.args.multitexture
            self.texture_path = self.args.texturePath



        def GetBatchArgs(self):
            self.argv = sys.argv[sys.argv.index("--") + 1:]
            parser = argparse.ArgumentParser()

            parser.add_argument("-ifp", "--inputFullPath", help="Full path of the input object")
            parser.add_argument("-pip", "--processedInputPath", help="Path of the object once processed")
            parser.add_argument("-n", "--name", help="Name of the object")
            parser.add_argument("-oe", "--objectExtension", help="Extension of the object")
            parser.add_argument("-ie", "--imageExtension", help="Extension of the texture")
            parser.add_argument("-pop", "--preprocessOutputPath", help="Preprocessed object output path")
            parser.add_argument("-mt", "--multitexture", help="Object has multitexture")
            parser.add_argument("-tp", "--texturePath", help="Path of the texture")

            self.args = parser.parse_args(self.argv)

class SingleTextureProcess():
    single_texture_object = None
    single_texture_name = None
    single_texture_object_extension = None
    single_texture_output_path = None
    single_texture_texture_path = None
    single_texture_scene = None
    single_texture_image_extension = None
    single_texture_root_path = None
    single_texture_clean_object = None

    def __init__(self, object, name, object_extension, output_path, texture_path, scene, image_extension, root_path):
        self.single_texture_object = object
        self.single_texture_name = name
        self.single_texture_object_extension = object_extension
        self.single_texture_output_path = output_path
        self.single_texture_texture_path = texture_path
        self.single_texture_scene = scene
        self.single_texture_image_extension = image_extension
        self.single_texture_root_path = root_path

        print("HEYYY SINGLE TEXTURE OBJECT IS " + str(self.single_texture_object))

        self.CleanGeometry()
        self.ProcessTextures()

        self.single_texture_clean_object = self.single_texture_object

    def CleanGeometry(self):
        # print("HEYY SINGLE TEXTURE CLEAN GEOMETRY OF OBJECT " + self.single_texture_object)
        object = self.single_texture_object
        Triangulate(object)


    def ProcessTextures(self):
        image_path = None
        destination_path = None

        if self.single_texture_object_extension != 'gltf' and self.single_texture_object_extension != 'glb':
            image_path = os.path.join(self.single_texture_root_path, self.single_texture_name + '_color' + "." + self.single_texture_image_extension)
            destination_path = os.path.join(self.single_texture_output_path, self.single_texture_name + '_color' + "." + self.single_texture_image_extension)
            origin_path = image_path
            # print('HEYYYYYY TEXTURE PATH IS ' + texture_path)
            # print('HEYYYYYY ORIGIN PATH IS ' + origin_path)
            # print('HEYYYYYY DESTINATION PATH IS ' + destination_path)
            shutil.copy(origin_path, destination_path)

        else:
            self.SaveTextures()


    def SaveTextures(self):
        material = self.single_texture_object.data.materials[0]
        material.use_nodes = True
        tree = material.node_tree
        nodes = tree.nodes
        links = tree.links
        Diffuse_node = nodes.get('Principled BSDF')
        image_name = None
        image = None

        if Diffuse_node is None:
            Diffuse_node = nodes.get('Diffuse BSDF')

        socket = Diffuse_node.inputs[0]

        link = next(link for link in links if link.to_node == Diffuse_node and link.to_socket == socket)

        image_node = link.from_node

        if image_node.type == 'TEX_IMAGE':
            image = image_node.image
            image_name = image.name

        image.filepath_raw = os.path.join(self.single_texture_output_path, self.single_texture_name + '_color' + '.png')
        image.file_format = 'PNG'
        image.save()

class ImportToScene():
    import_to_scene_rootpath = None
    import_to_scene_object_path = None
    import_to_scene_object_extension = None
    import_to_scene_object_name = None
    import_to_scene_scene = None
    import_to_scene_models = []
    import_to_scene_animation_data = None
    import_to_scene_is_animated = None


    def __init__(self, object_path, object_extension, object_name, scene, rootpath):
        self.import_to_scene_rootpath = rootpath
        self.import_to_scene_object_path = object_path
        self.import_to_scene_object_extension = object_extension
        self.import_to_scene_object_name = object_name
        self.import_to_scene_scene = scene
        self.import_to_scene_is_animated = None




        self.Import()
        self.CheckMultiScene()

        self.import_to_scene_animation_data = self.CheckAnimation()

        self.GetModel()


    def Import(self):
        candidate_object = self.import_to_scene_object_path

        if self.import_to_scene_object_extension == 'obj':
            bpy.ops.import_scene.obj(filepath=candidate_object)

        elif self.import_to_scene_object_extension == 'fbx':
            bpy.ops.import_scene.fbx(filepath=candidate_object)

        elif self.import_to_scene_object_extension == 'gltf' or self.import_to_scene_object_extension == 'glb':
            bpy.ops.import_scene.gltf(filepath=candidate_object)

        elif self.import_to_scene_object_extension == 'stl':
            bpy.ops.import_mesh.stl(filepath=candidate_object)

        elif self.import_to_scene_object_extension == 'ply':
            bpy.ops.import_scene.ply(filepath=candidate_object)

        elif self.import_to_scene_object_extension == '3ds':
            bpy.ops.import_scene.autodesk_3ds(filepath=candidate_object)

        elif self.import_to_scene_object_extension == 'dae':
            bpy.ops.wm.collada_import(filepath=candidate_object)




    def CheckMultiScene(self):
        self.list_scenes = bpy.data.scenes
        if len(self.list_scenes)>1:
            self.SetScene()

        else:
            pass

        self.import_to_scene_scene = bpy.context.scene
        bpy.context.scene.render.engine = 'CYCLES'
        # print (scene.name)

    def SetScene(self):
        list = self.list_scenes
        for i in range(len(list)):
            scene = list[i]
            for obj in self.import_to_scene_scene.objects:
                if obj.name != 'RootNode' and obj.type == 'MESH':
                    bpy.context.window.screen.scene = bpy.data.scenes[self.import_to_scene_scene.name]


    def CheckAnimation(self):
        scene = self.import_to_scene_scene

        for obj in scene.objects:
            if obj.type == 'ARMATURE':
                print('HEYYYYYY Thats an armature!')
                filepath = self.WriteThatFile(True)
                self.import_to_scene_is_animated = True
                return filepath



            else:
                print('HEYYYYY RAS')
                self.import_to_scene_is_animated = False





    def WriteThatFile(self, bool):
        animation_data_path = self.import_to_scene_rootpath

        filename = 'animated.txt'

        self.filepath = os.path.join(animation_data_path, filename)

        if self.filepath is not None:
            f = open(self.filepath, 'w+')

        else:
            f = open(self.filepath, 'x')


        f.close()

        return self.filepath



    def GetModel(self):
        # WE NEED TO SELECT ALL MESHES IF THEY ARE PLURAL
        all_objects = self.import_to_scene_scene.objects

        #We start by making a list of all the objects in the scene
        if len(all_objects) > 1:
            for object in self.import_to_scene_scene.objects:
                # print(object.name)
                if object.type == 'MESH' and 'RootNode' not in object.name:
                    bpy.data.objects[object.name].select = True
                    self.import_to_scene_models.append(bpy.data.objects[object.name])

            # CheckList(list_objects)


        else:
            for object in self.import_to_scene_scene.objects:
                if object.type == 'MESH' and 'RootNode' not in object.name:
                    self.import_to_scene_models.append(bpy.data.objects[object.name])
                    # Select and make object active
                    SelectActive(self.import_to_scene_models)



class MakeSingular():
    make_singular_objects = None
    make_singular_scene = None
    make_singular_object_name = None
    make_singular_object_list = []
    make_singular_single_object = None

    def __init__(self, objects, scene, object_name):
        self.make_singular_objects = objects
        self.make_singular_scene = scene
        self.make_singular_object_name = object_name



        self.make_singular_object_list = self.CheckParent()
        self.make_singular_single_object = self.CheckSeparate()

        # print("HEYYY MAKE SINGULAR " + str(self.make_singular_single_object))


    def CheckParent(self):
        objects_in_scene = []
        # print('OBJECTS' + str(objects))

        for i in range(len(self.make_singular_objects)):
            object= self.make_singular_objects[i]
            bpy.data.objects[object.name].select = True
            objects_in_scene.append(object.name)

            # Checking if parented
            if object.parent:
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                # matrixcopy = object.matrix_world.copy()
                # object.parent = None
                # object.matrix_world = matrixcopy

        return objects_in_scene


    def CheckSeparate(self):
        model = None
        list = self.make_singular_object_list
        if len(list) > 1:
            for i in range(len(list)):
                name = list[i]
                bpy.data.objects[name].select = True
                bpy.context.scene.objects.active = bpy.data.objects[name]

            bpy.ops.object.join()

            for object in self.make_singular_scene.objects:

                if object.type == 'MESH' and 'RootNode' not in object.name:
                    # print("HEYYYYY I AM HERE" + object.name)
                    bpy.data.objects[object.name].name = self.make_singular_object_name
                    model = bpy.data.objects[object.name]

        else:
            for object in self.make_singular_scene.objects:
                if object.type == 'MESH' and 'RootNode' not in object.name:
                    bpy.data.objects[object.name].name = self.make_singular_object_name

                    model = bpy.data.objects[object.name]

        # We need to rename the joined object with the object name, because it might take another name during the join process
        model.name = self.make_singular_object_name



        return model

class MultiTextureProcess():
    multi_texture_process_highpoly = None
    multi_texture_process_object_name = None
    multi_texture_process_object_extension = None
    multi_texture_process_texture_path = None
    multi_texture_process_output_path = None
    multi_texture_process_bake_resolution = None
    multi_texture_process_scene = None
    texture_list = []
    lowpoly = None


    def __init__(self, highpoly, object_name, object_extension, texture_path, output_path, bake_resolution, scene):
        self.multi_texture_process_highpoly = highpoly
        self.multi_texture_process_object_name = object_name
        self.multi_texture_process_object_extension = object_extension
        self.multi_texture_process_texture_path = texture_path
        self.multi_texture_process_output_path = output_path
        self.multi_texture_process_bake_resolution = bake_resolution
        self.multi_texture_process_scene = scene

        if self.multi_texture_process_object_extension != 'gltf' and self.multi_texture_process_object_extension != 'glb':
            self.texture_list = self.Construct()
            self.ApplyTextures()

        # CREATE BAKED OBJECT

        self.lowpoly = self.CreateLowPoly()

        # CLEAN MATERIALS OF BAKED OBJECT
        self.CleanMaterials()

        # CLEAN GEOMETRY
        self.CleanGeometry()

        # UNWRAP
        self.Unwrap()

        # CREATE IMAGE WHICH WILL RECEIVE THE BAKE
        self.baked_color = self.CreateImage()

        # CREATE MATERIAL FOR THE LOW POLY
        self.CreateMaterial()

        # CREATE THE BAKING CAGE
        self.cage = self.CreateCage()

        # CONFIGURE THE BAKING CAGE
        # This value should not be over 0.03
        self.ratio = 0.010
        self.cage = self.ConfigureCage()

        # BAKE
        self.Bake()

        self.clean_object = self.lowpoly




    def Construct(self):
        fileList = []
        textureList = []

        for file in os.listdir(self.multi_texture_process_texture_path):
            fileList.append(file)

        # CheckList(fileList)

        for file in fileList:
            if 'color' in file or 'Color' in file:
                if 'jpeg' in file or 'jpg' in file or 'png' in file:
                    textureList.append(file)

        # CheckList(textureList)

        return textureList

    def ApplyTextures(self):
        model = self.multi_texture_process_highpoly
        list = self.texture_list
        loaded_diffuse = None
        material_names_list = []
        Length = len(list)

        for i in range(Length):
            material_names_list.append(model.data.materials[i].name)

        # The materials might not be in the right order. We need to sort them.
        sorted_material_names_list = sorted(material_names_list)

        # Now we assume here that the materials have the same name as the texture. We will initiate a loop which will apply the right texture to the right material by refering to 'i', the name of both material and texture.

        Length = len(sorted_material_names_list)
        for i in range(Length):
            # GET MATERIAL AND NODES
            name = sorted_material_names_list[i]
            material = bpy.data.materials[name]
            material.use_nodes = True

            # SORT TREE NODES
            tree = bpy.data.materials[name].node_tree
            nodes = tree.nodes
            links = tree.links

            # CLEAR ALL SHADER NODES
            for node in nodes:
                if node.type != 'OUTPUT_MATERIAL':
                    nodes.remove(node)

            # CREATE NEW NODES AND LINK THEM
            image_node = tree.nodes.new('ShaderNodeTexImage')
            BSDF_node = nodes.new('ShaderNodeBsdfPrincipled')
            Output_node = nodes.get('Material Output')

            links.new(image_node.outputs[0], BSDF_node.inputs[0])
            links.new(BSDF_node.outputs[0], Output_node.inputs[0])

            # LOAD TEXTURE
            # We match the index of the sorted material list to the index of texture list we constructed earlier.
            loaded_diffuse = bpy.data.images.load(os.path.join(self.multi_texture_process_texture_path, list[i]))
            image_node.image = loaded_diffuse

    def CreateLowPoly(self):
        highpoly = self.multi_texture_process_highpoly
        SelectActive(highpoly)
        # We have to use the duplicate function and not copy, because if we copy, the lowpoly will be linked to the highpoly and not independent.
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        lowpoly = None
        for object in self.multi_texture_process_scene.objects:
            if object.type == 'MESH' and object.name != 'RootNode' and object.name != highpoly.name:
                lowpoly = bpy.data.objects[object.name]

        SelectActive(lowpoly)

        return lowpoly

    def CleanMaterials(self):
        object = self.lowpoly
        for mat in object.data.materials:
            bpy.context.object.active_material_index = 0
            bpy.ops.object.material_slot_remove()

    def CleanGeometry(self):
        object = self.lowpoly
        Triangulate(object)
        # No need to remove doubles, it is done in the bakemyscan script (invalid clnors message), but it works with this function if needed.
        # RemoveDoubles(object)


    def Unwrap(self):
        object = self.lowpoly
        print('----------------------------------------------------------------------------------------------')
        print('BE PATIENT, WE ARE UNWRAPPING YOUR MODEL, IT MIGHT TAKE SOME TIME!')
        print('Time for a cat video!')
        print('----------------------------------------------------------------------------------------------')
        SelectActive(object)
        bpy.ops.uv.smart_project()

    def CreateImage(self):
        bpy.ops.image.new(name=os.path.join(self.multi_texture_process_highpoly.name + '_' + 'color'), width=self.multi_texture_process_bake_resolution,
                          height=self.multi_texture_process_bake_resolution)
        image = bpy.data.images[os.path.join(self.multi_texture_process_highpoly.name + '_' + 'color')]

        return image

    def CreateMaterial(self):
        lowpoly = self.lowpoly
        highpoly = self.multi_texture_process_highpoly
        baked_color = self.baked_color
        SelectActive(lowpoly)
        mat = bpy.data.materials.new(highpoly.name)
        mat.use_nodes = True

        tree = mat.node_tree
        nodes = tree.nodes
        links = tree.links

        # Storing the variables of the tree node for them to be more accessible
        tree = mat.node_tree
        nodes = tree.nodes
        links = tree.links

        # Creating the nodes I want
        BSDF_node = nodes.new('ShaderNodeBsdfPrincipled')
        Output_node = nodes.get('Material Output')
        image_node = nodes.get('Diffuse BSDF')

        # Removing the default diffuse bsdf
        diffnodes = mat.node_tree.nodes
        node = nodes['Diffuse BSDF']
        nodes.remove(node)

        # Making the link between Principled Shader and Output
        links.new(BSDF_node.outputs[0], Output_node.inputs[0])

        # Attaching the image
        diff_texture_node = nodes.new('ShaderNodeTexImage')
        diff_texture_node.image = baked_color
        links.new(diff_texture_node.outputs[0], BSDF_node.inputs[0])

        # Applying the material to the object
        lowpoly.data.materials.append(mat)

    def CreateCage(self):
        lowpoly = self.lowpoly
        highpoly = self.multi_texture_process_highpoly
        scene = self.multi_texture_process_scene

        SelectActive(lowpoly)
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        cage = None

        for ob in scene.objects:
            if ob.type == 'MESH' and ob.name != lowpoly.name and ob.name != highpoly.name and ob.name != "RootNode":
                cage = bpy.data.objects[ob.name]

        bpy.data.objects[cage.name].select = True
        bpy.context.scene.objects.active = bpy.data.objects[cage.name]

        return cage

    def ConfigureCage(self):
        cage = self.cage
        scene = self.multi_texture_process_scene
        ratio = self.ratio
        SelectActive(cage)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.shrink_fatten(value=ratio, use_even_offset=False, mirror=False, proportional='DISABLED',
                                        proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.editmode_toggle()
        return cage

    def Bake(self):
        highpoly = self.multi_texture_process_highpoly
        lowpoly = self.lowpoly
        output_path = self.multi_texture_process_output_path
        baked_color = self.baked_color
        cage = self.cage
        image = baked_color
        filepath = output_path
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[highpoly.name].select = True
        bpy.data.objects[lowpoly.name].select = True
        bpy.context.scene.objects.active = lowpoly

        print('----------------------------------------------------------------------------------------------')
        print('BE PATIENT, WE ARE BAKING YOUR MODEL, IT MIGHT TAKE SOME TIME!')
        print('Time for another cat video!')
        print('----------------------------------------------------------------------------------------------')
        bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, filepath=filepath, use_selected_to_active=True,
                            use_cage=True, cage_object=cage.name)

        image.filepath_raw = os.path.join(output_path, baked_color.name + '.png')
        image.file_format = 'PNG'
        image.save()

def Unparent(objects):
    object_list = objects

    for i in object_list:
        object = bpy.data.objects[i.name]
        if object.parent:
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')


def CheckArgs():
    print('HEYYYYYYYYYYYYYYYYYYYYYYYYYY')
    print('root_path is ' + sys.argv[4])
    print('object_path is ' + sys.argv[5])
    print('object_name is ' + sys.argv[6])
    print('object extension is ' + sys.argv[7])
    print('image_extension is ' + sys.argv[8])
    print('output_path is ' + sys.argv[9])
    print('multitexture is ' + sys.argv[10])
    print('texture_path is ' + sys.argv[11])

def SelectActive(object):

    bpy.ops.object.select_all( action='DESELECT' )


    if type(object) == list:
        for i in object:

            bpy.data.objects[i.name].select = True
            bpy.context.scene.objects.active = bpy.data.objects[i.name]

    else :
        bpy.data.objects[object.name].select = True
        bpy.context.scene.objects.active = bpy.data.objects[object.name]


def Triangulate(model):
    object = model

    if type(object) == list:
        for ob in object:
            print(bpy.data.objects[ob.name])
            # object_data = ob.data
            # bm = bmesh.new()
            # bm.from_mesh(object_data)
            # bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
            # bm.to_mesh(object_data)
            # bm.free()

    else:
        object_data = object.data
        print(bpy.data.objects[object.name])
        # bm = bmesh.new()
        # bm.from_mesh(object_data)
        # bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
        # bm.to_mesh(object_data)
        # bm.free()


def CheckObj(scene):
    for object in scene.objects:
        print(object.name)

def CheckList(list):
    for i in list:
        print( 'FIIIIIIIIIILELIST IS ' + str(i))

def Place(object):
    SelectActive(object)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    area = None
    space = None

    # I have to snap the object to the 3D cursor, but for that I have to bypass the context stuff
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            break

    for space in area.spaces:
        if space.type == 'VIEW_3D':
            break

    object.location = space.cursor_location

    # Freeze all transforms
    bpy.ops.object.transform_apply( location=True, rotation=True, scale=True )

def GetMaterialAmount(object):
    materialList = []

    for mat in object.data.materials:
        materialList.append(mat)

    if len(materialList) > 1:
        return True

    else:
        return False

    # print ('HEYYYYYYYYYYY ' + str( has_multi_texture ))

def RemoveDoubles(object):
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()


def Export(object, name, path):

    SelectActive(object)
    export_filepath = os.path.join(path, name + '_clean' + '.obj')
    bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)

    print('----------------------------------------------------------------------------------------------')
    print('YOUR MODEL IS CLEANED, NOW WE ARE GOING TO DECIMATE IT FOR YOU :)')
    print('----------------------------------------------------------------------------------------------')


def Run():
    # INITIALIZING THE SCENE
    scene = bpy.context.scene
    bpy.context.scene.render.engine = 'CYCLES'

    # GETTING THE VARIABLES SENT BY BATCH
    args = DefineArguments()



    # DECLARING PYTHON VARIABLES
    # Change this resolution for a higher value if you have a better computer. But the higher the longer the object will be to process.
    bake_resolution = 2048
    has_multi_texture = None
    models = []

    # CHECK THE ARGUMENT LIST
    # Debug purposes, keep this commented otherwise
    # CheckArgs()

    # IMPORT THE OBJECT
    # Use extend here to add each argument of the list to the models list as an individual. If you use append and append a list to a list, the appeneded list will be appended as an object but with all the values together, not separated.
    import_process = ImportToScene(args.object_path, args.object_extension, args.object_name, scene, args.root_path)
    scene = import_process.import_to_scene_scene
    models = import_process.import_to_scene_models

    print("HEYYYYYY PATH IS " + str(import_process.import_to_scene_animation_data))

    if os.path.exists(import_process.import_to_scene_animation_data):
        isAnimated = True

    else :
        isAnimated = False

    # Unparent(models)
    single_model_process = MakeSingular(models, scene, args.object_name)
    single_model = single_model_process.make_singular_single_object
    single_model.name = single_model_process.make_singular_object_name


    print("HEY RUN MAIN " + str(single_model))

    # DEBUG OPTIONS TO CHECK THE MODELS AND SCENE
    # CheckList(models)
    # CheckObj(scene)


    if isAnimated == False:


        # PLACE THE OBJECT AT THE CENTER AND FREEZE TRANSFORM
        Place(single_model)


# Ok this may seem weird, but it's just in case we must not merge and unparent the objects of the scene for the future
    models = single_model


    # CHECK WHETHER THE OBJECT HAS MULTITEXTURES OR NOT
    if args.multitexture == 'Yes':
        has_multi_texture = True


    elif args.multitexture == 'No':
        has_multi_texture = False


        if args.object_extension == 'gltf' or args.object_extension == 'glb':
            # In the case of a gltf or glb object, we can't separate the textures in the color folder. The only way to check whether the object has several textures then is to analyze its materials.
            has_multi_texture = GetMaterialAmount(models)



    # PROCEEED ACCORDING TO PREVIOUS RESULT
    if has_multi_texture:
        multi_texture_process = MultiTextureProcess(models, args.object_name, args.object_extension, args.texture_path, args.output_path, bake_resolution, scene)
        clean_object = multi_texture_process.clean_object

    else:
        single_texture_process = SingleTextureProcess(models, args.object_name, args.object_extension, args.output_path, args.texture_path, scene, args.image_extension, args.root_path)
        clean_object = single_texture_process.single_texture_clean_object


    Export(clean_object, args.object_name, args.output_path)

Run()