set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath= ..\Blender\2.79\scripts\addons\Object_Reexport.py



for %%I in (%1) do set name=%%~nxI

mkdir %1\..\..\Output\%name%

set inputFullPath=%1

set outputFullPath=%1\..\..\Output\%name%

set outFolder=%1\..\..\Output\%name%

set inPath=%1\%name%.obj

set outPath=%1\..\..\Output\%name%\%name%.obj

REM for now let's assume there will only be a jpg for the texture, and that normals and AO will be baked anyway from the high poly model. So no need to precise _diffuse after the %name%
set colorPath=%1\%name%.jpg

set target=8000

set method=DECIMATE

set resolution=1024



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