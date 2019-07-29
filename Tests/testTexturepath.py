import bpy

ma_scene = bpy.context.scene
for un_objet in ma_scene.objects:
    if un_objet.type == 'MESH':
        #je dit à chaque objet mesh que je rencontre (donc normalement un seul) d'être actif
        bpy.context.scene.objects.active = un_objet

        #je fous dans une variable ce qui doit normalementetre mon seul objet actif
curr_object = bpy.context.active_object

material = curr_object.data.materials[0]

material.use_nodes = True

tree = material.node_tree
nodes = tree.nodes
links = tree.links

BSDF = nodes.get("Principled BSDF")

socket = BSDF.inputs[0]

link = next( link for link in links if link.to_node == BSDF and link.to_socket == socket )

imageNode = link.from_node

if imageNode.type == 'TEX_IMAGE':
    image = imageNode.image
    
    print (image.name)