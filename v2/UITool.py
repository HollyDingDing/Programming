import tkinter as tk
import os
from tkinter import ttk
from modelBuilderUI import ModuleUI
import json


class CreateGUI:
    def __init__(self):
        self.maxWidth = 700
        self.maxHeight = 600
        self.state = ("disabled", "normal")
        self.allCode = ""
        self.boolState = False
        self.window = tk.Tk()
        self.window.title('Model Creator')
        self.window.geometry('{}x{}'.format(self.maxWidth, self.maxHeight))
        self.window.minsize(self.maxWidth, self.maxHeight)
        self.window.maxsize(self.maxWidth, self.maxHeight)

        self.div_size = 350
        self.count = 0
        self.img_size = self.div_size * 2

        self.div1 = tk.Frame(self.window, width=self.img_size, height=self.img_size, bg='blue')
        self.div1.grid(column=0, row=0, rowspan=2)
        # self.canvas = tk.Canvas(self.div1, width=self.img_size, height=self.img_size, bg="blue")
        # self.canvas.pack()
        # self.scrollBar = tk.Scrollbar(self.div1, command=self.div1.yview)
        # self.scrollBar.pack(side="right", fill="y")
        self.labelPlaceX = 40
        self.labelStartY = 39
        self.labelMarginY = 40
        self.comboboxPlaceX = 360
        self.comboboxStartY = 40
        self.comboboxMarginY = 40
        self.installObjPlaceX = (200, 270)

        self.pythonVersion = ""
        self._createAllLabels()
        self._createCombobox()
        self.update()
        self.installTensorflow = f"python{self.pythonVersion} -m pip install tensorflow=="
        self.installMatplotlib = f"python{self.pythonVersion} -m pip install matplotlib=="
        self.installOpencv = f"python{self.pythonVersion} -m pip install opencv-python=="
        self.allInstallCmdMember = [
            [self.installTensorflow, self.tensorflowCombobox, self.varTf],
            [self.installMatplotlib, self.matplotlibCombobox, self.varMTL],
            [self.installOpencv, self.opencvCombobox, self.varOPCV]
        ]
        self.allInstallCmd = ""
        self.runCmdResult = ""
        self._createBuildBtn()
        self._createInstallBtn()
        self._createCheckBtn()
        # self.runStart()

    def _createAllLabels(self):
        tk.Label(self.window, text="Python Version", font=('Consolas', 12)).place(x=self.labelPlaceX,
                                                                                  y=self.labelStartY + self.labelMarginY * 0)
        tk.Label(self.window, text="Install Tf", font=('Consolas', 12)).place(x=self.labelPlaceX,
                                                                              y=self.labelStartY + self.labelMarginY * 1)
        tk.Label(self.window, text="Install MPL", font=('Consolas', 12)).place(x=self.labelPlaceX,
                                                                               y=self.labelStartY + self.labelMarginY * 2)
        tk.Label(self.window, text="Install Opencv", font=('Consolas', 12)).place(x=self.labelPlaceX,
                                                                                  y=self.labelStartY + self.labelMarginY * 3)

    def _createBuildBtn(self):
        self.buildBtn = tk.Button(self.window, text="Build", width=10, height=1,
                                  font=("Consolas", 10), command=self.buildFunc)
        self.buildBtn.place(x=600, y=460)

    def buildFunc(self):
        self.builder = ModuleUI()
        self.builder.runStart()

    def _createCheckBtn(self):
        self.checkBtn = tk.Button(self.window, text="Check Result", width=15, height=1,
                                  font=("Consolas", 10), command=self._checkResult)
        self.boolState = False
        self.checkBtn.configure(state=self.state[int(self.boolState)])
        self.checkBtn.place(x=580, y=540)

    def _checkResult(self):
        self.checkWindow = tk.Toplevel(self.window)
        self.checkWindow.title('Command Result')
        self.checkWindow.geometry('{}x{}'.format(int(self.maxWidth*1.5), int(self.maxHeight*1.5)))
        self.checkWindow.minsize(int(self.maxWidth*1.5), int(self.maxHeight*1.5))
        self.checkWindow.maxsize(int(self.maxWidth*1.5), int(self.maxHeight*1.5))
        self.chk_div_size = int(350*1.5)
        self.chk_img_size = self.chk_div_size * 2
        self.chk_div = tk.Frame(self.checkWindow, width=self.chk_img_size, height=self.chk_img_size, bg='black')
        self.chk_div.grid(column=0, row=0, rowspan=2)
        tk.Label(self.checkWindow, text="Result", font=("Consolas", 12)).place(x=40, y=40)
        # self.allResult = tk.Listbox(self.checkWindow)
        # self.allResult.config(font=('Consolas', 12), width=30)
        # self.allResult.insert(tk.END, self.runCmdResult)
        # self.allResult.place(x=40, y=70)
        self.allResult = tk.Text(self.checkWindow, width=107, height=30, font=("Consolas", 12))
        self.allResult.insert(1.0, self.runCmdResult)
        self.allResult.place(x=40, y=70)

    def _createInstallBtn(self):
        self.installBtn = tk.Button(self.window, text="Install", width=10, height=1,
                                    font=("Consolas", 10), command=self._installCommand)
        self.installBtn.place(x=600, y=500)

    def _installCommand(self):
        self.boolState = True
        self.checkBtn.configure(state=self.state[int(self.boolState)])
        self.allInstallCmd = ""
        for install in self.allInstallCmdMember:
            isInstall = bool(install[2].get())
            if isInstall:
                installVersion = str(install[1].get())
                installCmd = f"{install[0]}{installVersion}\n"
                self.allInstallCmd += installCmd
        with open("runInstall.sh", "w") as f:
            f.write(self.allInstallCmd)
        output = os.popen("sh ./runInstall.sh")
        self.runCmdResult = output.read()
        with open("runCmdResult.txt", "w") as f:
            f.write(self.runCmdResult)

    def _createCombobox(self):
        self.varPythonVersion = tk.IntVar()
        self.varPythonVersion.set(3)
        self.pythonVersionCombobox = ttk.Combobox(self.window,
                                                  values=
                                                  [
                                                      "",
                                                      "3",
                                                  ],
                                                  font=("Consolas", 12))
        self.pythonVersionCombobox.current(1)
        self.pythonVersionCombobox.place(x=self.comboboxPlaceX, y=self.comboboxStartY)
        self.varTf = tk.BooleanVar()
        self.varTf.set(True)
        self.installTf1 = tk.Radiobutton(self.window, text='True', font=('Consolas', 10),
                                     variable=self.varTf, value='True')
        self.installTf1.place(x=self.installObjPlaceX[0], y=self.comboboxStartY + self.comboboxMarginY * 1)
        self.installTf2 = tk.Radiobutton(self.window, text='False', font=('Consolas', 10),
                                        variable=self.varTf, value='False')
        self.installTf2.place(x=self.installObjPlaceX[1], y=self.comboboxStartY + self.comboboxMarginY * 1)
        self.installTf1.select()
        self.tensorflowCombobox = ttk.Combobox(self.window,
                                               values=
                                               [
                                                   "2.8.0",
                                                   "2.7.0",
                                                   "2.6.0",
                                                   "2.5.0",
                                                   "2.4.1",
                                                   "2.4.0",
                                                   "2.3.0",
                                                   "2.2.0",
                                                   "2.1.0",
                                                   "1.15.5"
                                               ],
                                               font=("Consolas", 12))
        self.tensorflowCombobox.current(0)
        self.tensorflowCombobox.place(x=self.comboboxPlaceX, y=self.comboboxStartY + self.comboboxMarginY * 1)

        self.varMTL = tk.BooleanVar()
        self.varMTL.set(True)
        self.installMTL1 = tk.Radiobutton(self.window, text='True', font=('Consolas', 10),
                                         variable=self.varMTL, value='True')
        self.installMTL1.place(x=self.installObjPlaceX[0], y=self.comboboxStartY + self.comboboxMarginY * 2)
        self.installMTL2 = tk.Radiobutton(self.window, text='False', font=('Consolas', 10),
                                         variable=self.varMTL, value='False')
        self.installMTL2.place(x=self.installObjPlaceX[1], y=self.comboboxStartY + self.comboboxMarginY * 2)
        self.installMTL1.select()
        self.matplotlibCombobox = ttk.Combobox(self.window,
                                               values=
                                               [
                                                   "3.5.0",
                                                   "3.4.0",
                                                   "3.3.0",
                                                   "3.2.0",
                                                   "3.1.0",
                                                   "3.0.0",
                                                   "2.2.0",
                                                   "2.1.0"
                                               ],
                                               font=("Consolas", 12))
        self.matplotlibCombobox.current(0)
        self.matplotlibCombobox.place(x=self.comboboxPlaceX, y=self.comboboxStartY + self.comboboxMarginY * 2)

        self.varOPCV = tk.BooleanVar()
        self.varOPCV.set(True)
        self.installOPCV1 = tk.Radiobutton(self.window, text='True', font=('Consolas', 10),
                                          variable=self.varOPCV, value='True')
        self.installOPCV1.place(x=self.installObjPlaceX[0], y=self.comboboxStartY + self.comboboxMarginY * 3)
        self.installOPCV2 = tk.Radiobutton(self.window, text='False', font=('Consolas', 10),
                                          variable=self.varOPCV, value='False')
        self.installOPCV2.place(x=self.installObjPlaceX[1], y=self.comboboxStartY + self.comboboxMarginY * 3)
        self.installOPCV1.select()
        self.opencvCombobox = ttk.Combobox(self.window,
                                           values=
                                           [
                                               "4.5.5.62",
                                               "4.5.3.56",
                                               "4.5.2.54",
                                               "4.5.1.48",
                                               "4.4.0.46",
                                               "3.4.11.45"
                                           ],
                                           font=("Consolas", 12))
        self.opencvCombobox.current(0)
        self.opencvCombobox.place(x=self.comboboxPlaceX, y=self.comboboxStartY + self.comboboxMarginY * 3)

    def update(self):
        temp = self.pythonVersionCombobox.get()
        if not self.pythonVersion == temp:
            self.pythonVersion = temp
            self.installTensorflow = f"python{self.pythonVersion} -m pip install tensorflow=="
            self.installMatplotlib = f"python{self.pythonVersion} -m pip install matplotlib=="
            self.installOpencv = f"python{self.pythonVersion}"
            self.allInstallCmdMember = [
                [self.installTensorflow, self.tensorflowCombobox, self.varTf],
                [self.installMatplotlib, self.matplotlibCombobox, self.varMTL]
            ]
        self.window.after(1000, self.update)

    def runStart(self):
        self.window.mainloop()


def main():
    gui = CreateGUI()
    gui.runStart()
    # gui.defaultGUI()
    # print(gui.varVideo.get(), gui.varModel.get(), gui.varDebug.get())


if __name__ == "__main__":
    main()


