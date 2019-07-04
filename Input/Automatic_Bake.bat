set blenderPath=..\Blender\blender.exe

set bakeScriptPath=..\Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py



for %%I in (%1) do set name=%%~nxI

mkdir ..\Output\%name%

set inPath=..\Input\%name%\%name%.gltf

set outPath=..\Output\%name%\%name%.gltf

set colorPath=..\Input\%name%\%name%_diffuse.png

set target=1500

set method=DECIMATE

set resolution=1024





%blenderPath% -b -P %bakeScriptPath% -- %inPath% %outPath% -M %method% -X %target% -R %resolution% -c %colorPath%

ren %outPath%.glb %name%.glb

pause