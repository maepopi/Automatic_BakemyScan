set blenderPath=..\Blender\blender.exe

set convertScriptPath= ..\Blender\2.79\scripts\addons\Object_Reexport.py

set objectPath=E:\MaelysJob\LOCAL_GIT_PROJECTS\AUTOMATIC_BAKEMYSCAN\Automatic_BakemyScan\Output\Inuit\Inuit_Mesh.obj

set resolution=1024


%blenderPath% -P %convertScriptPath% -- %objectPath% 


pause