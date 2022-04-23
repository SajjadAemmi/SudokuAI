import random
import time
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from source_python.sudoku import Sudoku
from .data import start_matrices


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.old_row, self.old_col = None, None

        loader = QUiLoader()
        self.ui = loader.load('mainwindow.ui')

        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.ui.progress_bar.setVisible(False)

        for i in range(9):
            for j in range(9):
                self.board[i][j] = getattr(self.ui, f'tb_{i}{j}')

        self.ui.menu_new_game.triggered.connect(self.newGame)
        self.ui.menu_open.triggered.connect(self.openFile)
        self.ui.menu_exit.triggered.connect(self.exit)
        self.ui.menu_help_game.triggered.connect(self.help)
        self.ui.menu_about.triggered.connect(self.about)

        self.ui.btn_check.clicked.connect(self.check)
        self.ui.btn_new_game.clicked.connect(self.newGame)
        self.ui.btn_solve.clicked.connect(self.solveGame)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.ui.cb_preview.clicked.connect(self.setPreview)

        self.sudoku = Sudoku()
        self.sudoku.signal_show_cell.connect(self.showCell)
        self.sudoku.signal_hide_cell.connect(self.hideCell)
        self.sudoku.signal_solved.connect(self.solved)

        self.newGame()
        self.ui.show()

    def exit(self):
        exit()
    
    def setPreview(self):
        self.sudoku.preview = not self.sudoku.preview

    def stop(self):
        self.run = False
        del self.sudoku

    def openFile(self):
        file_location = QFileDialog.getOpenFileName(self, caption="Open File", dir=".", filter="*.txt")[0]

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
        self.init_matrix = list()
        self.sudoku.matrix = list()
        rows = random.choice(start_matrices)

        for row in rows:
            cells = "".join(row).split(' ')
            self.init_matrix.append(list(map(int, cells)))
            self.sudoku.matrix.append(list(map(int, cells)))

        self.ui.progress_bar.setVisible(False)
        self.ui.lbl_time.setVisible(False)
        self.updateBoard()

    def solveGame(self):
        self.ui.progress_bar.setVisible(True)
        self.ui.lbl_time.setVisible(False)

        self.start_time = time.time()
        self.sudoku.start()

    def solved(self):
        self.end_time = time.time()
        self.ui.lbl_time.setText(str("%.4f" % (self.end_time - self.start_time)) + " seconds")
        self.ui.progress_bar.setVisible(False)
        self.ui.lbl_time.setVisible(True)
        self.updateBoard()
        
    def showCell(self, row, col, num):
        if self.old_row != None and self.old_col != None:
            self.board[self.old_row][self.old_col].setStyleSheet('background-color: lightgreen')

        self.old_row, self.old_col = row, col
        self.board[row][col].setText(str(num))
        self.board[row][col].setStyleSheet("background-color: lightblue")

    def hideCell(self, row, col):
        self.board[row][col].setStyleSheet('none')
        self.board[row][col].setText('')
    
    def updateBoard(self):
        for i in range(9):
            for j in range(9):
                if str(self.sudoku.matrix[i][j]) == '0':
                    self.board[i][j].setText("")                    
                else:
                    self.board[i][j].setText(str(self.sudoku.matrix[i][j]))
                
                if str(self.init_matrix[i][j]) != '0':
                    self.board[i][j].setStyleSheet('background-color: lightgray')
                    self.board[i][j].setReadOnly(True)
                else:
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
