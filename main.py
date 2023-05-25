# Import tkinter library
from tkinter import *
import sys
import Scanner.theScanner as sc
import customtkinter
customtkinter.set_appearance_mode("dark-blue")
customtkinter.set_default_color_theme("dark-blue")
from PyQt5 import QtCore, QtWidgets,QtWebEngineWidgets
import Parser.parser as pr
import os
from animation.vid import animate
import tkinter as tk


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

        self.textwidget.update_idletasks()

        # Add the following line to update the widget and redraw the line numbers
        self.textwidget.update()
        self.textwidget.update_idletasks()



class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.configure(background='#f8f9fa')
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

    def getText(self):
        return self.text.get("1.0","end-1c")


class Ui_Dialog(object):
  def setupUi(self, Dialog):
    Dialog.setObjectName("Dialog")
    Dialog.resize(2000, 1000)
    self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
    self.verticalLayout.setObjectName("verticalLayout")
    self.centralwidget = QtWidgets.QWidget(Dialog)
    self.centralwidget.setObjectName("centralwidget")
    self.webEngineView =QtWebEngineWidgets.QWebEngineView(self.centralwidget)
    self.webEngineView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'\basic.html'))
    self.verticalLayout.addWidget(self.webEngineView)
    self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName("buttonBox")
    self.verticalLayout.addWidget(self.buttonBox)
    self.retranslateUi(Dialog)
    self.buttonBox.accepted.connect(Dialog.accept)
    self.buttonBox.rejected.connect(Dialog.reject)
    QtCore.QMetaObject.connectSlotsByName(Dialog)
  def retranslateUi(self, Dialog):
    _translate = QtCore.QCoreApplication.translate
    Dialog.setWindowTitle(_translate("Dialog", "Dialog"))



# Define a new function to open the window
def scanner():
    text = myText.getText()
    sc.rootScan(text)




# Retrieve the input from the text field
def retrieve_input():
    text = myText.getText()
    pr.rootScan(text)



def show_html():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec()




if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("700x750")
    frame = customtkinter.CTkFrame(master=root);

    frame.pack(pady=20, padx=60, fill="both", expand=True);
    label = customtkinter.CTkLabel(master=frame, text="Compiler Project", font=(("Montserrat"), 23))
    label.pack(pady=12, padx=10)

    myText = Example(frame)
    myText.pack(side="top", fill="both", expand=True)

    scanner = customtkinter.CTkButton(master=frame, text="Scan The Tokens", command=scanner);
    scanner.pack(pady=12, padx=10)

    parser = customtkinter.CTkButton(master=frame, text="parser", command=retrieve_input, state=NORMAL);
    parser.pack(pady=12, padx=10)

    showVideo = customtkinter.CTkButton(master=frame, text="show Animation", command=animate, state=NORMAL);
    showVideo.pack(pady=12, padx=10)


    dfa = customtkinter.CTkButton(master=frame, text="Generate Dfa", command=show_html);
    dfa.pack(pady=12, padx=10)

    root.mainloop();


