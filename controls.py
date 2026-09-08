from tkinter import *
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """A vertically scrollable container. Add widgets to `.body` instead of `self`."""

    def __init__(self, parent):
        super().__init__(parent)
        canvas = Canvas(self, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.body = ttk.Frame(canvas)
        window = canvas.create_window((0, 0), window=self.body, anchor=N + W)

        def on_body_configure(event):
            canvas.configure(scrollregion=canvas.bbox(ALL))

        def on_canvas_configure(event):
            canvas.itemconfigure(window, width=event.width)

        self.body.bind('<Configure>', on_body_configure)
        canvas.bind('<Configure>', on_canvas_configure)

        def on_mousewheel(event):
            delta = event.delta if event.delta else (120 if event.num == 4 else -120)
            canvas.yview_scroll(int(-delta / 120), UNITS)

        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', on_mousewheel))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))
        canvas.bind('<Enter>', lambda e: (canvas.bind_all('<Button-4>', on_mousewheel),
                                           canvas.bind_all('<Button-5>', on_mousewheel)), add='+')


class Slider:
    def __init__(self, parent, param):
        self.param = param
        self.label = param.label
        min_pos = min(param.options)
        max_pos = max(param.options)

        frame = ttk.LabelFrame(parent, text=param.label, padding=(8, 4))
        frame.pack(fill=X, padx=6, pady=4)
        frame.columnconfigure(1, weight=1)

        self.min_var = IntVar(value=min_pos)
        self.max_var = IntVar(value=max_pos)

        ttk.Label(frame, text='Min').grid(row=0, column=0, sticky=W)
        self.min_scale = Scale(frame, variable=self.min_var, length=180, width=10,
                                from_=min_pos, to=max_pos, orient=HORIZONTAL,
                                showvalue=1, resolution=1, command=lambda x: self.check_min())
        self.min_scale.grid(row=0, column=1, sticky=EW, padx=6)

        ttk.Label(frame, text='Max').grid(row=1, column=0, sticky=W)
        self.max_scale = Scale(frame, variable=self.max_var, length=180, width=10,
                                from_=min_pos, to=max_pos, orient=HORIZONTAL,
                                showvalue=1, resolution=1, command=lambda x: self.check_max())
        self.max_scale.grid(row=1, column=1, sticky=EW, padx=6)

        self.param.options = range(min_pos, max_pos + 1)

    def check_min(self):
        if self.max_var.get() < self.min_var.get():
            self.max_var.set(self.min_var.get())
        self.param.options = range(self.min_var.get(), self.max_var.get() + 1)

    def check_max(self):
        if self.max_var.get() < self.min_var.get():
            self.min_var.set(self.max_var.get())
        self.param.options = range(self.min_var.get(), self.max_var.get() + 1)


class Check:
    def __init__(self, option, parent, text, bank, type):
        self.type = type
        self.bank = bank
        self.parent = parent
        self.var = IntVar(value=1)
        self.option = option
        self.box = ttk.Checkbutton(parent, variable=self.var, text=text, command=lambda: self.toggle())
        self.box.pack(anchor=W)

    def _options_list(self):
        if self.type == 'o':
            return self.bank.options
        elif self.type == 'h':
            return self.bank.highnibbles
        else:
            return self.bank.lownibbles

    def toggle(self):
        self.set_checked(bool(self.var.get()))

    def set_checked(self, checked):
        o = self._options_list()
        if checked:
            if self.option not in o:
                o.append(self.option)
            self.var.set(1)
        else:
            if self.option in o:
                o.remove(self.option)
            self.var.set(0)


class Checkbank:
    def __init__(self, parent, param, numrows):
        self.options = param.options
        self.numcols = round(len(param.options) / numrows) + 1
        self.highnibbles = param.highnibbles
        self.lownibbles = param.lownibbles
        self.bank = []
        self.param = param
        self.frame = ttk.LabelFrame(parent, text=param.label, padding=(8, 4))
        self.columns = []

        header = ttk.Frame(self.frame)
        header.pack(fill=X, pady=(0, 4))
        ttk.Button(header, text='All', width=6, command=self.select_all).pack(side=LEFT, padx=(0, 4))
        ttk.Button(header, text='None', width=6, command=self.select_none).pack(side=LEFT)

        columns_row = ttk.Frame(self.frame)
        columns_row.pack(fill=X)
        for i in range(self.numcols):
            self.columns.append(ttk.Frame(columns_row))

        [c.pack(side=LEFT, anchor=N, padx=4) for c in self.columns]

        if not param.options == ['']:
            for o in param.options:
                self.addBox(Check(o, self.columns[int(self.options.index(o) / numrows)],
                                   self.param.checks[self.param.options.index(o)], self, 'o'))
        else:
            for h in param.highnibbles:
                self.addBox(Check(h, self.frame, self.param.highchecks[self.param.highnibbles.index(h)], self, 'h'))
            for l in param.lownibbles:
                self.addBox(Check(l, self.frame, self.param.lowchecks[self.param.lownibbles.index(l)], self, 'l'))

        self.frame.pack(fill=X, padx=6, pady=4, anchor=N)

    def addBox(self, box):
        self.bank.append(box)

    def select_all(self):
        for box in self.bank:
            box.set_checked(True)

    def select_none(self):
        for box in self.bank:
            box.set_checked(False)
        # At least one option must stay selected so randomize() never
        # has to choose from an empty pool.
        if self.bank:
            self.bank[0].set_checked(True)
