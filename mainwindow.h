#include <fstream>
#include <QMainWindow>
#include "QLineEdit"
#include <sudoku.h>
#include "ui_mainwindow.h"


#define UNASSIGNED 0
#define N 9


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void updateBoard();

private:
    Ui::MainWindow *ui;
    int init_matrix[N][N];
    QLineEdit *tb[N][N];
    Sudoku *sudoku;
    int old_row;
    int old_col;
    clock_t start_time;
    clock_t end_time;

private slots:
    void newGame();
    void solveGame();
    void solved();
    void slotShowCell(int row, int col, int num);
    void slotHideCell(int row, int col);
};
