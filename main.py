from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys
import random
import time
import threading
import data
import os

os.environ["QT_MAC_WANTS_LAYER"] = "1"


class SolveSudoku(threading.Thread):
    def __init__(self, m):
        threading.Thread.__init__(self)
        self.DH = []
        self.matrix = m
        self.old_row, self.old_col = None, None
        self.delay = 0.05

    def run(self):
        self.degreeCalculation()
        if self.Sudoku():
            print("Done!")
            p.matrix = self.matrix
            p.updateBoard()
            p.ui.progress_bar.setVisible(False)
        else:
            print("No solution exists")

    def degreeCalculation(self):
        for i in range(9):
            for j in range(9):
                cntr = 0
                if self.matrix[i][j] == 0:
                    for k in range(9):
                        if (self.matrix[i][k] == 0 and k != j) or (self.matrix[k][j] == 0 and k != i):
                            cntr += 1

                    for k in range((i // 3) * 3, ((i // 3) * 3) + 3):
                        for m in range((j // 3) * 3, ((j // 3) * 3) + 3):
                            if self.matrix[k][m] == 0 and k != i and m != j:
                                cntr += 1
                    
                    node = {'degree':cntr, 'row':i, 'col':j, 'isset':0}
                    self.DH.append(node)

        self.DH = sorted(self.DH, key=lambda k: k['degree'])

    def usedInRow(self, row, num):
        if all(self.matrix[row][col] != num for col in range(9)):
            return False
        return True

    def usedInCol(self, col, num):
        if all(self.matrix[row][col] != num for row in range(9)):
            return False
        return True

    def usedInBox(self, boxStartrow, boxStartcol, num):
        if all(self.matrix[row + boxStartrow][col + boxStartcol] != num for col in range(3) for row in range(3)):
            return False
        return True

    def isSafe(self, row, col, num):
        return not self.usedInRow(row, num) and not self.usedInCol(col, num) and \
               not self.usedInBox(row - row % 3, col - col % 3, num)

    def Heuristic(self):
        for node in self.DH:
            if node['isset'] == 0:
                row = node['row']
                col = node['col']
                return True, row, col
        return False, 0, 0

    def Set(self, row, col):
        this = next(item for item in self.DH if row == item['row'] and col == item['col'])
        this['isset'] = 1

        for node in self.DH:
            if this['row'] == node['row'] or this['col'] == node['col'] or (
                    this['row'] // 3 == node['row'] // 3 and this['col'] // 3 == node['col'] // 3):
                node['degree'] -= 1

        self.DH = sorted(self.DH, key=lambda k: k['degree'])

    def UnSet(self, row, col):
        this = next(item for item in self.DH if row == item['row'] and col == item['col'])
        this['isset'] = 0

        for node in self.DH:
            if this['row'] == node['row'] or this['col'] == node['col'] or (
                    this['row'] // 3 == node['row'] // 3 and this['col'] // 3 == node['col'] // 3):
                node['degree'] += 1

        self.DH = sorted(self.DH, key=lambda k: k['degree'])

    def Show(self, row, col, num):
        time.sleep(self.delay)
        if self.old_row != None and self.old_col != None:
            p.board[self.old_row][self.old_col].setStyleSheet('background-color: lightgreen')

        self.old_row, self.old_col = row, col
        p.board[row][col].setText(str(num))
        p.board[row][col].setStyleSheet("background-color: lightblue")
        time.sleep(self.delay)

    def Hide(self, row, col):
        p.board[row][col].setStyleSheet('none')
        p.board[row][col].setText('')
        time.sleep(self.delay)

    def Sudoku(self):
        if p.run:
            try:
                flag, row, col = self.Heuristic()

                if not flag:
                    return True

                for num in range(1, 10):
                    if self.isSafe(row, col, num) and p.run:

                        self.Set(row, col)
                        self.matrix[row][col] = num
                        if p.preview:
                            self.Show(row, col, num)

                        if self.Sudoku():
                            return True

                        self.UnSet(row, col)
                        self.matrix[row][col] = 0
                        if p.preview:
                            self.Hide(row, col)

                return False

            except:
                print('some problem')

        return True


class Program(QMainWindow):

    def __init__(self):
        super(Program, self).__init__()
        
        self.matrix = list()

        loader = QUiLoader()
        self.ui = loader.load('mainwindow.ui')

        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.preview = False
        self.ui.progress_bar.setVisible(False)

        for i in range(9):
            for j in range(9):
                self.board[i][j] = getattr(self.ui, f'tb_{i}{j}')

        self.ui.menu_new_game.triggered.connect(self.newGame)
        self.ui.menu_open.triggered.connect(self.openFile)
        self.ui.menu_exit.triggered.connect(exit)
        self.ui.menu_help_game.triggered.connect(self.help)
        self.ui.menu_about.triggered.connect(self.about)

        self.ui.btn_check.clicked.connect(self.check)
        self.ui.btn_new_game.clicked.connect(self.newGame)
        self.ui.btn_solve.clicked.connect(self.solve)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.ui.cb_preview.clicked.connect(self.setPreview)

        self.newGame()
        self.ui.show()

    def setPreview(self):
        self.preview = not self.preview

    def stop(self):
        self.run = False
        del self.solveSudoku

    def openFile(self):
        file_location = QFileDialog.getOpenFileName(self, caption="Open File", directory=".", filter="*.txt")[0]

        rows = open(file_location, 'r').read().split('\n')
        if len(rows) != 9:
            msgbox = QMessageBox()
            msgbox.setWindowTitle('Error')
            msgbox.setText('File is invalid')
            msgbox.exec_()
            return

        self.matrix = list()
        for row in rows:
            cells = row.split(' ')
            if len(cells) != 9 or any(cell not in ['0','1','2','3','4','5','6','7','8','9'] for cell in cells):
                msgbox = QMessageBox()
                msgbox.setWindowTitle('Error')
                msgbox.setText('File is invalid')
                msgbox.exec_()
                return
            self.matrix.append(cells)

        self.updateBoard()

    def help(self):
        msgbox = QMessageBox()
        msgbox.setText('To open the file, note the following:\n\n'
                       '1-File must contain 9 lines\n'
                       '2-There should be 9 digits in each line\n'
                       '3-Digits must be separated by space')

        msgbox.setWindowTitle('Help')
        msgbox.exec_()

    def about(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle('About')
        msgbox.setText('Sudoku v3.1\n\n'
                       'Programmer: Sajjad Aemmi\n'
                       'Email: sajjadaemmi@gmail.com')
        msgbox.exec_()

    def newGame(self):
        self.matrix = list()
        rows = random.choice(data.startMatrixs)

        for row in rows:
            cells = "".join(row).split(' ')
            self.matrix.append(cells)
        self.updateBoard()

    def solve(self):
        m = [[int(item) for item in row] for row in self.matrix]
        self.run = True
        self.ui.progress_bar.setVisible(True)
        self.solveSudoku = SolveSudoku(m)
        self.solveSudoku.start()

    def updateBoard(self):
        for i in range(9):
            for j in range(9):
                if str(self.matrix[i][j]) != '0':
                    self.board[i][j].setText(str(self.matrix[i][j]))
                    self.board[i][j].setStyleSheet('background-color: lightgray')
                    self.board[i][j].setReadOnly(True)
                else:
                    self.board[i][j].setText('')
                    self.board[i][j].setStyleSheet('none')
                    self.board[i][j].setReadOnly(False)

    def check(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == '0':
                    self.board[i][j].setStyleSheet('none')
                else:
                    self.board[i][j].setStyleSheet('background-color: lightgray')

        for k in range(9):
            for i in range(9):
                for j in range(9):
                    if self.board[k][i].text() == self.board[k][j].text() and i != j and self.board[k][i].text() != '':
                        self.board[k][i].setStyleSheet('background-color: pink')
                    if self.board[i][k].text() == self.board[j][k].text() and i != j and self.board[i][k].text() != '':
                        self.board[i][k].setStyleSheet('background-color: pink')

        for n in range(0, 9, 3):
            for m in range(0, 9, 3):
                for i in range(n, n + 3):
                    for j in range(m, m + 3):
                        for k in range(n, n + 3):
                            for l in range(m, m + 3):
                                if self.board[i][j].text() == self.board[k][l].text() and i != k and j != l and \
                                        self.board[i][j].text() != '':
                                    self.board[i][j].setStyleSheet('background-color: pink')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = Program()
    sys.exit(app.exec_())
