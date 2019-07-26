set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath= ..\Blender\2.79\scripts\addons\Object_Reexport.py

set convertToTrisScriptPath=..\Blender\2.79\scripts\addons\convert_to_tris.py



for %%I in (%1) do set name=%%~nxI

mkdir %1\..\..\Output\%name%

set inputFullPath=%1

set outputFullPath=%1\..\..\Output\%name%




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


REM BASIC VARIABLES

set inPath=%1\%name%.%object_extension%
set colorPath=%1\%name%.%image_extension%
set method=DECIMATE
set resolution=1024


REM PREPARATION OF THE OBJECT PRIOR TO DECIMATION

%blenderPath% -b -P %convertToTrisScriptPath% -- %inPath% %object_extension%

REM VERY LOW POLY VERSION
set verylowtarget=1500
set target_indicator=verylow

mkdir %1\..\..\Output\%name%\%target_indicator%
set outFolder=%1\..\..\Output\%name%\%target_indicator%

set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %verylowtarget% -R %resolution% -c %colorPath%


ren %outPath% %name%_Mesh_%target_indicator%.obj

set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%resolution%_%target_indicator%.jpg
ren %outFolder%\%name%_normal.jpg %name%_normal_%resolution%_%target_indicator%.jpg

mkdir %outputFullPath%\Glb

set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%resolution%_%target_indicator%.jpg
set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%resolution%_%target_indicator%.jpg
set exportpath=%outputFullPath%\Glb
set exportname=%name%_Mesh_%verylowtarget%



%blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname%


REM MEDIUM POLY VERSION


echo The process is done ! You can close the console !

pause