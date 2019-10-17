import bpy
import sys
import os
import bmesh
from os import listdir

def Run():
    scene = bpy.context.scene
    bpy.context.scene.render.engine = "CYCLES"


    texture_path = sys.argv[4]
    output_path = sys.argv[5]
    obj_name = sys.argv[6]
    object_extension = sys.argv[7]
    object_path = sys.argv[8]
    bake_resolution = 2048

    # CheckArgs()
    textureList = Construct(obj_name, texture_path, output_path)

    # I have to import the object, but to use it in other functions I choose to store it in a variable. The import function must return an object.

    highpoly = Import(obj_name, object_extension, object_path, scene)

    Place(highpoly)

    ApplyTextures(texture_path, textureList, highpoly)

    lowpoly = CreateLowPoly(scene, highpoly)


    #USe the following lines if you need to make the object active for next steps.
    # bpy.ops.object.select_all(action='DESELECT')
    # bpy.data.objects[lowpoly.name].select = True
    # bpy.context.scene.objects.active = bpy.data.objects[lowpoly.name]


    CleanMaterials(lowpoly)

    Unwrap(lowpoly)

    baked_color = CreateImage(highpoly, bake_resolution)

    CreateMaterial(lowpoly, highpoly, baked_color)

    Bake(highpoly, lowpoly, output_path, baked_color)

    Export(lowpoly, output_path, obj_name)

def CheckArgs():
    print("HEYYYYYYYYYYYYYYYYYYYYYYYYYY")
    print( "argument 9 is " + sys.argv[8])
    print( "argument 8 is " + sys.argv[7])
    print("argument 7 is " + sys.argv[6])
    print("argument 6 is " + sys.argv[5])
    print("argument 5 is " + sys.argv[4])

def CheckList(list):
    for i in list:
        print( "FIIIIIIIIIILELIST IS " + i )

def Construct(obj_name, texture_path, output_path):
    fileList = []
    textureList = []

    for file in os.listdir(texture_path):
        fileList.append(file)

    # CheckList(fileList)

    for file in fileList:
        if "color" in file or "Color" in file:
            if "jpeg" in file or "jpg" in file or "png" in file:
                textureList.append(file)


    # CheckList(textureList)

    return textureList

def Import(name, obj_extension, path, scene):
    candidate_object = path
    myobject = None

    if obj_extension == "obj":
        bpy.ops.import_scene.obj( filepath=candidate_object )

    elif obj_extension == "fbx":
        bpy.ops.import_scene.fbx( filepath=candidate_object )

    elif obj_extension == "gltf" or obj_extension == "glb":
        bpy.ops.import_scene.gltf( filepath=candidate_object )

    elif obj_extension == "stl":
        bpy.ops.import_mesh.stl( filepath=candidate_object )

    elif obj_extension == "ply":
        bpy.ops.import_scene.ply( filepath=candidate_object )

    elif obj_extension == "3ds":
        bpy.ops.import_scene.autodesk_3ds( filepath=candidate_object )

    elif obj_extension == "dae":
        bpy.ops.wm.collada_import( filepath=candidate_object )


    for object in scene.objects:
        # développer cette partie plus tard dans le script de pre processing pour virer les nodes, par contre faudra sûrement join l'objet à l'issue de ce script ci.
        #Plus tard il faudra peut-être prévoir de gérer un cas où l'objet est en plusieurs parties
        if object.type == "MESH" and object.name != "RootNode":
            myobject = bpy.data.objects[object.name]

    #Object selected and active
    bpy.data.objects[myobject.name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[myobject.name]

    return myobject

def Place(object):
    # print("HEYYYYYYYYY OBJECT " + object.name)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    area = None
    space = None

    # I have to snap the object to the 3D cursor, but for that I have to bypass the context stuff
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            break

    for space in area.spaces:
        if space.type == "VIEW_3D":
            break

    object.location = space.cursor_location

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def ApplyTextures(texture_path, textureList, highpoly):
    loaded_diffuse = None
    materialNamesList = []
    Length = len(textureList)
    for i in range (Length):
        #Aaaand there's a problem there. The materials are not listed in the right order.
        # print ("HEYYY MATERIALS ARE " + highpoly.data.materials[i].name)
        materialNamesList.append(highpoly.data.materials[i].name)

    sorted_materialNamesList = sorted(materialNamesList)

    #Check that the materials were correctly sorted
    # Length = len(sorted_materialNamesList)
    # for i in range (Length):
    #     name = sorted_materialNamesList[i]
    #     print(name)

    Length = len(sorted_materialNamesList)
    for i in range (Length):
        #Get Material and Nodes
        name = sorted_materialNamesList[i]
        material = bpy.data.materials[name]
        material.use_nodes = True

        tree = bpy.data.materials[name].node_tree
        nodes = tree.nodes
        links = tree.links

        #Clear all nodes
        for node in nodes:
            if node.type != "OUTPUT_MATERIAL":
                nodes.remove(node)

        #Create new nodes and link them
        image_node = tree.nodes.new("ShaderNodeTexImage")
        BSDFNode = nodes.new ("ShaderNodeBsdfPrincipled")
        OutputNode = nodes.get("Material Output")

        links.new(image_node.outputs[0], BSDFNode.inputs[0])
        links.new(BSDFNode.outputs[0], OutputNode.inputs[0])


        #Load texture
        loaded_diffuse = bpy.data.images.load(os.path.join(texture_path, textureList[i]))
        image_node.image = loaded_diffuse


def CreateLowPoly(scene, highpoly):

    #We have to use the duplicate function and not copy, because if we copy, the lowpoly will be linked to the highpoly and not independent.
    bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
    lowpoly = None

    # I don't know how to get the duplicated object so I'll just run through the scene again and find it. But this method implies there are no other meshes in the scene and that the highpoly is one single object...
    # When we have more objects for the high poly, we should do a list listing all the high poly objects, then check whether the new object's name is within that list. If not, then it is our duplicate
    for object in scene.objects:
        if object.type == "MESH" and object.name != "RootNode" and object.name != highpoly.name:
            lowpoly = bpy.data.objects[object.name]

    # print( "HEYYYYYYYYYYYYY " + lowpoly.name)

    return lowpoly


def CleanMaterials(lowpoly):
    for mat in lowpoly.data.materials:
        bpy.context.object.active_material_index = 0
        bpy.ops.object.material_slot_remove()


def Unwrap(lowpoly):
    bpy.context.scene.objects.active = lowpoly
    bpy.ops.uv.smart_project()

def CreateImage(highpoly, bake_resolution):

    bpy.ops.image.new(name=os.path.join(highpoly.name + "_" + "color"), width=bake_resolution, height=bake_resolution)
    image = bpy.data.images[os.path.join(highpoly.name + "_" + "color")]

    return image

def CreateMaterial(lowpoly, highpoly, baked_color):
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
    BSDF = nodes.new( "ShaderNodeBsdfPrincipled" )
    Output = nodes.get( "Material Output" )
    Diffuse = nodes.get( "Diffuse BSDF" )

    # Removing the default diffuse bsdf
    diffnodes = mat.node_tree.nodes
    node = nodes["Diffuse BSDF"]
    nodes.remove( node )

    # Making the link between Principled Shader and Output
    links.new( BSDF.outputs[0], Output.inputs[0] )

    # Attaching the image
    diff_texture_node = nodes.new("ShaderNodeTexImage")
    diff_texture_node.image = baked_color
    links.new(diff_texture_node.outputs[0], BSDF.inputs[0])

    # Applying the material to the object
    lowpoly.data.materials.append(mat)


def Bake(highpoly, lowpoly, output_path, baked_color):
    image = baked_color
    filepath = output_path
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.data.objects[highpoly.name].select = True
    bpy.data.objects[lowpoly.name].select = True
    bpy.context.scene.objects.active = lowpoly

    bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, filepath = filepath, use_selected_to_active=True, cage_extrusion = 0.3)

    image.filepath_raw = os.path.join(output_path, baked_color.name + ".png")
    image.file_format = "PNG"
    image.save()


def Export(lowpoly, output_path, obj_name):
    bpy.ops.object.select_all( action='DESELECT' )
    bpy.data.objects[lowpoly.name].select = True
    bpy.context.scene.objects.active = lowpoly
    export_filepath = os.path.join(output_path, obj_name + "_multiprocessed" + ".obj" )
    bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)





Run()