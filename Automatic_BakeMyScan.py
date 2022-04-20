
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from GUI_BMS import Ui_MainWindow
import sys
import os
import shutil
import subprocess
import time


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        #Define a "latest path" text file
        self.this_script_path = os.path.realpath(__file__)
        self.plugin_path = os.path.dirname(self.this_script_path)
        self.default_path_file = os.path.join(self.this_script_path, '..', 'default_path.txt')
        if os.path.exists(self.default_path_file):
            print("Found the default path file")
            self.file = open(self.default_path_file, "r")
            self.file_lines = self.file.readlines()
            self.default_path = self.file_lines[0]
            print("the default path is " + str(self.default_path))
            self.file.close()
        
        else:
            print("default file not found")
            self.file = open(self.default_path_file, "w+")
            self.file.write(self.plugin_path)
            self.default_path = self.plugin_path
            self.file.close()


        #Connect the Plugin input button to browser
        self.plugin_input_button = self.ui.plugin_input_button
        self.plugin_input_button.setText(self.default_path)
        self.plugin_input_button.clicked.connect(self.browsePlugin)
        

        #Connect the Object input button to browser
        self.object_input_button = self.ui.object_input_button
        self.object_input_button.clicked.connect(self.browseObject)


        #Connect the polygon button
        self.target_line = self.ui.polygons_lineEdit
        self.target_line.textChanged.connect(self.onChangeText)

        #Connect the Combo box
        self.diffres_comboBox = self.ui.diffres_comboBox
        self.diffres_comboBox.currentIndexChanged.connect(self.getDiffComboValue)

        self.normres_comboBox = self.ui.normres_comboBox
        self.normres_comboBox.currentIndexChanged.connect(self.getNormComboValue)

    
        #At last connect the decimate button, which will essentially send all the data to the ObjectDataClass
        self.decimate_button = self.ui.decimate_button
        self.decimate_button.clicked.connect(self.start)

        #Console display
        self.consoleText = self.ui.plainTextEdit
        

    
    #Ideally we should find a way to put arguments directly inside the function called into clicked.connect. Here we have to actually separate what we 
    # want in two branches in order to be able to pass an argument to the browse function, and thus avoid to define it twice.
    def browsePlugin(self):
        self.browse("Plugin")
    
    def browseObject(self):
        self.browse("Object")
        
    
    def browse(self, string):
        # print("You clicked on the plugin input button")
        # print(string)

        if string is "Plugin":
            foldername= QFileDialog.getExistingDirectory(
                self,
                caption='Select a folder'
            )
            if foldername:
                    self.plugin_input_button.setText(foldername)
                    self.plugin_path = foldername
                    self.default_path = self.plugin_path

                    print("plugin path is " + self.default_path)

                    #Here we make sure the last location chosen will become the default location at the next iteration
                    file = open(self.default_path_file, "r+")
                    
                
                    for line in file:
                        print("I'm analyzing the content of the file")
                        if self.plugin_path not in line:

                            print(self.plugin_path  + " is not in the file")
                            file.seek(0)
                            file.write(self.plugin_path)
                            file.truncate()
                        
                        else:
                            print('Path is identical, no changes made')
                    
                    
                    self.file.close()
                
                    
        

        if string is "Object":
            #◙I'm deleting gltf as there is currently a problem at import (maybe the importer is too old)
            fname = QFileDialog.getOpenFileName(self, "Choose your file", "", 
            "Obj Files (*.obj);;Fbx Files (*.fbx);; GLB Files (*.glb);; STL Files (*.stl) ;; PLY Files (*.ply) ;; 3ds Files (*.3ds);; DAE Files (*.dae)")[0]
            if fname:
                self.object_path = fname
                self.object_folder = os.path.dirname(fname)
                # print("object file is" + fname)
                # print ("object folder is " + self.object_folder)
                self.object_input_button.setText(fname)


    
    #Let's notice here that it does consider to be passing an argument to the function, which is the text with the textChanged
    def onChangeText(self, text):
        # print(text)
        self.target = str(text)
        # print("Target is now " + self.target)
        
    #Same thing here with the separation of the method in two
    def getDiffComboValue(self):
        self.diffuse_resolution = self.getComboValue("diffuse")

    def getNormComboValue(self):
        self.normal_resolution = self.getComboValue("normal")
        
    def getComboValue(self, string):
        if string == "diffuse":
        #We are storing this into an it because the resolution parameter will need to be an int or float, not a string.
            self.res = int(self.diffres_comboBox.currentText())

        if string == "normal":
            self.res = int(self.normres_comboBox.currentText())

        # print ("resolution is " + str(self.res))
        return self.res


    # This function will allow, for now, to just change a few parameters in the batch script that used to be launched manually. Ideally,
    # the whold batch script should be rewritten through Python with variables. See Flag_Generator script.



    def start(self):
        self.consoleText.setPlainText("Processing your object, please wait...")
        self.processBatch()

    def processBatch(self):
        

        self.batch_script = self.writeBatch()
        self.launchBatch(self.batch_script)
        self.cleanBatch(self.batch_script)
        self.consoleText.setPlainText("Your object has been processed, you will find it in the Output folder :)")
     
        

    def writeBatch(self):
        #Copy the batch file
        src_batch = os.path.join(self.plugin_path, "Input","RefBatch.bat")
        dst_batch = os.path.join(self.plugin_path, "Input","Running.bat")
        shutil.copyfile(src_batch, dst_batch)
        self.batch_script = dst_batch

        #Here i'm making sure the path written in the batch file will be correctly syntaxed

        path = self.convertPath(self.object_folder)
        replacement = ""

        file = open(self.batch_script, "r")

        for line in file :
            if "%1" in line:
                changes = line.replace("%1", path)
                replacement = replacement + changes
            
            elif "set diffuse_resolution=" in line:
                changes = line.replace("1024", str(self.diffuse_resolution))
                replacement = replacement + changes
            
            elif "set normal_resolution=" in line:
                changes = line.replace("1024", str(self.normal_resolution))
                replacement = replacement + changes

            elif "set target=" in line :
                changes = line.replace("1500", str(self.target))
                replacement = replacement + changes

            
            else:
                replacement = replacement + line
        

        file.close()
        fout = open(self.batch_script, "w")
        fout.write(replacement)
        fout.close()

        return self.batch_script

    def launchBatch(self, script):
        #Launch bat. The process_wait() makes sure that all the images are done.
        process  = subprocess.Popen(script)
        process.wait()



    def cleanBatch(self,script):
        os.remove(script)
     

    def convertPath(self, path):
        path = path.replace("/", os.sep)
        # print("New path is " + path)

        return path
    
        


        #deduce the other back end data

        






def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()

    sys.exit(app.exec_())



window()