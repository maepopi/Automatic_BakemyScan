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
    root_path = sys.argv[5]
    object_path = sys.argv[6]
    object_name = sys.argv[7]
    object_extension = sys.argv[8]
    image_extension = sys.argv[9]
    output_path = sys.argv[10]
    multitexture = sys.argv[11]
    texture_path = sys.argv[12]

    # DECLARING PYTHON VARIABLES
    # Change this resolution for a higher value if you have a better computer. But the higher the longer the object will be to process.
    bake_resolution = 2048
    has_multi_texture = None
    clean_object = None

    # CHECK THE ARGUMENT LIST
    # Debug purposes, keep this commented otherwise
    # CheckArgs()


    # IMPORT THE OBJECT
    model = Import(object_path, object_extension, object_name, scene)

    # CheckObj(scene)

    # MAKE SURE THE OBJECT IS JOINED AND INDEPENDENT IN THE SCENE
    model = MakeSingular(model, scene, object_name)

    # PLACE THE OBJECT AT THE CENTER AND FREEZE TRANSFORM
    Place(model)

    # CHECK WHETHER THE OBJECT HAS MULTITEXTURES OR NOT
    if multitexture == 'Yes':
        has_multi_texture = True


    elif multitexture == 'No':
        has_multi_texture = False


        if object_extension == 'gltf' or object_extension == 'glb':
            # In the case of a gltf or glb object, we can't separate the textures in the color folder. The only way to check whether the object has several textures then is to analyze its materials.
            has_multi_texture = GetMaterialAmount(model)

    # print('COUCOUUUUUUUUU ' + str(has_multi_texture))

    # PROCEEED ACCORDING TO PREVIOUS RESULT
    if has_multi_texture:
        clean_object = MultiTextureProcess(model, object_name, object_extension, texture_path, output_path, scene, bake_resolution)

    else:
        # print("HEYYYY NO BAKING")
        clean_object = SingleTextureProcess(model, object_name, object_extension, output_path, texture_path, scene, image_extension, root_path)


    Export(clean_object, object_name, output_path)

def SingleTextureProcess(object, name, object_extension, output_path, texture_path, scene, image_extension, root_path):
    CleanGeometry(object)
    SaveTextures(object, name, object_extension, output_path, texture_path, scene, image_extension, root_path)
    clean_object = object

    return clean_object

def SaveTextures(object, name, object_extension, output_path, texture_path, scene, image_extension, root_path):
    image_path = None
    destination_path = None

    if object_extension != 'gltf' and object_extension != 'glb':
        if image_extension == 'jpg':
            image_path = os.path.join(root_path, name + '_color' + '.jpg')
            destination_path = os.path.join(output_path, name + '_color' + '.jpg')

        elif image_extension == 'jpeg':
            image_path = os.path.join(root_path, name + '_color' + '.jpeg')
            destination_path = os.path.join( output_path, name + '_color' + '.jpeg')

        elif image_extension == 'png':
            image_path = os.path.join(root_path, name + '_color' + '.png')
            destination_path = os.path.join(output_path, name + '_color' + '.png')

        origin_path = image_path
        # print('HEYYYYYY TEXTURE PATH IS ' + texture_path)
        # print('HEYYYYYY ORIGIN PATH IS ' + origin_path)
        # print('HEYYYYYY DESTINATION PATH IS ' + destination_path)
        shutil.copy(origin_path, destination_path)

    else:
        material = object.data.materials[0]
        material.use_nodes = True
        tree = material.node_tree
        nodes = tree.nodes
        links = tree.links

        Diffuse_node = nodes.get('Principled BSDF')
        image_name = None

        if Diffuse_node is None:
            Diffuse_node = nodes.get('Diffuse BSDF')

        socket = Diffuse_node.inputs[0]

        link = next(link for link in links if link.to_node == Diffuse_node and link.to_socket == socket)

        image_node = link.from_node

        if image_node.type == 'TEX_IMAGE':
            image = image_node.image
            image_name = image.name


        image.filepath_raw = os.path.join(output_path, name + '_color' + '.png')
        image.file_format = 'PNG'
        image.save()

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
    SelectActive(model)


    return model

def SelectActive(object):
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.data.objects[object.name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[object.name]

def CheckObj(scene):
    for object in scene.objects:
        print(object.name)

def CheckList(list):
    for i in list:
        print( 'FIIIIIIIIIILELIST IS ' + str(i))


def MakeSingular(object, scene, object_name):
    object_list = CheckParent(object, scene)
    object = CheckSeparate(object, object_list, scene, object_name)

    return object

def CheckParent(object, scene):
    objects_in_scene = []

    for object in scene.objects:
        if object.type == 'MESH' and object.name != 'RootNode':
            bpy.data.objects[object.name].select = True
            objects_in_scene.append(object)

            #Checking if parented
            if object.parent:
                matrixcopy = object.matrix_world.copy()
                object.parent = None
                object.matrix_world = matrixcopy

    return objects_in_scene

def CheckSeparate(object, list, scene, name):
    if len(list) > 1:
        for object in list:
            bpy.data.objects[object.name].select = True
            bpy.context.scene.objects.active = bpy.data.objects[object.name]

        bpy.ops.object.join()

    bpy.data.objects[object.name].name = name

    model = bpy.data.objects[object.name]

    return model

    # print('OBJECT NAME ISSSSS ' + bpy.data.objects[object.name].name)

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

def MultiTextureProcess(highpoly, name, object_extension, texture_path, output_path, scene, bake_resolution):
    # If the object is not a gltf and not a glb, we'll need to replug the textures
    if object_extension != 'gltf' and object_extension != 'glb':
        # print ('HEYYYYYY IM FUCKED ' + object_extension)
        texture_list = Construct(name, texture_path, output_path)
        ApplyTextures(highpoly, texture_list, texture_path)

    # CREATE BAKED OBJECT
    lowpoly = CreateLowPoly(scene, highpoly)

    # CLEAN MATERIALS OF BAKED OBJECT
    CleanMaterials(lowpoly)

    # CLEAN GEOMETRY OF BAKED OBJECT
    CleanGeometry(lowpoly)

    # UNWRAP
    Unwrap(lowpoly)

    # CREATE IMAGE WHICH WILL RECEIVE THE BAKE
    baked_color = CreateImage(highpoly, bake_resolution)

    # CREATE MATERIAL FOR THE LOW POLY
    CreateMaterial(lowpoly, highpoly, baked_color)

    # BAKE
    Bake(highpoly, lowpoly, output_path, baked_color)

    clean_object = lowpoly

    return clean_object

def Construct(name, texture_path, output_path):
    fileList = []
    textureList = []

    for file in os.listdir( texture_path ):
        fileList.append( file )

    # CheckList(fileList)

    for file in fileList:
        if 'color' in file or 'Color' in file:
            if 'jpeg' in file or 'jpg' in file or 'png' in file:
                textureList.append( file )

    # CheckList(textureList)

    return textureList

def ApplyTextures(model, list, texture_path):
    loaded_diffuse = None
    material_names_list = []
    Length = len(list)

    for i in range(Length):
        material_names_list.append(model.data.materials[i].name)

    # The materials might not be in the right order. We need to sort them.
    sorted_material_names_list = sorted(material_names_list)

    # Now we assume here that the materials have the same name as the texture. We will initiate a loop which will apply the right texture to the right material by refering to 'i', the name of both material and texture.

    Length = len(sorted_material_names_list)
    for i in range (Length):
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

        #LOAD TEXTURE
        # We match the index of the sorted material list to the index of texture list we constructed earlier.
        loaded_diffuse = bpy.data.images.load(os.path.join(texture_path, list[i]))
        image_node.image = loaded_diffuse


def CreateLowPoly(scene, highpoly):
    SelectActive(highpoly)
    # We have to use the duplicate function and not copy, because if we copy, the lowpoly will be linked to the highpoly and not independent.
    bpy.ops.object.duplicate( linked=False, mode='TRANSLATION' )
    lowpoly = None
    for object in scene.objects:
        if object.type == 'MESH' and object.name != 'RootNode' and object.name != highpoly.name:
            lowpoly = bpy.data.objects[object.name]

    # print( 'HEYYYYYYYYYYYYY ' + lowpoly.name)

    SelectActive(lowpoly)

    return lowpoly

def CleanMaterials(object):
    for mat in object.data.materials:
        bpy.context.object.active_material_index = 0
        bpy.ops.object.material_slot_remove()


def CleanGeometry(object):
    # SelectActive(object)
    Triangulate(object)
    # No need to remove doubles, it is done in the bakemyscan script, but it works with this function if needed.
    # RemoveDoubles(object)


def Triangulate(object):
    object_data = object.data
    bm = bmesh.new()
    bm.from_mesh(object_data)
    bmesh.ops.triangulate( bm, faces=bm.faces[:], quad_method=0, ngon_method=0 )
    bm.to_mesh(object_data)
    bm.free()


def RemoveDoubles(object):
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()


def Unwrap(object):
    SelectActive(object)
    bpy.ops.uv.smart_project()

def CreateImage(highpoly, bake_resolution):
    bpy.ops.image.new( name=os.path.join( highpoly.name + '_' + 'color'), width=bake_resolution, height=bake_resolution )
    image = bpy.data.images[os.path.join( highpoly.name + '_' + 'color')]

    return image

def CreateMaterial(lowpoly, highpoly, baked_color):
    SelectActive(lowpoly)
    mat = bpy.data.materials.new( highpoly.name )
    mat.use_nodes = True

    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Storing the variables of the tree node for them to be more accessible
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Creating the nodes I want
    BSDF_node = nodes.new( 'ShaderNodeBsdfPrincipled' )
    Output_node = nodes.get( 'Material Output' )
    image_node = nodes.get( 'Diffuse BSDF' )

    # Removing the default diffuse bsdf
    diffnodes = mat.node_tree.nodes
    node = nodes['Diffuse BSDF']
    nodes.remove(node)

    # Making the link between Principled Shader and Output
    links.new( BSDF_node.outputs[0], Output_node.inputs[0] )

    # Attaching the image
    diff_texture_node = nodes.new( 'ShaderNodeTexImage')
    diff_texture_node.image = baked_color
    links.new( diff_texture_node.outputs[0], BSDF_node.inputs[0] )

    # Applying the material to the object
    lowpoly.data.materials.append(mat)


def Bake(highpoly, lowpoly, output_path, baked_color):
    image = baked_color
    filepath = output_path
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.data.objects[highpoly.name].select = True
    bpy.data.objects[lowpoly.name].select = True
    bpy.context.scene.objects.active = lowpoly

    bpy.ops.object.bake( type='DIFFUSE', pass_filter={'COLOR'}, filepath=filepath, use_selected_to_active=True, cage_extrusion=0.3)

    image.filepath_raw = os.path.join(output_path, baked_color.name + '.png' )
    image.file_format = 'PNG'
    image.save()

def Export(object, name, path):
    SelectActive(object)
    export_filepath = os.path.join(path, name + '_clean' + '.obj')
    bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)



Run()