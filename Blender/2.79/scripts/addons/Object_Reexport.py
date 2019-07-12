
import bpy
import os
import math
import shutil
import glob
import sys
import argparse

#Passage en Cycles
bpy.context.scene.render.engine = 'CYCLES'



#Defining a function that searches the file. If the file exists, then the function returns it. If not, then the function comes empty.
def find_image_file(folderpath, itemname, suffix, tails):
    for tail in tails:
        candidate_path = os.path.join(folderpath, itemname + suffix + tail)
        print('testing: ' + candidate_path)
        if os.path.isfile(candidate_path):
            print('found')
            return candidate_path
    return None


def run():

    # put the location to the folder where the objs are located here in this fashion
    # this line will only work on windows ie C:\objects
    #Attention bien penser à changer l'index de l'argument selon sa place dans la ligne de commande
    rootfolder= os.path.join(sys.argv[5])

    
    print(rootfolder)
     
    

    # get list of all files in directory
    #folder_list = sorted(os.listdir(filepath)) ==> Pourquoi on a enlevé ça?

    obj_list=[]
   

    #-----------------------------------------
    #
    #     OBJECTS AND TEXTURES TO BE IMPORTED
    #
    #-------------------------------------------



    obj_list.append(rootfolder)

    print(obj_list)


            

    #--------------------------
    #
    #     IMPORT
    #
    #--------------------------


    for item_path in obj_list:
        #path de l'objet à importer
        candidate_object= item_path 
        #j'importe l'objet
        bpy.ops.import_scene.obj(filepath = candidate_object)
        
    
    print(item_path)

    #--------------------------
    #
    #     SELECTION
    #
    #--------------------------

        #je selectionne l'objet importé
        #je passemat. par toute la scène pour ne selectionner qu'un seul objet

    ma_scene = bpy.context.scene
    for un_objet in ma_scene.objects:
        if un_objet.type == 'MESH':
        #je dit à chaque objet mesh que je rencontre (donc normalement un seul) d'être actif
        	bpy.context.scene.objects.active = un_objet

        #je fous dans une variable ce qui doit normalementetre mon seul objet actif
    curr_object = bpy.context.active_object

    #--------------------------
    #
    #     MATERIAL
    #
    #--------------------------

        #Creation of the material we want on the object
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
    links.new( BSDF.outputs[0], Output.inputs[0] )

    # Applying the material to the object
    curr_object.data.materials[0] = mat

      

    # #--------------------------
    # #
    # #     IMPORT TEXTURES
    # #
    # #--------------------------
    

    diffuse_path=sys.argv[6]
    normal_path=sys.argv[7]

        # # On récupère le dossier de l'objet importé
    # itemfolderpath= os.path.dirname(item_path)
        
        
    # #tem name (without extension)
    # itemname = os.path.splitext(os.path.basename(item_path))[0]
        
    # image_resolutions = [2048, 1024, 512]
    # image_extensions = ['.png','.jpg','.jpeg']
    # image_tails = ['_' + str(resolution) + extension for resolution in image_resolutions for extension in image_extensions]
        
    # item_suffix_index = itemname.find("_Mesh")
    # image_base_name = itemname[0:item_suffix_index] if item_suffix_index >= 0 else itemname
        
    # diffuse_path = find_image_file(itemfolderpath,image_base_name, '_diffuse', image_tails)
    # normal_path = find_image_file(itemfolderpath,image_base_name, '_normal', image_tails)
    # ORM_path = find_image_file(itemfolderpath,image_base_name, '_ORM', image_tails)

    # if diffuse_path is not None:
        # print("diffuse path is" + diffuse_path)
        # print("itemfolderpath is" + itemfolderpath)
        # print("item_path is" + item_path)

       
# #        #--------------------------
# #        #
# #        #     LINK TEXTURES
# #        #
# #        #--------------------------

        #On charge les images dans Blender et on les met dans des nodes qu'on connecte au shader
    loaded_diffuse = bpy.data.images.load(diffuse_path)
    diff_texture_node = nodes.new("ShaderNodeTexImage")
    diff_texture_node.image = loaded_diffuse

        #On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
    Diffuse_fullname=loaded_diffuse.name
    Diffuse_splitname=os.path.splitext(Diffuse_fullname)
    loaded_diffuse.name=Diffuse_splitname[0]


    link_diffuse=links.new(diff_texture_node.outputs[0], BSDF.inputs[0])

    if normal_path is not None:
        loaded_normal = bpy.data.images.load(normal_path)
        norm_texture_node = nodes.new("ShaderNodeTexImage")
        norm_texture_node.image = loaded_normal
        norm_texture_node.color_space='NONE'
            
            #On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
        Normal_fullname=loaded_normal.name
        Normal_splitname=os.path.splitext(Normal_fullname)
        loaded_normal.name=Normal_splitname[0]
            
        link_normal=links.new(norm_texture_node.outputs[0], BSDF.inputs[17])
            

        # if ORM_path is not None:
            # loaded_ORM = bpy.data.images.load(ORM_path)
            # ORM_texture_node = nodes.new("ShaderNodeTexImage")
            # ORM_texture_node.image = loaded_ORM
            # ORM_texture_node.color_space='NONE'
            
            # #On enlève l'extension au nom de la texture sinon il va exporter la texture avec deux fois .jpg
            # ORM_fullname=loaded_ORM.name
            # ORM_splitname=os.path.splitext(ORM_fullname)
            # loaded_ORM.name=ORM_splitname[0]
            
            # link_ORM=links.new(ORM_texture_node.outputs[0], GLTF.inputs[2])
            # link_ORM=links.new(ORM_texture_node.outputs[0], GLTF.inputs[7])
            
            

        # link_all= links.new(BSDF.outputs[0], nodes.get("Material Output").inputs[0])


        # #--------------------------
        # #
        # #     EXPORT OBJECT
        # #
        # #--------------------------

        #On détermine le dossier d'export, qu'il va falloir créer
        export_folderpath= os.path.join(sys.argv[8])

        # if not os.path.exists(export_folderpath):
        #     os.makedirs(export_folderpath)

        #On détermine le chemin final et le nom d'export de l'objet
        export_filepath = os.path.join(export_folderpath, sys.argv[9])


        #On exporte
        # Note que dans les arguments on peut exporter en GLTF_SEPARATE, GLB ou GLTF_EMBEDDED
        bpy.ops.export_scene.gltf(filepath=export_filepath, export_format="GLB", export_selected=True)
        # bpy.ops.object.delete()


        

run()



