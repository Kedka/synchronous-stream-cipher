import sys
import itertools
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_seed = QtWidgets.QLabel(self.centralwidget)
        self.label_seed.setGeometry(QtCore.QRect(10, 10, 75, 25))
        self.label_seed.setObjectName("label_seed")

        self.line_edit_seed = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_seed.setGeometry(QtCore.QRect(10, 35, 75, 23))
        self.line_edit_seed.setObjectName("line_edit_seed")

        self.line_edit_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_filename.setGeometry(QtCore.QRect(50, 105, 100, 23))
        self.line_edit_filename.setObjectName("line_edit_filename")

        self.label_func = QtWidgets.QLabel(self.centralwidget)
        self.label_func.setGeometry(QtCore.QRect(100, 10, 75, 25))
        self.label_func.setObjectName("label_func")

        self.line_edit_func = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_func.setGeometry(QtCore.QRect(100, 35, 75, 23))
        self.line_edit_func.setObjectName("line_edit_func")

        self.pushButton_cipher = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cipher.setGeometry(55, 70, 90, 25)
        self.pushButton_cipher.setObjectName("cipher")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton_cipher.clicked.connect(self.cipher)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_seed.setText(_translate("MainWindow", "Seed:"))
        self.label_func.setText(_translate("MainWindow", "Function:"))

        self.line_edit_seed.setText(_translate("MainWindow", "101"))
        self.line_edit_func.setText(_translate("MainWindow", "110"))
        self.line_edit_filename.setText(_translate("MainWindow", "filename.extension"))

        self.pushButton_cipher.setText(_translate("MainWindow", "Cipher/Decipher"))

    def cipher(self):

        seed = list(self.line_edit_seed.text())
        seed_arr = [int(s) for s in seed]
        func = list(self.line_edit_func.text())
        func_arr = [int(s) for s in func]

        filename = self.line_edit_filename.text()

        with open(filename, "rb") as binaryfile:
                input_arr = bytearray(binaryfile.read())

        output_arr = []

        for i in input_arr:
            
            input_binary = [int(x) for x in list('{0:08b}'.format(i))]

            output_bin = []

            for b in input_binary:
                first = True
                for j in range(len(func_arr)):
                    if func_arr[j] == 1:
                        if first == True:
                            z = seed_arr[j]
                            first = False
                        else:
                            z ^= seed_arr[j]
                output_bin.append(z ^ b)
                seed_arr.insert(0, z)
                del seed_arr[-1]
            array2bin_output = ''.join(map(str, output_bin))

            hexed_output = hex(int(array2bin_output, 2))

            output_arr.append(hexed_output[2:])

        for i in range(len(output_arr)):
            if len(output_arr[i]) < 2:
                output_arr[i] = '0'+output_arr[i]

        output_file = open("output.bin", "wb")
        for i in output_arr:
            output_file.write(bytearray.fromhex(i))

        print("Job done maestro")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())