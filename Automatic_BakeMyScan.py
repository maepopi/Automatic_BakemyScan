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
        # Define a "latest path" text file
        self.this_script_path = os.path.realpath(__file__)
        self.plugin_path = os.path.dirname(self.this_script_path)
        self.default_path_file = os.path.join(self.this_script_path, '..', 'default_path.txt')
        if os.path.exists(self.default_path_file):
            print("Found the default path file")
            self.file = open(self.default_path_file, "r")
            self.file_lines = self.file.readlines()
            self.default_path = self.file_lines[0]
            print("The default path is " + str(self.default_path))
            self.file.close()
        
        else:
            print("Default file not found")
            self.file = open(self.default_path_file, "w+")
            self.file.write(self.plugin_path)
            self.default_path = self.plugin_path
            self.file.close()

        # Connect the Plugin input button to browser
        self.plugin_input_button = self.ui.plugin_input_button
        self.plugin_input_button.setText(self.default_path)
        self.plugin_input_button.clicked.connect(self.browsePlugin)

        # Connect Blender path input button to browser
        self.blender_input_button = self.ui.blender_input_button
        self.blender_input_button.clicked.connect(self.browseBlender)
        
        # Connect the Object input button to browser
        self.object_input_button = self.ui.object_input_button
        self.object_input_button.clicked.connect(self.browseObject)

        # Connect the polygon button
        self.target_line = self.ui.polygons_lineEdit
        self.target_line.textChanged.connect(self.onChangeText)

        # Connect the Combo box
        self.diffres_comboBox = self.ui.diffres_comboBox
        self.diffres_comboBox.currentIndexChanged.connect(self.getDiffComboValue)

        self.normres_comboBox = self.ui.normres_comboBox
        self.normres_comboBox.currentIndexChanged.connect(self.getNormComboValue)
    
        # Connect the decimate button, which will essentially send all the data to the ObjectDataClass
        self.decimate_button = self.ui.decimate_button
        self.decimate_button.clicked.connect(self.start)

        # Console display
        self.consoleText = self.ui.console  # Corrected the attribute name
        
    def browsePlugin(self):
        self.browse("Plugin")
    
    def browseObject(self):
        self.browse("Object")

    def browseBlender(self):
        self.browse("Blender")
    
    def browse(self, string):
        if string == "Blender":
            fname = QFileDialog.getOpenFileName(self, "Choose your Blender executable", "", "Executable Files (*.exe);;All Files (*)")[0]
            if fname:
                self.blender_path = fname
                self.blender_input_button.setText(fname)
                print("Blender path is " + self.blender_path)
        elif string == "Plugin":
            foldername = QFileDialog.getExistingDirectory(self, caption='Select a folder')
            if foldername:
                self.plugin_input_button.setText(foldername)
                self.plugin_path = foldername
                self.default_path = self.plugin_path
                print("Plugin path is " + self.default_path)

                # Update the default path file
                with open(self.default_path_file, "w") as file:
                    file.write(self.plugin_path)
        elif string == "Object":
            fname = QFileDialog.getOpenFileName(self, "Choose your file", "", "Obj Files (*.obj);;Fbx Files (*.fbx);; GLB Files (*.glb);; STL Files (*.stl);; PLY Files (*.ply);; 3ds Files (*.3ds);; DAE Files (*.dae)")[0]
            if fname:
                self.object_path = fname
                self.object_folder = os.path.dirname(fname)
                self.object_input_button.setText(fname)

    def onChangeText(self, text):
        self.target = str(text)
        
    def getDiffComboValue(self):
        self.diffuse_resolution = self.getComboValue("diffuse")

    def getNormComboValue(self):
        self.normal_resolution = self.getComboValue("normal")
        
    def getComboValue(self, string):
        if string == "diffuse":
            self.res = int(self.diffres_comboBox.currentText())

        if string == "normal":
            self.res = int(self.normres_comboBox.currentText())

        return self.res

    def start(self):
        self.consoleText.setPlainText("Processing your object, please wait...")
        self.processBatch()

    def processBatch(self):
        self.batch_script = self.writeBatch()
        self.launchBatch(self.batch_script)
        self.cleanBatch(self.batch_script)
        self.consoleText.setPlainText("Your object has been processed, you will find it in the Output folder :)")
     
    def writeBatch(self):
        # Copy the batch file
        src_batch = os.path.join(self.plugin_path, "Input", "RefBatch.bat")
        dst_batch = os.path.join(self.plugin_path, "Input", "Running.bat")
        shutil.copyfile(src_batch, dst_batch)
        self.batch_script = dst_batch

        path = self.convertPath(self.object_folder)
        replacement = ""

        file = open(self.batch_script, "r")

        for line in file:
            if "%1" in line:
                changes = line.replace("%1", path)
                replacement += changes
            
            elif "set diffuse_resolution=" in line:
                changes = line.replace("1024", str(self.diffuse_resolution))
                replacement += changes
            
            elif "set normal_resolution=" in line:
                changes = line.replace("1024", str(self.normal_resolution))
                replacement += changes

            elif "set target=" in line:
                changes = line.replace("1500", str(self.target))
                replacement += changes

            elif "set blenderPath=" in line:
                changes = line.replace("blender_placeholder", self.blender_path)
                replacement += changes
            
            elif "set bakeScriptPath" in line:
                blender_folder = os.path.dirname(self.blender_path)
                bakemyscan_script = os.path.join(blender_folder, '2.79', 'scripts', 'addons', 'BakeMyScan', 'scripts', 'bakemyscan.py' )
                changes = line.replace("bakescript_placeholder", bakemyscan_script)
                replacement += changes  
            
            elif "set convertScriptPath" in line:
                blender_folder = os.path.dirname(self.blender_path)
                convert_script = os.path.join(blender_folder, '2.79', 'scripts', 'addons', 'auto_bakemyscan_object_reexport.py' )
                changes = line.replace("convert_script_placeholder", convert_script)
                replacement += changes  

            elif "set preProcessScriptPath" in line:
                blender_folder = os.path.dirname(self.blender_path)
                preprocess_script = os.path.join(blender_folder, '2.79', 'scripts', 'addons', 'auto_bakemyscan_preprocess.py' )
                changes = line.replace("preprocess_script_placeholder", preprocess_script)
                replacement += changes  

            
            
            else:
                replacement += line

        with open(self.batch_script, "w") as fout:
            fout.write(replacement)

        return self.batch_script

    def launchBatch(self, script):
        process = subprocess.Popen(script)
        process.wait()

    def cleanBatch(self, script):
        os.remove(script)

    def convertPath(self, path):
        path = path.replace("/", os.sep)
        return path

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()