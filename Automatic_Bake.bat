set blenderPath=Blender\blender.exe

set bakeScriptPath=Blender\2.79\scripts\addons\BakeMyScan\scripts\bakemyscan.py

set inPath=Input\Inuit.fbx

set outPath=Output\Inuit.obj

set colorPath=Input\5000_Inuit_Texture_retouche.png

set target=1500

set method=DECIMATE

set resolution=1024



%blenderPath% -b -P %bakeScriptPath% -- %InPath% %outPath% -M %method% -X %target% -R %resolution% -c %colorPath%

pause