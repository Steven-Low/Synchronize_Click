import tkinter as tk
from PIL import ImageTk, Image


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("200x100")
        self.attributes("-alpha", 0.8)
        self.configure(bg='grey')
        self.title("Sync")
        # self.wm_attributes('-transparentcolor', 'grey')
        self.floater = FloatingWindow(self)

        button = tk.Button(self, text="click me!", command=self.click)  # do not pass () here !!!!!
        button.pack()

        # Create a label to prompt the user for input
        label = tk.Label(self, text="Enter an integer:")
        label.pack()

        # Create an Entry widget for the user to enter an integer
        vcmd = (self.register(self.validate), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")
        self.entry = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.entry.pack()

        # Create a button to submit the integer input
        button = tk.Button(self, text="Submit", command=self.submit)
        button.pack()

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        # Only allow integer input
        if text in "0123456789":
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                pass
        return False

    def submit(self):
        # Get the integer input from the Entry widget
        integer = int(self.entry.get())
        print("Input:", integer)

    def click(self):
        x = self.floater.winfo_x()
        y = self.floater.winfo_y()
        print("position x", x)  # print position
        print("position y", y)


class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.geometry(f"+{800}+{300}")

        # Create an object of tkinter ImageTk
        image = Image.open("image.png")
        resize = image.resize((128, 128))
        image = ImageTk.PhotoImage(resize)
        self.wm_attributes('-transparentcolor', 'grey')
        self.grip = tk.Label(self, image=image, bg='grey')
        self.grip.image = image
        self.grip.pack()

        # self.grip.pack(side="left", fill="y")
        # self.label.pack(side="right", fill="both", expand=True)

        self.grip.bind("<ButtonPress-1>", self.start_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_move)
        self.grip.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")


app = App()

app.mainloop()
