import tkinter as tk
from gui import Application

def main():
    root = tk.Tk()
    root.title("Face Recognition Training GUI")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()