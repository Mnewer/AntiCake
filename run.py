import tkinter as tk
from gui import Application

def main():
    root = tk.Tk()
    root.title("Facial Recognition Managment")  # Add window title
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()