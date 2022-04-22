#include "fstream"
#include "QMainWindow"
#include "QThread"


#define UNASSIGNED 0
#define N 9


struct DegreeHeuristic
{
    int Row; int Col; int degree; int IsSet;
};


class Sudoku : public QThread
{
    Q_OBJECT

public:
    int matrix[N][N];
    bool preview;
    explicit Sudoku();
    ~Sudoku();
    void run();
    void sort();
    void degreeCalculation();
    bool heuristic(int &Row, int &Col);
    bool solve();
    void set(int Row, int Col);
    void unSet(int Row, int Col);
    bool usedInRow(int Row, int num);
    bool usedInCol(int Col, int num);
    bool usedInBox(int boxStartRow, int boxStartCol, int num);
    bool isSafe(int Row, int Col, int num);

private:
    float delay;
    std::vector<DegreeHeuristic> DH;
    int DH_size;

public slots:
   void setPreview(bool);

signals:
   void signalShowCell(int row, int col, int num);
   void signalHideCell(int row, int col);
   void solved();

};
