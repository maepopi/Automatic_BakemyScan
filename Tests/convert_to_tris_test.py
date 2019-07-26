import bpy
import bmesh


ma_scene = bpy.context.scene
for un_objet in ma_scene.objects:
    if un_objet.type == 'MESH':
        bpy.context.scene.objects.active = un_objet

        
curr_object = bpy.context.active_object

object = curr_object.data
bm=bmesh.new()
bm.from_mesh(object)

bmesh.ops.triangulate(bm, faces=bm.faces[:],quad_method=0,ngon_method=0)

bm.to_mesh(object)
bm.free()

