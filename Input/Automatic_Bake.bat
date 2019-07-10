set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set convertScriptPath= ..\Blender\2.79\scripts\addons\testScript.py



for %%I in (%1) do set name=%%~nxI

mkdir ..\Output\%name%

set outFolder=..\Output\%name%

set inPath=..\Input\%name%\%name%.fbx

set outPath=..\Output\%name%\%name%.obj

set colorPath=..\Input\%name%\%name%_diffuse.png

set target=1500

set method=DECIMATE

set resolution=1024

set word=Bouh





%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %target% -R %resolution% -c %colorPath%

REM ren %outPath%.glb %name%.glb

ren %outPath% %name%_Mesh.obj

ren %outFolder%\%name%_albedo.jpg %name%_diffuse_%resolution%.jpg
ren %outFolder%\%name%_normal.jpg %name%_normal_%resolution%.jpg






pause