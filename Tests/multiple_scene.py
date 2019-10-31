import bpy


def SetScene(list_scenes):
    for i in range (len(list_scenes)):
        scene = list_scenes[i]
        for obj in scene.objects:
            if obj.name != 'RootNode' and obj.type == 'MESH':
                bpy.context.window.screen.scene = bpy.data.scenes[scene.name]
    
def Run():
    list_scenes = bpy.data.scenes

    if len(list_scenes)>1:
        SetScene(list_scenes)
        scene = bpy.context.scene
        
                    
    else:
        pass
    
    
    print(scene.name)

    for object in scene.objects:
        
        if object.name == 'Object_3':
            print ('FOUND')
        
Run()