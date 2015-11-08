import tkinter as tk
from loader_sim import *#interactive_parse, Stack

fileHandle = open("loader.c", "r")
loaderc = fileHandle.read()
fileHandle.close()

loaderc_lines = loaderc.split('\n')
#loaderc_d = '\n'.join(loaderc_lines[:8] + ['...'] + loaderc_lines[38:-3])
loaderc_d = '\n'.join(loaderc_lines[39:-4])

class LoaderGUI:
    def __init__(self, parent):
        self.parent = parent
        self.panes = tk.Frame(parent)
        self.panes.pack()

        self.mainFrame = tk.Frame(self.panes)
        self.mainFrame.pack(side=tk.LEFT)
        seperator = tk.Frame(self.panes, width=2,  bd=1, relief=tk.SUNKEN);
        seperator.pack(side=tk.LEFT, fill=tk.Y, padx=2)
        self.program = LineFocus(self.panes, 5, text=loaderc_d)
        self.program.pack(side=tk.LEFT)
        #self.program.line_configure(3, foreground='red')
        seperator = tk.Frame(self.panes, width=2,  bd=1, relief=tk.SUNKEN);
        seperator.pack(side=tk.LEFT, fill=tk.Y, padx=2)
        self.stackSpace = tk.Frame(self.panes)
        self.stackSpace.pack(side=tk.LEFT)

        self.bin = ""
        self.binLabel = tk.Label(self.mainFrame, text=self.bin,
            justify=tk.RIGHT, anchor=tk.E)
        self.binLabel.pack(side=tk.TOP)

        self.buttonFrame = tk.Frame(self.mainFrame)
        self.buttonFrame.pack(side=tk.TOP)
        self.b0 = tk.Button(self.buttonFrame, command=self.p0, text="0")
        self.b0.pack(side=tk.LEFT)
        self.b1 = tk.Button(self.buttonFrame, command=self.p1, text="1")
        self.b1.pack(side=tk.LEFT)
        self.quit = tk.Button(self.buttonFrame, command=self.mainFrame.quit,
            text="Quit")
        self.quit.pack(side=tk.LEFT)

        self.logtext = "TEST\n"
        self.logBox = tk.Label(self.mainFrame, text=self.logtext)
        #self.logBox.pack(side=tk.TOP)

        self.state = tk.Label(self.mainFrame, text='')
        self.state.pack(side=tk.TOP)
        self.stack = GUIStack(self.stackSpace)
        self.backend = interactive_parse(self.stack, None, self.log)
        self.state.configure(text=next(self.backend))

    def p0(self):
        self.bin = "0" + self.bin
        self.labelUpdate()
        self.program.set_focus(self.program.focus - 1)
        self.state.configure(text=self.backend.send(False))
        self.more()

    def p1(self):
        self.bin = "1" + self.bin
        self.labelUpdate()
        self.program.set_focus(self.program.focus + 1)
        self.state.configure(text=self.backend.send(True))
        self.more()

    def more(self):
        t = self.stack.top()
        self.log("({}) {}".format(len(self.stack.list), test_show(t.ctx, t.typ,
            t.term)))
        self.stack.update()

    def labelUpdate(self):
        self.binLabel.configure(text=self.bin)
    
    def log(self, out):
        self.logtext += out + "\n"
        self.logBox.configure(text=self.logtext)
        print(out)

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
        #assert focus >= 0
        prev_focus = self.focus
        if prev_focus == focus:
            return
        else:
            self.line_configure(prev_focus, foreground='black')
            self.line_configure(focus, foreground='red')
            self.focus = focus

class GUIStack(Stack):
    def __init__(self, parent):
        Stack.__init__(self)
        self.parent = parent
        self.label = tk.Label(self.parent)
        self.label.pack(side=tk.TOP)
        self.update()

    def do_and_update(func):
        def new_func(self, *arg, **key):
            res = func(self, *arg, **key)
            self.update()
            return res
        return new_func
    
    push = do_and_update(Stack.push)
    pop = do_and_update(Stack.pop)

    def update(self):
        objs = []
        for t in self:
            objs.append(test_show(t.ctx, t.typ, t.term))
        txt = '\n'.join(objs)
        self.label.configure(text=txt)

if __name__ == "__main__":
    root = tk.Tk()
    loadergui = LoaderGUI(root)
    root.mainloop()
