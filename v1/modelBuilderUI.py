import tkinter as tk
import os
import time
from tkinter import filedialog as fd
from tkinter import ttk
import json


class ModuleUI:
    def __init__(self):
        self.maxWidth = 1300
        self.maxHeight = 700
        self.state = ("disabled", "normal")
        self.allCode = ""
        self.boolState = False
        self.window = tk.Tk()
        self.window.title('Model Builder')
        self.window.geometry('{}x{}'.format(self.maxWidth, self.maxHeight))
        self.window.minsize(self.maxWidth, self.maxHeight)
        self.window.maxsize(self.maxWidth, self.maxHeight)
        self.frameLabel1 = tk.LabelFrame(self.window, width=int(self.maxWidth * (2 / 5)), height=self.maxHeight, bg="#87CEEB")
        self.frameLabel1.pack(side="left")
        self.frameLabel2 = tk.LabelFrame(self.window, width=int(self.maxWidth * (3 / 5)), height=self.maxHeight, bg="#6495ED")
        self.frameLabel2.pack(side="right")
        self.scrollBar = tk.Scrollbar(self.frameLabel2, orient="vertical", width=15)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listBox = tk.Listbox(self.frameLabel2, width=100, height=50, bg="#6495ED", yscrollcommand=self.scrollBar.set, font=("Consolas", 12))
        self.listBox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollBar.configure(command=self.listBox.yview)

        self._createConstantValues()
        self._createAllLabels()
        self._createAllBtn()
        self._createAllEntry()
        self._createAllCombobox()
        self.varLayerTypeNotUseTkObj = {
            "Conv2D": [],
            "Dense": [self.layerKernelSizeCom],
            "MaxPooling2D": [self.unitNumEntry, self.layerActivationCom, self.inputShapeEntry],
            "Flatten": [self.unitNumEntry, self.layerKernelSizeCom, self.layerActivationCom, self.inputShapeEntry],
            "Dropout": [self.layerKernelSizeCom, self.layerActivationCom, self.inputShapeEntry]
        }
        self.varLayerAllTkObj = [self.unitNumEntry, self.layerKernelSizeCom, self.layerActivationCom, self.inputShapeEntry]
        self.update()
        # for i in range(40):
        #     self.listBox.insert(i, "hewd\n")
        #
        # for i in range(41, 61):
        #     self.listBox.insert(i, "dsasad\n")

    def _createConstantValues(self):
        self.labelPlaceX = 30
        self.labelStartY = 30
        self.labelMarginY = 30
        self.comboboxPlaceX = 200
        self.comboboxStartY = 30
        self.comboboxMarginY = 30
        self.comboboxWidth = 15
        self.lastSelected = 0
        self.preTime = time.time()
        self.modelName = ""
        self.importCommand = "import tensorflow as tf\n" \
                             "import cv2\n" \
                             "from tensorflow.keras import Sequential\n" \
                             "from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Flatten, Dropout\n\n\n"
        self.isBuildSequential = False
        self.initialCommand = "model = Sequential(name=)"

        self.varFrame1Labels = ["Model Name", "Choose Layer", "Units Num", "Kernel Size", "Activation", "Input Shape", "File Directory"]
        self.varModelLayerNames = ["Conv2D", "Dense", "MaxPooling2D", "Flatten", "Dropout"]
        self.varLayerChoiceInstallCmd = {
            "Conv2D": "model.add(Conv2D(filters=, kernel_size=, activation=, input_shape=))",
            "Dense": "model.add(Dense(units=, activation=, input_shape=))",
            "MaxPooling2D": "model.add(MaxPooling2D(pool_size=))",
            "Flatten": "model.add(Flatten())",
            "Dropout": "model.add(Dropout(rate=))"
        }
        self.varLayerKernelSize = ["(9, 9)", "(7, 7)", "(5, 5)", "(3, 3)"]
        self.varLayerPoolSize = ["(2, 2)", "(3, 3)", "(4, 4)", "(5, 5)", "(6, 6)", "(7, 7)", "(8, 8)", "(9, 9)"]
        self.varModelActivations = ["relu", "tanh", "sigmoid", "softmax"]
        self.allLayerNum = self.varConv2DNum = self.varDenseNum = self.varMaxPooling2DNum = self.varFlattenNum = self.varDropoutNum = 0
        self.varUnitNumRateNum = {
            "Conv2D": "Filters Num",
            "Dense": "Units Num",
            "Dropout": "Dropout Rate"
        }
        self.varAllSize = {
            "Conv2D": ["Kernel Size", self.varLayerKernelSize],
            "MaxPooling2D": ["Pool Size", self.varLayerPoolSize]
        }
        self.varAllLayerCommand = {}
        for key in self.varLayerChoiceInstallCmd.keys():
            self.varAllLayerCommand.setdefault(key, {})
        self.varAllCommand = {}
        self.allLabels = []
        self.varLayerNumDict = {
            "Conv2D": self.varConv2DNum,
            "Dense": self.varDenseNum,
            "MaxPooling2D": self.varMaxPooling2DNum,
            "Flatten": self.varFlattenNum,
            "Dropout": self.varDropoutNum
        }
        self.varAllPath = []
        self.dirPath = ""

    def _createAllLabels(self):
        for label in self.varFrame1Labels:
            i = self.varFrame1Labels.index(label)
            self.allLabels.append(tk.Label(self.frameLabel1, text=label, width=15, font=("Consolas", 12)))
            self.allLabels[i].place(x=self.labelPlaceX,
                                    y=self.labelStartY + self.labelMarginY * self.varFrame1Labels.index(label))

    def _createAllBtn(self):
        self.openFileBtn = tk.Button(self.frameLabel1, text="View Path", width=10, font=("Consolas", 12),
                                     command=self.openFile)
        self.openFileBtn.place(x=51, y=247)
        self.addBtn = tk.Button(self.frameLabel1, text="Add", width=10, font=("Consolas", 12),
                                command=self._addLayer)
        self.addBtn.place(x=51, y=284)
        self.removeBtn = tk.Button(self.frameLabel1, text="Remove", width=10, font=("Consolas", 12),
                                   command=self._removeLayer)
        self.removeBtn.place(x=51, y=321)
        self.createBtn = tk.Button(self.frameLabel1, text="Create", width=10, font=("Consolas", 12),
                                   command=self._createFile)
        self.createBtn.place(x=51, y=358)

    def _createFile(self):
        directory = str(self.directoryCom.get())
        with open(fr"{directory}/{self.modelName}_model.py", "w") as f:
            f.write(self.importCommand)
            f.write(f"def {self.modelName}_createModel():\n\t")
            f.write(self.initialCommand + "\n")
            for key in self.varAllCommand.keys():
                for name in self.varAllCommand[key].keys():
                    f.write("\t")
                    name = str(name).replace("\'", '\"')
                    f.write(self.varAllCommand[key][name][1] + "\n")
            f.write("\treturn model\n")
            f.write("\n\n")
            f.write(f"if __name__ == \"__main__\":\n\t"
                    f"model = {self.modelName}_createModel()\n")

    def _removeLayer(self):
        layerName = ''
        self.chosenLayerId = self.listBox.curselection()[0] + 1
        self.listBox.delete(self.chosenLayerId - 1)
        self.listBox.select_clear(self.chosenLayerId)
        self.listBox.select_set(0)
        for key in self.varAllCommand[self.chosenLayerId].keys():
            layerName = str(key).replace("\'", '\"')
        layerNum = self.varAllCommand[self.chosenLayerId][layerName][0]
        self.varAllLayerCommand[layerName].pop(f"layer{layerNum}")
        self.varAllCommand.pop(self.chosenLayerId)
        layerTemp = self.varAllLayerCommand.copy()
        temp = self.varAllCommand.copy()
        self.varAllLayerCommand = {}
        for key in self.varLayerChoiceInstallCmd.keys():
            self.varAllLayerCommand.setdefault(key, {})
        self.varAllCommand = {}
        for item in layerTemp.keys():
            counter = 1
            for key in layerTemp[item].keys():
                layer = f"layer{counter}"
                name = str(key).replace("\'", '\"')
                self.varAllLayerCommand[item].setdefault(layer, layerTemp[item][name])
                counter += 1
        counter = 1
        self.varLayerNumDict[layerName] -= 1
        self.allLayerNum -= 1
        for item in temp.keys():
            for key in temp[item].keys():
                self.varAllCommand.setdefault(counter, {str(key): [counter, temp[item][key][1]]})
            counter += 1
        # print(self.varAllLayerCommand)
        # print(self.varAllCommand)

    def _addLayer(self):
        self.modelName = str(self.modelNameEntry.get())
        self.layerChosen = str(self.layerChoiceCom.get())
        self.unitNum = str(self.unitNumEntry.get())
        self.layerActivation = str(self.layerActivationCom.get())
        func = getattr(self, self.layerChosen)
        func(self.layerChosen)

    def Conv2D(self, chosenLayer):
        command = self.varLayerChoiceInstallCmd[chosenLayer]
        try:
            filters = 0
            filters = int(self.unitNumEntry.get())
            if not filters == 0:
                command = command.replace("filters=", f"filters={filters}")
                command = command.replace("kernel_size=", f"kernel_size={self.layerKernelSizeCom.get()}")
                command = command.replace('activation=', f'activation=\"{self.layerActivationCom.get()}\"')
                try:
                    if self.allLayerNum == 0:
                        shape = str(self.inputShapeEntry.get())
                        if len(shape) == 0:
                            command = command.replace(", input_shape=", "")
                        else:
                            print(shape.find("("), shape.find(")"))
                            if "(" in shape and ")" in shape:
                                command = command.replace(", input_shape=", f", input_shape={shape}")
                            else:
                                command = command.replace(", input_shape=", "")
                    else:
                        command = command.replace(", input_shape=", "")
                    self.varConv2DNum += 1
                    self.allLayerNum += 1
                    self.listBox.insert(tk.END, command)
                    self.listBox.select_clear(self.lastSelected)
                    self.listBox.select_set(self.allLayerNum - 1)
                    self.lastSelected = self.allLayerNum - 1
                    self.varAllCommand.setdefault(self.allLayerNum, {chosenLayer: [self.varConv2DNum, command]})
                    self.varAllLayerCommand[chosenLayer].setdefault(f"layer{self.varConv2DNum}", command)
                    print(command)
                except ValueError:
                    print("[VALUE ERROR] input_shape is not a tuple type")
            else:
                print("[ERROR] filters cannot be zero!!!")
        except ValueError:
            print("[VALUE ERROR] filters is not a int type")

    def Dense(self, chosenLayer):
        command = self.varLayerChoiceInstallCmd[chosenLayer]
        try:
            units = 0
            units = int(self.unitNumEntry.get())
            if not units == 0:
                command = command.replace("units=", f"units={units}")
                command = command.replace('activation=', f'activation=\"{self.layerActivationCom.get()}\"')
                try:
                    if self.allLayerNum == 0:
                        shape = str(self.inputShapeEntry.get())
                        if len(shape) == 0:
                            command = command.replace(", input_shape=", "")
                        else:
                            print(shape.find("("), shape.find(")"))
                            if "(" in shape and ")" in shape:
                                command = command.replace(", input_shape=", f", input_shape={shape}")
                            else:
                                command = command.replace(", input_shape=", "")
                    else:
                        command = command.replace(", input_shape=", "")
                    self.varDenseNum += 1
                    self.allLayerNum += 1
                    self.listBox.insert(tk.END, command)
                    self.listBox.select_clear(self.lastSelected)
                    self.listBox.select_set(self.allLayerNum - 1)
                    self.lastSelected = self.allLayerNum - 1
                    self.varAllCommand.setdefault(self.allLayerNum, {chosenLayer: [self.varDenseNum, command]})
                    self.varAllLayerCommand[chosenLayer].setdefault(f"layer{self.varDenseNum}", command)
                    print(command)
                except ValueError:
                    print("[VALUE ERROR] input_shape is not a tuple type")
            else:
                print("[ERROR] units cannot be zero!!!")
        except ValueError:
            print("[VALUE ERROR] units is not a int type")

    def MaxPooling2D(self, chosenLayer):
        command = self.varLayerChoiceInstallCmd[chosenLayer]
        command = command.replace('pool_size=', f'pool_size={self.layerKernelSizeCom.get()}')
        self.allLayerNum += 1
        self.varMaxPooling2DNum += 1
        self.listBox.insert(tk.END, command)
        self.listBox.select_clear(self.lastSelected)
        self.listBox.select_set(self.allLayerNum - 1)
        self.lastSelected = self.allLayerNum - 1
        self.varAllCommand.setdefault(self.allLayerNum, {chosenLayer: [self.varMaxPooling2DNum, command]})
        self.varAllLayerCommand[chosenLayer].setdefault(f"layer{self.varMaxPooling2DNum}", command)
        print(command)

    def Flatten(self, chosenLayer):
        command = self.varLayerChoiceInstallCmd[chosenLayer]
        self.allLayerNum += 1
        self.varFlattenNum += 1
        self.listBox.insert(tk.END, command)
        self.listBox.select_clear(self.lastSelected)
        self.listBox.select_set(self.allLayerNum - 1)
        self.lastSelected = self.allLayerNum - 1
        self.varAllCommand.setdefault(self.allLayerNum, {chosenLayer: [self.varFlattenNum, command]})
        self.varAllLayerCommand[chosenLayer].setdefault(f"layer{self.varFlattenNum}", command)
        print(command)

    def Dropout(self, chosenLayer):
        command = self.varLayerChoiceInstallCmd[chosenLayer]
        try:
            rate = float(self.unitNumEntry.get())
            if 1 > rate > 0:
                command = command.replace("rate=", f"rate={rate}")
                self.allLayerNum += 1
                self.varDropoutNum += 1
                self.listBox.insert(tk.END, command)
                self.listBox.select_clear(self.lastSelected)
                self.listBox.select_set(self.allLayerNum - 1)
                self.lastSelected = self.allLayerNum - 1
                self.varAllCommand.setdefault(self.allLayerNum, {chosenLayer: [self.varDropoutNum, command]})
                self.varAllLayerCommand[chosenLayer].setdefault(f"layer{self.varDropoutNum}", command)
                print(command)
        except:
            print("[VALUE ERROR] rate is not a float type")

    def update(self):
        now = time.time()
        if now - self.preTime > 0.5:
            nameTemp = str(self.modelNameEntry.get())
            # print(nameTemp, self.initialCommand)
            if not self.modelName == nameTemp:
                self.modelName = nameTemp
                print("replace")
                self.initialCommand = self.initialCommand.replace(self.initialCommand[19: len(self.initialCommand) - 1],
                                                                  f'name=\"{self.modelName}\"')
            self.preTime = now

        layerName = str(self.layerChoiceCom.get())
        for key in self.varAllSize.keys():
            if layerName == key:
                self.allLabels[3].configure(text=self.varAllSize[layerName][0])
                self.layerKernelSizeCom.configure(values=self.varAllSize[layerName][1])
                break
        for key in self.varUnitNumRateNum.keys():
            if layerName == key:
                self.allLabels[2].configure(text=self.varUnitNumRateNum[layerName])
                break
        temp = self.varLayerAllTkObj.copy()
        for key in self.varLayerTypeNotUseTkObj.keys():
            if layerName == key:
                for obj in self.varLayerTypeNotUseTkObj[layerName]:
                    temp.remove(obj)
                    obj.configure(state=self.state[0])
                for obj in temp:
                    obj.configure(state=self.state[1])
                break
        self.window.after(100, self.update)

    def openFile(self):
        self.dirPath = fd.askdirectory()
        if not self.dirPath in self.varAllPath:
            self.varAllPath.append(self.dirPath)
            self.directoryCom.configure(values=self.varAllPath)
        self.directoryCom.current(self.varAllPath.index(self.dirPath))

    def _createAllEntry(self):
        self.modelNameEntry = tk.Entry(self.frameLabel1, font=("Consolas", 12), width=self.comboboxWidth + 2)
        self.modelNameEntry.place(x=200, y=30)
        self.unitNumEntry = tk.Entry(self.frameLabel1, font=("Consolas", 12), width=self.comboboxWidth + 2)
        self.unitNumEntry.place(x=200, y=90)
        self.inputShapeEntry = tk.Entry(self.frameLabel1, font=("Consolas", 12), width=self.comboboxWidth + 2)
        self.inputShapeEntry.place(x=200, y=180)

    def _createAllCombobox(self):
        self.layerChoiceCom = ttk.Combobox(self.frameLabel1, width=self.comboboxWidth,
                                           values=self.varModelLayerNames, font=("Consolas", 12))
        self.layerChoiceCom.place(x=self.comboboxPlaceX,
                                  y=self.comboboxStartY + self.comboboxMarginY * 1)
        self.layerKernelSizeCom = ttk.Combobox(self.frameLabel1, width=self.comboboxWidth,
                                               values=self.varLayerKernelSize, font=("Consolas", 12))
        self.layerKernelSizeCom.place(x=self.comboboxPlaceX,
                                      y=self.comboboxStartY + self.comboboxMarginY * 3)
        self.layerActivationCom = ttk.Combobox(self.frameLabel1, width=self.comboboxWidth,
                                               values=self.varModelActivations, font=("Consolas", 12))
        self.layerActivationCom.place(x=self.comboboxPlaceX,
                                      y=self.comboboxStartY + self.comboboxMarginY * 4)
        self.directoryCom = ttk.Combobox(self.frameLabel1, width=self.comboboxWidth,
                                         values=self.varAllPath, font=("Consolas", 12))
        self.directoryCom.place(x=self.comboboxPlaceX,
                                y=self.comboboxStartY + self.comboboxMarginY * 6)

    def runStart(self):
        self.window.mainloop()


if __name__ == "__main__":
    builder = ModuleUI()
    builder.runStart()

