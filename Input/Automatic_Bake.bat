set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath= ..\Blender\2.79\scripts\addons\Object_Reexport.py

set convertToTrisScriptPath=..\Blender\2.79\scripts\addons\convert_to_tris.py



for %%I in (%1) do set name=%%~nxI

mkdir %1\..\..\Output\%name%

set inputFullPath=%1

set outputFullPath=%1\..\..\Output\%name%

set outFolder=%1\..\..\Output\%name%


if exist "%inputFullPath%\%name%.obj" goto:obj
if exist "%inputFullPath%\%name%.fbx" goto:fbx
if exist "%inputFullPath%\%name%.gltf" goto:gltf
if exist "%inputFullPath%\%name%.glb" goto:glb
if exist "%inputFullPath%\%name%.stl" goto:stl
if exist "%inputFullPath%\%name%.ply" goto:ply
if exist "%inputFullPath%\%name%.3ds" goto:3ds


:obj
set object_extension=obj
goto:object_extension_done

:fbx
set object_extension=fbx
goto:object_extension_done

:gltf
set object_extension=gltf
goto:object_extension_done

:glb
set object_extension=glb
goto:object_extension_done

:stl
set object_extension=stl
goto:object_extension_done

:ply
set object_extension=ply
goto:object_extension_done

:3ds
set object_extension=3ds
goto:object_extension_done


:object_extension_done
echo object extension is %object_extension%


if exist "%inputFullPath%\%name%.jpg" goto:jpg
if exist "%inputFullPath%\%name%.jpeg" goto:jpeg
if exist "%inputFullPath%\%name%.png" goto:png

:jpg
set image_extension=jpg
goto:image_extension_done

:jpeg
set image_extension=jpeg
goto:image_extension_done

:png
set image_extension=png
goto:image_extension_done

:image_extension_done
echo image_extension is %image_extension%


set inPath=%1\%name%.%object_extension%


set outPath=%1\..\..\Output\%name%\%name%.obj

REM for now let's assume there will only be a jpg for the texture, and that normals and AO will be baked anyway from the high poly model. So no need to precise _diffuse after the %name%

set colorPath=%1\%name%.%image_extension%

set target=8000

set method=DECIMATE

set resolution=1024

%blenderPath% -b -P %convertToTrisScriptPath% -- %inPath% %object_extension%


%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %target% -R %resolution% -c %colorPath%


ren %outPath% %name%_Mesh.obj

set newPath=%1\..\..\Output\%name%\%name%_Mesh.obj


ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%resolution%.jpg
ren %outFolder%\%name%_normal.jpg %name%_normal_%resolution%.jpg

mkdir %outputFullPath%\Glb

set diffusepath=%outputFullPath%\%name%_diffuse_%resolution%.jpg
set normalpath=%outputFullPath%\%name%_normal_%resolution%.jpg
set exportpath=%outputFullPath%\Glb
set exportname=%name%_Mesh_%target%




%blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname%


echo The process is done ! You can close the console !

pause