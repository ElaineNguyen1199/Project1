from gui import *

def main():
    window = Tk()
    window.title("ATM")
    window.geometry('300x400')
    window.resizable(False, False)
    AccountGUI(window)
    window.mainloop()

if __name__ == '__main__':
    main()
