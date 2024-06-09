# Automatic_BakemyScan

>**Disclaimer**:
> 
>This code is rather old. It's a project I worked on when I was doing my PhD thesis and building AR/VR applications for museums. At the time, I was also learning to code and it is very palpable in the current state of the code! When I've got some time, I'll try refactoring it and make it simpler and more readable.

# Introduction

This tutorial presents a small program we have developed thanks to <a href="http://bakemyscan.org/" target="blank">Loic Norgeot's </a> awesome and opensource plugin for Blender, called **"Bake my scan"**. It is a plugin that allows you to quickly process your **3D scans** or **highly complex objects** for them to be imported in real-time applications.

I simply turned it into an independant plugin you can launch through a python app. There's also a "manual" process that allows you to drag and drop a folder containing your object and its diffuse texture on top of a batch script.

I also have developed a version of this plugin which allows you to simply **drag and drop an object** on a script, and it will **automatically process it** and export five different versions of the decimated object, from very low poly (1 500 triangles) to relatively high (120 000 triangles). 

# Installation
1. Clone the repo
2. Install, somewhere on your computer, [Blender 2.79](https://www.blender.org/download/releases/2-79/) (portable preferably)
3. In your cloned repository, copy paste the "addons" folder located in "src" into the "2.79/scripts" folder of your Blender installation.
4. Open Blender, go into User Preferences, and activate these two addons:
    - Bake my scan
    - Import-Export: glTF 2.0 format
5. Save the user preferences


# Usage
## How to prepare your object
The script is designed to be able to import most of the existing 3D formats. In the "input" folder, **create a new folder** named after the object you want to optimize. Foe example let's say **"Cat"**.

In this folder, first you have to put your high-poly mesh, **named exactly like the folder** (in our case, **"Cat"**). In the end, your object should look like something like **"Cat.obj"** or **"Cat.fbx"**.

In the same folder, you now have to put your diffuse texture, that is to say the **color map** of your object. There again, it should be **named exactly like the folder**, but you should add **"_color"** to the name of your texture. You now should have something like **"Cat_color.jpg"** or **"Cat_color.png"**.

> **Multiple textures**
>
> If your object has **several color textures**, you must **create** a **"Color"** folder and put the textures in **there**. **Each texture** should be named **"name_color0"**, **"name_color1"**, etc.


## Through the app
1. Double click on Automatic_BakeMyScan.exe
2. Browse the different forms to locate the repo itself, then the Blender executable, and the object you want to optimize (go fetch the actual 3D object inside the "input" folder)
3. Specify your target polygon amount to which you want the object decimated
4. Specify the resolution you want for the diffuse texture as well as for the normal texture
5. Hit "Decimate". When your object is ready, it will be in the "Output" folder.


## Through the batch script
You can drag and drop your folder containing your object to decimate directly onto the **Automatic_Bake_Batch_Resolution.bat** script. This will result in outputting different decimated versions of your object, in the "Output" folder.

>Note:
> 
> The "Output" folder contains a folder with the name of your processed object. For example "Cat". Inside this folder, you have a "GLB" folder which contains the GLB outputs of your model. Alongside this "GLB" folder, you have different folders named with the deximation target ("verylow", "low" etc.) which each contains the obj version of the object, alongside the unpacked textures.