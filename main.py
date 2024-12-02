from gui import *

def main() -> None:
    """
    Creates the main Tkinter window
    """
    window = Tk()
    window.title("ATM")
    window.geometry('300x500')
    window.resizable(False, False)
    AccountGUI(window)
    window.mainloop()

if __name__ == '__main__':
    main()
