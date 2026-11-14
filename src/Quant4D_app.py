import sys
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def main():
    """Entry point for the ``quant4d`` console script."""
    import PyQt5.QtWidgets as qtw
    from callbacks.guiClass import MainWindow

    app = qtw.QApplication(sys.argv)
    Quant4D_MainWindow = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
