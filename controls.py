from tkinter import *
import random

class Slider:
    def __init__(self, parent, param):
        self.min_var = IntVar()
        self.max_var = IntVar()
        min_pos = min(param.options)
        max_pos = max(param.options)
        self.min_scale = Scale(parent,
                               variable=self.min_var,
                               length=150,
                               width=5,
                               from_=min_pos,
                               to=max_pos,
                               orient=HORIZONTAL,
                               command=lambda x:self.check_min())

        self.max_scale = Scale(parent,
                               variable=self.max_var,
                               length=150,
                               width=5,
                               from_=min_pos,
                               to=max_pos,
                               orient=HORIZONTAL,
                               command=lambda x:self.check_max())

        self.min_scale.pack(side=LEFT)
        self.max_scale.pack(side=RIGHT)
        parent.pack()
        self.min_var.set(min_pos)
        self.max_var.set(max_pos)
        self.param = param
        self.label = param.label

    def check_min(self):
        if self.max_var.get() < self.min_var.get():
            self.max_var.set(self.min_var.get())
        self.param.options = range(self.min_var.get(), self.max_var.get()+1)

    def check_max(self):
        if self.max_var.get() < self.min_var.get():
            self.min_var.set(self.max_var.get())
        self.param.options = range(self.min_var.get(), self.max_var.get()+1)


    def get_random(self):
        print('yes')
        return random.sample(range(self.min_var.get(), self.max_var.get()+1), 1)

class Check:
    def __init__(self, option, parent, text, bank, type):
        self.type = type
        self.bank = bank
        self.parent = parent
        self.var = IntVar()
        self.option = option
        self.box = Checkbutton(parent, variable=self.var, text=text, command=lambda:self.update())
        self.box.pack()
        self.var.set(1)

    def update(self):
        if self.type == 'o':
            o = self.bank.options
        elif self.type == 'h':
            o = self.bank.highnibbles
        elif self.type == 'l':
            o = self.bank.lownibbles

        if self.option in o:
            o.remove(self.option)
        else:
            o.append(self.option)
        if o == []:
            o.append(self.option)
            self.var.set(1)
        print(o)

class Checkbank:
    def __init__(self, parent, param, numrows):
        self.options = param.options
        self.numcols = round(len(param.options) / numrows) + 1
        self.highnibbles = param.highnibbles
        self.lownibbles = param.lownibbles
        self.bank = []
        self.param = param
        self.frame = Frame(parent, bd=2)
        self.columns = []
        for i in range(self.numcols):
            self.columns.append(Frame(parent))

        Label(self.frame, text=self.param.label).pack()

        self.frame.pack()
        [c.pack(side=LEFT) for c in self.columns]

        if not param.options == ['']:
            for o in param.options:
                self.addBox(Check(o, self.columns[int(self.options.index(o) / numrows)], self.param.checks[self.param.options.index(o)], self, 'o'))
        else:
            for h in param.highnibbles:
                self.addBox(Check(h, self.frame, self.param.highchecks[self.param.highnibbles.index(h)], self, 'h'))
            for l in param.lownibbles:
                self.addBox(Check(l, self.frame, self.param.lowchecks[self.param.lownibbles.index(l)], self, 'l'))

        parent.pack(side=LEFT, anchor=N, padx=10)

    def addBox(self, box):
        self.bank.append(box)

    def get_random(self):
        pass

    def update(self):
        pass
