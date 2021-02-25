#include <QMainWindow>
#include "ui_mainwindow.h"


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr) : QMainWindow(parent) , ui(new Ui::MainWindow)
    {
        ui->setupUi(this);
//        connect(ui->pushButton, SIGNAL(clicked()), this, SLOT(NumPressed()));
    }

    ~MainWindow()
    {
        delete ui;
    }

private:
    Ui::MainWindow *ui;

private slots:
    void NumPressed()
    {
//        ui->pushButton->setText("besco");
    }
};
