import tkinter as tk

fileHandle = open("loader.c", "r")
loaderc = fileHandle.read()
fileHandle.close()

loaderc_lines = loaderc.split('\n')
loaderc_d = '\n'.join(loaderc_lines[:8] + ['...'] + loaderc_lines[38:-3])

class LoaderGUI:
    def __init__(self, parent):
        self.parent = parent
        self.panes = tk.Frame(parent)
        self.panes.pack()
        self.topFrame = tk.Frame(self.panes)
        self.topFrame.pack(side=tk.LEFT)
        seperator = tk.Frame(self.panes, width=2,  bd=1, relief=tk.SUNKEN);
        seperator.pack(side=tk.LEFT, fill=tk.Y, padx=2)
        self.program = LineFocus(self.panes, 5, text=loaderc_d)
        self.program.pack(side=tk.LEFT)
        #self.program.line_configure(3, foreground='red')
        self.bin = ""
        self.binLabel = tk.Label(self.topFrame, text=self.bin, justify=tk.RIGHT,
            anchor=tk.E)
        self.binLabel.pack(side=tk.TOP)
        self.buttonFrame = tk.Frame(self.topFrame)
        self.buttonFrame.pack(side=tk.TOP)
        self.b0 = tk.Button(self.buttonFrame, command=self.p0, text="0")
        self.b0.pack(side=tk.LEFT)
        self.b1 = tk.Button(self.buttonFrame, command=self.p1, text="1")
        self.b1.pack(side=tk.LEFT)
        self.quit = tk.Button(self.buttonFrame, command=self.topFrame.quit,
            text="Quit")
        self.quit.pack(side=tk.LEFT)

    def p0(self):
        self.bin = "0" + self.bin
        self.labelUpdate()
        self.program.set_focus(self.program.focus - 1)

    def p1(self):
        self.bin = "1" + self.bin
        self.labelUpdate()
        self.program.set_focus(self.program.focus + 1)

    def labelUpdate(self):
        self.binLabel.configure(text=self.bin)

class TextLines:
    def __init__(self, parent, text=''):
        self.parent = parent
        self.text = text

        self.frame = tk.Frame(self.parent)
        self.lines = []
        for l in self.text.split('\n'):
            line = tk.Label(self.frame, text=l, anchor=tk.E)
            line.pack(side=tk.TOP, anchor=tk.W)
            self.lines.append(line)

    def pack(self, *arg, **kw):
        self.frame.pack(*arg, **kw)

    def line_configure(self, ln, **kw):
        self.lines[ln].configure(**kw)

class LineFocus(TextLines):
    def __init__(self, parent, focus, *arg, **kw):
        TextLines.__init__(self, parent, *arg, **kw)
        self.focus = focus
        self.line_configure(focus, foreground='red')

    def set_focus(self, focus):
        assert focus >= 0
        prev_focus = self.focus
        if prev_focus == focus:
            return
        else:
            self.line_configure(prev_focus, foreground='black')
            self.line_configure(focus, foreground='red')
            self.focus = focus

if __name__ == "__main__":
    root = tk.Tk()
    loadergui = LoaderGUI(root)
    root.mainloop()
