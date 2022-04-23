#include <iostream>
#include "QFile"
#include "QDir"
#include "QtDebug"
#include "QMessageBox"
#include "QTextStream"
#include "source_cpp/mainwindow.h"
#include "time.h"


using namespace std;

int temp[N][N];

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            this->tb[i][j] = MainWindow::findChild<QLineEdit *>("tb_" + QString::number(i) + QString::number(j));
        }
    }

    connect(ui->btn_solve, SIGNAL(clicked()), this, SLOT(solveGame()));
    connect(ui->btn_new_game, SIGNAL(clicked()), this, SLOT(newGame()));

    sudoku = new Sudoku();
    connect(sudoku, SIGNAL(signalShowCell(int, int, int)), this, SLOT(slotShowCell(int, int, int)));
    connect(sudoku, SIGNAL(signalHideCell(int, int)), this, SLOT(slotHideCell(int, int)));
    connect(sudoku, SIGNAL(solved()), this, SLOT(solved()));
    connect(ui->cb_preview, SIGNAL(toggled(bool)), sudoku, SLOT(setPreview(bool)));

    this->newGame();

    old_row = -1;
    old_col = -1;
}


MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::newGame()
{
//    QString dir = QDir::currentPath();
    srand(time(0));
    int r = rand() % 6 + 1;
    QFile file(":/data/s" + QString::number(r) + ".txt");

    if(!file.open(QIODevice::ReadOnly))
    {
        QMessageBox::information(0, "error", file.errorString());
    }

    QTextStream in(&file);

    for (int i = 0; i < N; i++)
    {
        QString line = in.readLine();
        QStringList fields = line.split(" ");

        for (int j = 0; j < N; j++)
        {
            sudoku->matrix[i][j] = fields[j].toInt();
            init_matrix[i][j] = fields[j].toInt();
        }
    }
    file.close();

    ui->progress_bar->setVisible(false);
    ui->lbl_time->setVisible(false);
    updateBoard();
}


void MainWindow::solveGame()
{
    ui->progress_bar->setVisible(true);
    ui->lbl_time->setVisible(false);
    start_time = clock();
    sudoku->start();
}


void MainWindow::solved()
{
    end_time = clock();
    ui->lbl_time->setText(QString::number(float(end_time - start_time) / CLOCKS_PER_SEC) + " seconds");
    ui->progress_bar->setVisible(false);
    ui->lbl_time->setVisible(true);
    updateBoard();
}


void MainWindow::slotShowCell(int row, int col, int num)
{
    if(old_row != -1 && old_col != -1)
    {
        this->tb[old_row][old_col]->setStyleSheet("background-color: lightgreen");
    }
    old_row = row;
    old_col = col;
    this->tb[row][col]->setText(QString::number(num));
    this->tb[row][col]->setStyleSheet("background-color: lightblue");
}


void MainWindow::slotHideCell(int row, int col)
{
    this->tb[row][col]->setStyleSheet("none");
    this->tb[row][col]->setText("");
}


void MainWindow::updateBoard()
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if(sudoku->matrix[i][j] == 0)
            {
                this->tb[i][j]->setText("");
            }
            else
            {
                this->tb[i][j]->setText(QString::number(sudoku->matrix[i][j]));
            }

            if(init_matrix[i][j] == 0)
            {
                this->tb[i][j]->setStyleSheet("none");
            }
            else
            {
                this->tb[i][j]->setStyleSheet("background-color: darkgray");
            }
        }
    }
}
