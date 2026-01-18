import sys
from PyQt5.QtWidgets import QApplication
from oknoSymulacja import symulacja

def main():
    app = QApplication(sys.argv)
    window = symulacja()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()