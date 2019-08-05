set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath=..\Blender\2.79\scripts\addons\Object_Reexport.py

set preProcessScriptPath=..\Blender\2.79\scripts\addons\preprocess.py



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
if exist "%inputFullPath%\%name%.dae" goto:dae


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

:dae
set object_extension=dae
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

set processInPath=%1\%name%.%object_extension%


REM PREPARATION OF THE OBJECT PRIOR TO DECIMATION
mkdir %1\Preprocess

set preprocess_output_path=%1\Preprocess

%blenderPath% -b -P %preProcessScriptPath% -- %inputFullPath% %processInPath% %object_extension% %image_extension% %preprocess_output_path% %name%

set object_extension=obj

REM here we have to precise again which is the extension of the copied texture, since at the first check, if the object is gltf, then it can't find the texture and thus its extension.
if exist "%1\Preprocess\%name%.jpg" goto:jpg_preprocess
if exist "%1\Preprocess\%name%.jpeg" goto:jpeg_preprocess
if exist "%1\Preprocess\%name%.png" goto:png_preprocess

:jpg_preprocess
set image_extension=jpg
goto:image_extension_preprocess_done

:jpeg_preprocess
set image_extension=jpeg
goto:image_extension_preprocess_done

:png_preprocess
set image_extension=png
goto:image_extension_preprocess_done


:image_extension_preprocess_done
echo image_extension is %image_extension%


set inPath=%1\Preprocess\%name%_clean.%object_extension%
set colorPath=%1\Preprocess\%name%.%image_extension%
set method=DECIMATE



REM LOW POLY VERSION
set diffuse_resolution=1024
set normal_resolution=1024
set lowtarget=3000
set target_indicator=low

mkdir %1\..\..\Output\%name%\%target_indicator%
set outFolder=%1\..\..\Output\%name%\%target_indicator%

set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %lowtarget% -R %diffuse_resolution% -c %colorPath%


ren %outPath% %name%_Mesh_%target_indicator%.obj

set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

mkdir %outputFullPath%\Glb

set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg
set exportpath=%outputFullPath%\Glb
set exportname=%name%_Mesh_%lowtarget%_%diffuse_resolution%-%normal_resolution%


%blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%


echo low poly exported, going to medium






echo The process is done ! You can close the console !

pause