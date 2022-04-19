set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath=..\Blender\2.79\scripts\addons\Object_Reexport.py

set multipleTexturesScript=..\Blender\2.79\scripts\addons\multipleTextures.py

set preProcessScriptPath=..\Blender\2.79\scripts\addons\preprocess.py



for %%I in (%1) do set name=%%~nxI

mkdir %1\..\..\Output\%name%

set inputFullPath=%1

set outputFullPath=%1\..\..\Output\%name%

REM THIS FOLDER IS ONLY FOR MULTIPLE TEXTURES
set txdir=%1\Color


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


if exist "%inputFullPath%\%name%_color.jpg" goto:jpg
if exist "%inputFullPath%\%name%_color.jpeg" goto:jpeg
if exist "%inputFullPath%\%name%_color.png" goto:png

if exist "%txdir%\" goto:multipletextures


:jpg
set image_extension=jpg
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.jpg
goto:image_extension_done

:jpeg
set image_extension=jpeg
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.jpeg
goto:image_extension_done

:png
set image_extension=png
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.png
goto:image_extension_done

:multipletextures
echo MULTIPLE TEEEEEEEEEEEXTURE
set multitexture=Yes
set image_extension=None
set texturepath=%txdir%
goto:done

:image_extension_done
echo image_extension is %image_extension%

:done

echo multitexture detected


REM BASIC VARIABLES

set processInPath=%1\%name%.%object_extension%


REM PREPARATION OF THE OBJECT PRIOR TO DECIMATION
mkdir %1\Preprocess

set preprocess_output_path=%1\Preprocess

%blenderPath% -b -P %preProcessScriptPath% -- -ifp %inputFullPath% -pip %processInPath% -n %name% -oe %object_extension% -ie %image_extension% -pop %preprocess_output_path%  -mt %multitexture% -tp %texturepath%
REM            1  2         3               4           5               6       7                 8            9                          10           11               12


set object_extension=obj

REM here we have to precise again which is the extension of the copied texture, since at the first check, if the object is gltf, then it can't find the texture and thus its extension.
if exist "%1\Preprocess\%name%_color.jpg" goto:jpg_preprocess
if exist "%1\Preprocess\%name%_color.jpeg" goto:jpeg_preprocess
if exist "%1\Preprocess\%name%_color.png" goto:png_preprocess

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
set colorPath=%1\Preprocess\%name%_color.%image_extension%
set method=DECIMATE





REM MEDIUM POLY VERSION
set diffuse_resolution=2048
set normal_resolution=1024
set mediumtarget=6000
set target_indicator=medium

mkdir %1\..\..\Output\%name%\%target_indicator%
set outFolder=%1\..\..\Output\%name%\%target_indicator%

set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %mediumtarget% -R %diffuse_resolution% -c %colorPath%


ren %outPath% %name%_Mesh_%target_indicator%.obj

set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

mkdir %outputFullPath%\Glb

set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg


set ffmpegpath=%~dp0..\ffmpeg\bin\ffmpeg.exe
"%ffmpegpath%" -y -i %normalpath% -vf scale=%normal_resolution%:%normal_resolution% %outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg

set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg


set exportpath=%outputFullPath%\Glb
set exportname=%name%_Mesh_%mediumtarget%_%diffuse_resolution%-%normal_resolution%

%blenderPath% -b -P %convertScriptPath% -- -np %newPath% -dp %diffusepath% -nop %normalpath% -ep %exportpath% -en %exportname% -dr %diffuse_resolution% -nr %normal_resolution%





echo The process is done ! You can close the console !

pause

