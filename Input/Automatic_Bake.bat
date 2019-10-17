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

%blenderPath% -P %preProcessScriptPath% -- %inputFullPath% %processInPath% %name% %object_extension% %image_extension% %preprocess_output_path%  %multitexture% %texturepath%
REM            1               2         3        4             5               6           7                 8            9                          10           11



REM set object_extension=obj

REM REM here we have to precise again which is the extension of the copied texture, since at the first check, if the object is gltf, then it can't find the texture and thus its extension.
REM if exist "%1\Preprocess\%name%.jpg" goto:jpg_preprocess
REM if exist "%1\Preprocess\%name%.jpeg" goto:jpeg_preprocess
REM if exist "%1\Preprocess\%name%.png" goto:png_preprocess

REM :jpg_preprocess
REM set image_extension=jpg
REM goto:image_extension_preprocess_done

REM :jpeg_preprocess
REM set image_extension=jpeg
REM goto:image_extension_preprocess_done

REM :png_preprocess
REM set image_extension=png
REM goto:image_extension_preprocess_done


REM :image_extension_preprocess_done
REM echo image_extension is %image_extension%


REM set inPath=%1\Preprocess\%name%_clean.%object_extension%
REM set colorPath=%1\Preprocess\%name%.%image_extension%
REM set method=DECIMATE

REM REM VERY LOW POLY VERSION

REM set diffuse_resolution=1024
REM set normal_resolution=1024
REM set verylowtarget=1500
REM set target_indicator=verylow

REM mkdir %1\..\..\Output\%name%\%target_indicator%
REM set outFolder=%1\..\..\Output\%name%\%target_indicator%

REM set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj


REM %blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %verylowtarget% -R %diffuse_resolution% -c %colorPath%


REM ren %outPath% %name%_Mesh_%target_indicator%.obj

REM set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


REM ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

REM mkdir %outputFullPath%\Glb

REM set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg
REM set exportpath=%outputFullPath%\Glb
REM set exportname=%name%_Mesh_%verylowtarget%_%diffuse_resolution%-%normal_resolution%



REM %blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%

echo very low poly exported, going to low

pause


REM REM LOW POLY VERSION
REM set diffuse_resolution=1024
REM set normal_resolution=1024
REM set lowtarget=3000
REM set target_indicator=low

REM mkdir %1\..\..\Output\%name%\%target_indicator%
REM set outFolder=%1\..\..\Output\%name%\%target_indicator%

REM set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



REM %blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %lowtarget% -R %diffuse_resolution% -c %colorPath%


REM ren %outPath% %name%_Mesh_%target_indicator%.obj

REM set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


REM ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

REM mkdir %outputFullPath%\Glb

REM set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg
REM set exportpath=%outputFullPath%\Glb
REM set exportname=%name%_Mesh_%lowtarget%_%diffuse_resolution%-%normal_resolution%


REM %blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%


REM echo low poly exported, going to medium



REM REM MEDIUM POLY VERSION
REM set diffuse_resolution=2048
REM set normal_resolution=1024
REM set mediumtarget=6000
REM set target_indicator=medium

REM mkdir %1\..\..\Output\%name%\%target_indicator%
REM set outFolder=%1\..\..\Output\%name%\%target_indicator%

REM set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



REM %blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %mediumtarget% -R %diffuse_resolution% -c %colorPath%


REM ren %outPath% %name%_Mesh_%target_indicator%.obj

REM set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


REM ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

REM mkdir %outputFullPath%\Glb

REM set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg


REM set ffmpegpath=%~dp0..\ffmpeg\bin\ffmpeg.exe
REM "%ffmpegpath%" -y -i %normalpath% -vf scale=%normal_resolution%:%normal_resolution% %outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg

REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg


REM set exportpath=%outputFullPath%\Glb
REM set exportname=%name%_Mesh_%mediumtarget%_%diffuse_resolution%-%normal_resolution%

REM %blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%



REM echo medium poly exported, going to high

REM REM HIGH POLY VERSION
REM set diffuse_resolution=2048
REM set normal_resolution=2048
REM set hightarget=10000
REM set target_indicator=high

REM mkdir %1\..\..\Output\%name%\%target_indicator%
REM set outFolder=%1\..\..\Output\%name%\%target_indicator%

REM set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



REM %blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %hightarget% -R %diffuse_resolution% -c %colorPath%


REM ren %outPath% %name%_Mesh_%target_indicator%.obj

REM set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


REM ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

REM mkdir %outputFullPath%\Glb

REM set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg
REM set exportpath=%outputFullPath%\Glb
REM set exportname=%name%_Mesh_%hightarget%_%diffuse_resolution%-%normal_resolution%


REM %blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%

REM echo medium poly exported, going to high

REM REM VERY HIGH POLY VERSION
REM set diffuse_resolution=2048
REM set normal_resolution=2048
REM set veryhightarget=50000
REM set target_indicator=veryhigh

REM mkdir %1\..\..\Output\%name%\%target_indicator%
REM set outFolder=%1\..\..\Output\%name%\%target_indicator%

REM set outPath=%1\..\..\Output\%name%\%target_indicator%\%name%.obj



REM %blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %veryhightarget% -R %diffuse_resolution% -c %colorPath%


REM ren %outPath% %name%_Mesh_%target_indicator%.obj

REM set newPath=%1\..\..\Output\%name%\%target_indicator%\%name%_Mesh_%target_indicator%.obj


REM ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM ren %outFolder%\%name%_normal.jpg %name%_normal_%normal_resolution%_%target_indicator%.jpg

REM mkdir %outputFullPath%\Glb

REM set diffusepath=%outputFullPath%\%target_indicator%\%name%_diffuse_%diffuse_resolution%_%target_indicator%.jpg
REM set normalpath=%outputFullPath%\%target_indicator%\%name%_normal_%normal_resolution%_%target_indicator%.jpg
REM set exportpath=%outputFullPath%\Glb
REM set exportname=%name%_Mesh_%veryhightarget%_%diffuse_resolution%-%normal_resolution%


REM %blenderPath% -b -P %convertScriptPath% -- %newPath% %diffusepath% %normalpath% %exportpath% %exportname% %diffuse_resolution% %normal_resolution%



REM echo The process is done ! You can close the console !

REM pause