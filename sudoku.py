from PySide2.QtCore import QThread, Signal
import time

class Sudoku(QThread):
    signal_show_cell = Signal(object, object, object)
    signal_hide_cell = Signal(object, object)
    signal_solved = Signal()

    def __init__(self):
        super(Sudoku, self).__init__()
        
        self.matrix = list()
        self.DH = []
        self.delay = 0.05
        self.preview = False

    def run(self):
        self.degreeCalculation()
        if self.Sudoku():
            print("Done!")
            self.signal_solved.emit()
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

    def Sudoku(self):
        try:
            flag, row, col = self.Heuristic()

            if not flag:
                return True

            for num in range(1, 10):
                if self.isSafe(row, col, num):

                    self.Set(row, col)
                    self.matrix[row][col] = num
                    if self.preview:
                        time.sleep(self.delay)
                        self.signal_show_cell.emit(row, col, num)

                    if self.Sudoku():
                        return True

                    self.UnSet(row, col)
                    self.matrix[row][col] = 0
                    if self.preview:
                        time.sleep(self.delay)
                        self.signal_hide_cell.emit(row, col)

            return False

        except:
            print('some problem')

        return True
