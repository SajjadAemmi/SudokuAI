#include <iostream>
#include "unistd.h"
#include "QFile"
#include "QDir"
#include "QtDebug"
#include "QMessageBox"
#include "QTextStream"
#include "mainwindow.h"


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
    this->newGame();
    delay = 0.1;
    old_row = -1;
    old_col = -1;

//    connect(sudoku, SIGNAL(signalHideCell(int, int)), this, SLOT(slotHideCell(int, int)));
}


MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::newGame()
{
//    QString dir = QDir::currentPath();
    QFile file(":/data/s4.txt");
//    qDebug() << file_path;

    if(!file.open(QIODevice::ReadOnly)) {
        QMessageBox::information(0, "error", file.errorString());
    }

    QTextStream in(&file);

    for (int i = 0; i < N; i++)
    {
        QString line = in.readLine();
        QStringList fields = line.split(" ");

        for (int j = 0; j < N; j++)
        {
            temp[i][j] = fields[j].toInt();
            this->tb[i][j]->setText(fields[j]);
        }
    }

    file.close();
}


void MainWindow::solveGame()
{
    sudoku = new Sudoku(temp);
//    connect(sudoku, SIGNAL(signalShowCell(int, int, int)), this, SLOT(slotShowCell(int, int, int)));
    connect(sudoku, SIGNAL(signalTest()), this, SLOT(slotTest()));
    sudoku->start();
}

void MainWindow::slotTest()
{

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
    sleep(delay);
}


void MainWindow::slotHideCell(int row, int col)
{
    this->tb[row][col]->setStyleSheet("none");
    this->tb[row][col]->setText("");
    sleep(delay);
}
