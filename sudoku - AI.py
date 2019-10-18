from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import random
import time
import threading
import data


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
                    node = dict()
                    node['degree'] = cntr
                    node['row'] = i
                    node['col'] = j
                    node['isset'] = 0
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
        return not self.usedInRow(row, num) and \
               not self.usedInCol(col, num) and \
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
            p.board[self.old_row][self.old_col].setStyleSheet('none')

        time.sleep(self.delay)
        self.old_row, self.old_col = row, col
        time.sleep(self.delay)
        p.board[row][col].setText(str(num))
        time.sleep(self.delay)
        p.board[row][col].setStyleSheet("background-color: lightblue")
        time.sleep(self.delay)

    def Hide(self, row, col):
        time.sleep(self.delay)
        p.board[row][col].setStyleSheet('none')
        time.sleep(self.delay)
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
                        self.Show(row, col, num)

                        if self.Sudoku():
                            return True

                        self.UnSet(row, col)
                        self.matrix[row][col] = 0
                        self.Hide(row, col)

                return False

            except:
                print('some problem')

        return True
    
class Program(QWidget):

    def __init__(self):
        super().__init__()
        self.matrix = list()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('Sudoku')
        self.createUI()
        self.newGame()
        self.show()

    def createUI(self):
        vLayout = QVBoxLayout(self)

        #region Menu
        mainMenu = QMenuBar(self)
        vLayout.addWidget(mainMenu)

        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        menu_btn_new_game = QAction('New Game', self)
        menu_btn_new_game.triggered.connect(self.newGame)
        fileMenu.addAction(menu_btn_new_game)

        menu_btn_open_file = QAction('Open File', self)
        menu_btn_open_file.triggered.connect(self.openFile)
        fileMenu.addAction(menu_btn_open_file)

        menu_btn_exit = QAction('Exit', self)
        menu_btn_exit.triggered.connect(self.close)
        fileMenu.addAction(menu_btn_exit)

        menu_btn_help = QAction('Help', self)
        menu_btn_help.triggered.connect(self.help)
        helpMenu.addAction(menu_btn_help)

        menu_btn_about = QAction('About', self)
        menu_btn_about.triggered.connect(self.about)
        helpMenu.addAction(menu_btn_about)
        # endregion

        #region Board
        gLayout = QGridLayout()
        gLayout.setSpacing(0)
        vLayout.addLayout(gLayout)
        myfont = QFont('Arial', 20)

        self.parts = [[QGroupBox() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.parts[i][j].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                self.parts[i][j].setStyleSheet("QGroupBox::title { "
                                               "border: 0px ; "
                                               "border-radius: 0px; "
                                               "padding: 0px 0px 0px 0px; "
                                               "margin = 0px 0px 0px 0px } "
                                               "QGroupBox { "
                                               "margin = 0px 0px 0px 0px; "
                                               "border: 0px ; "
                                               "border-radius: 0px; "
                                               "padding: 0px 0px 0px 0px;} ")
                gLayout.addWidget(self.parts[i][j], i, j)

        self.board = [[QLineEdit() for _ in range(9)] for _ in range(9)]

        for row in range(3):
            for col in range(3):
                gLayout = QGridLayout()
                self.parts[row][col].setLayout(gLayout)

                for i in range(row * 3, row * 3 + 3):
                    for j in range(col * 3, col * 3 + 3):
                        self.board[i][j].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                        self.board[i][j].setAlignment(Qt.AlignCenter)
                        self.board[i][j].setFont(myfont)

                        gLayout.addWidget(self.board[i][j], i, j)
        # endregion

        # region Buttons
        btn_group = QGroupBox()
        btn_group.setStyleSheet("QGroupBox::title { "
                                "border: 0px ; "
                                "border-radius: 0px; "
                                "padding: 0px 0px 0px 0px; "
                                "margin = 0px 0px 0px 0px } "
                                "QGroupBox { "
                                "margin = 0px 0px 0px 0px; "
                                "border: 0px ; "
                                "border-radius: 0px; "
                                "padding: 0px 0px 0px 0px;} ")

        vLayout.addWidget(btn_group)
        hLayout = QHBoxLayout()
        btn_group.setLayout(hLayout)

        btn_check = QPushButton('Check')
        btn_check.clicked.connect(self.check)
        hLayout.addWidget(btn_check)

        btn_new_game = QPushButton('New Game')
        btn_new_game.clicked.connect(self.newGame)
        hLayout.addWidget(btn_new_game)

        btn_solve = QPushButton('Solve')
        btn_solve.clicked.connect(self.solve)
        hLayout.addWidget(btn_solve)

        btn_stop = QPushButton('Stop')
        btn_stop.clicked.connect(self.stop)
        hLayout.addWidget(btn_stop)
        # endregion

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
        msgbox.setText('Sudoku v3.0\n\n'
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
        self.solveSudoku = SolveSudoku(m)
        self.solveSudoku.start()

    def updateBoard(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] != '0':
                    self.board[i][j].setText(self.matrix[i][j])
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
