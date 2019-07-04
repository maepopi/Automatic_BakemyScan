set blenderPath=Blender\blender.exe

set bakeScriptPath=Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set inPath=Input\Femme.fbx

set outPath=Output\Femme.obj

%blenderPath% -b -P %bakeScriptPath% -- %InPath% %outPath%

pause