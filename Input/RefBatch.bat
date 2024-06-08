@echo off

REM Set paths
set blenderPath=blender_placeholder
set bakeScriptPath=bakescript_placeholder

set convertScriptPath=convert_script_placeholder
set preProcessScriptPath=preprocess_script_placeholder

REM Set object name
for %%I in (%1) do set name=%%~nxI

REM Create output directory if not exists
if not exist "%1\..\..\Output\%name%" (
    mkdir %1\..\..\Output\%name%
)

set inputFullPath=%1
set outputFullPath=%1\..\..\Output\%name%

REM Set texture directory
set txdir=%1\Color

REM Check for object file extension
if exist "%inputFullPath%\%name%.obj" goto :obj
if exist "%inputFullPath%\%name%.fbx" goto :fbx
if exist "%inputFullPath%\%name%.gltf" goto :gltf
if exist "%inputFullPath%\%name%.glb" goto :glb
if exist "%inputFullPath%\%name%.stl" goto :stl
if exist "%inputFullPath%\%name%.ply" goto :ply
if exist "%inputFullPath%\%name%.3ds" goto :3ds
if exist "%inputFullPath%\%name%.dae" goto :dae

:obj
set object_extension=obj
goto :object_extension_done

:fbx
set object_extension=fbx
goto :object_extension_done

:gltf
set object_extension=gltf
goto :object_extension_done

:glb
set object_extension=glb
goto :object_extension_done

:stl
set object_extension=stl
goto :object_extension_done

:ply
set object_extension=ply
goto :object_extension_done

:3ds
set object_extension=3ds
goto :object_extension_done

:dae
set object_extension=dae
goto :object_extension_done

:object_extension_done
echo Object extension is %object_extension%

REM Check for image file extension
if exist "%inputFullPath%\%name%_color.jpg" goto :jpg
if exist "%inputFullPath%\%name%_color.jpeg" goto :jpeg
if exist "%inputFullPath%\%name%_color.png" goto :png

if exist "%txdir%\" goto :multipletextures

:jpg
set image_extension=jpg
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.jpg
goto :image_extension_done

:jpeg
set image_extension=jpeg
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.jpeg
goto :image_extension_done

:png
set image_extension=png
set multitexture=No
set texturepath=%inputFullPath%\%name%_color.png
goto :image_extension_done

:multipletextures
echo Checking whether there are multiple textures
set multitexture=Yes
set image_extension=None
set texturepath=%txdir%
goto :done

:image_extension_done
echo Image extension is %image_extension%

:done
echo Multitextures detected

REM Set preprocessing variables
set processInPath=%1\%name%.%object_extension%
if not exist "%1\Preprocess" (
    mkdir %1\Preprocess
)
set preprocess_output_path=%1\Preprocess

REM Run Blender for preprocessing
%blenderPath% -b -P %preProcessScriptPath% -- -ifp %inputFullPath% -pip %processInPath% -n %name% -oe %object_extension% -ie %image_extension% -pop %preprocess_output_path% -mt %multitexture% -tp %texturepath%

REM Check for preprocessed image file extension
if exist "%1\Preprocess\%name%_color.jpg" goto :jpg_preprocess
if exist "%1\Preprocess\%name%_color.jpeg" goto :jpeg_preprocess
if exist "%1\Preprocess\%name%_color.png" goto :png_preprocess

:jpg_preprocess
set image_extension=jpg
goto :image_extension_preprocess_done

:jpeg_preprocess
set image_extension=jpeg
goto :image_extension_preprocess_done

:png_preprocess
set image_extension=png
goto :image_extension_preprocess_done

:image_extension_preprocess_done
echo Image extension after preprocessing is %image_extension%

REM Set paths for decimation
set inPath=%1\Preprocess\%name%_clean.%object_extension%
set colorPath=%1\Preprocess\%name%_color.%image_extension%
set method=DECIMATE
set diffuse_resolution=512
set normal_resolution=512
set target=2000

REM Create output target directory if not exists
if not exist "%1\..\..\Output\%name%\%target%" (
    mkdir "%1\..\..\Output\%name%\%target%"
)

set outFolder=%1\..\..\Output\%name%\%target%
set outPath=%outFolder%\%name%.obj

REM Run Blender for decimation
%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %target% -R %diffuse_resolution% -c %colorPath%

REM Rename and set new path
if exist "%outPath%" (
    ren "%outPath%" %name%_Mesh_%target%.obj
    set newPath=%outFolder%\%name%_Mesh_%target%.obj
) else (
    echo "File %outPath% not found."
    exit /b
)

REM Rename texture files
if exist "%outFolder%\%name%_albedo.jpg" (
    ren "%outFolder%\%name%_albedo.jpg" %name%_diffuse_%diffuse_resolution%_%target%.jpg
)

if exist "%outFolder%\%name%_normal.jpg" (
    ren "%outFolder%\%name%_normal.jpg" %name%_normal_%normal_resolution%_%target%.jpg
)

REM Create GLB output directory if not exists
if not exist "%outputFullPath%\Glb" (
    mkdir "%outputFullPath%\Glb"
)

REM Set paths for export
set diffusepath=%outputFullPath%\%target%\%name%_diffuse_%diffuse_resolution%_%target%.jpg
set normalpath=%outputFullPath%\%target%\%name%_normal_%normal_resolution%_%target%.jpg
set exportpath=%outputFullPath%\Glb
set exportname=%name%_Mesh_%target%_%diffuse_resolution%-%normal_resolution%

REM Run Blender for exporting to GLB
%blenderPath% -b -P %convertScriptPath% -- -np %newPath% -dp %diffusepath% -nop %normalpath% -ep %exportpath% -en %exportname% -dr %diffuse_resolution% -nr %normal_resolution%

echo Process done! You can close the console.
