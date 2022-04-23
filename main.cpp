#include <QApplication>
#include "source_cpp/mainwindow.h"


using namespace std;


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow window;
    window.show();

    return a.exec();
}
