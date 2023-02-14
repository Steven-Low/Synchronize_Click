import tkinter as tk
from PIL import ImageTk, Image
import time
from datetime import datetime
import pyautogui


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
        label = tk.Label(self, text="Enter a time (hh:mm:ss):")
        label.pack()

        self.entry = tk.Entry()
        self.entry.pack()

        # Create a button to submit the integer input
        button = tk.Button(self, text="Submit", command=self.submit)
        button.pack()

        self.delay = 0

    def submit(self):
        now = datetime.now()
        # Get the time input from the Entry widget
        try:
            time_str = str(self.entry.get())
            time_tuple = time.strptime(time_str, "%H:%M:%S")
            time_tuple = (now.year,now.month, now.day) + time_tuple[3:]
            future = time.mktime(time_tuple)
            delay = abs(future - time.time())
            print("delay: ",delay, int(delay*1000) )
            self.after(int(delay*1000),self.click)

        except ValueError:
            pass

    def click(self):
        x = self.floater.winfo_x() + 7
        y = self.floater.winfo_y() + 7

        print("position x", x)  # print position
        print("position y", y)
        (xp, yp) = pyautogui.position()
        pyautogui.click(x,y)
        pyautogui.moveTo(xp,yp)


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
