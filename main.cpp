#include <QApplication>
#include <QMainWindow>
#include <iostream>
#include <fstream>
#include <mainwindow.h>

using namespace std;

#define UNASSIGNED 0
#define N 9


struct DegreeHeuristic
{
    int Row; int Col; int degree; int IsSet;
}DH[100];

int NumOfZero = 0;

int temp[N][N];

bool isSafe(int matrix[N][N], int Row, int Col, int num);
void PrintSudoku(int matrix[N][N], int Row, int Col);


void input(int matrix[N][N])
{
    fstream f;

    f.open("d://s6.txt", ios::in);

    if (!f)
    {
        cout << "no file available\n";
        system("pause");
        exit(0);
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            f >> matrix[i][j];
            temp[i][j] = matrix[i][j];
        }
    }
    f.close();
}


void output(int matrix[N][N])
{
    fstream f;

    f.open("d://out.txt", ios::out);

    if (!f)
    {
        cout << "no file available\n";
        system("pause");
        exit(0);
    }

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            f << matrix[i][j] << " ";
        }
        f << "\n";
    }
    f.close();
}

//=============================================

void sort()
{
    for (int i = 0; i < NumOfZero; i++)
    {
        for (int j = i + 1; j < NumOfZero; j++)
        {
            if (DH[i].degree > DH[j].degree)
                swap(DH[i], DH[j]);
        }
    }
}

//=============================================

void DegreeCalculation(int matrix[N][N])
{
    int cntr;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cntr = 0;
            if (matrix[i][j] == UNASSIGNED)
            {
                for (int k = 0; k < N; k++)
                {
                    if (matrix[i][k] == UNASSIGNED && k != j)
                    {
                        cntr++;
                    }
                    if (matrix[k][j] == UNASSIGNED && k != i)
                    {
                        cntr++;
                    }
                }
                for (int k = (i / 3) * 3; k < ((i / 3) * 3) + 3; k++)
                {
                    for (int m = (j / 3) * 3; m < ((j / 3) * 3) + 3; m++)
                    {
                        if (matrix[k][m] == UNASSIGNED && k != i && m != j)
                        {
                            cntr++;
                        }
                    }
                }
                DH[NumOfZero].degree = cntr;
                DH[NumOfZero].Row = i;
                DH[NumOfZero].Col = j;
                NumOfZero++;
            }
        }
    }
    for (int i = 0; i < NumOfZero; i++)
    {
        DH[i].IsSet = 0;
    }
    sort();
}

//=============================================

bool Heuristic(int matrix[N][N], int &Row, int &Col)
{
    for (int i = 0; i < NumOfZero; i++)
    {
        if (DH[i].IsSet == 0)
        {
            Row = DH[i].Row;
            Col = DH[i].Col;

            return true;
        }
    }
    return false;
}

void Set(int matrix[N][N], int Row, int Col)
{
    for (int i = 0; i < NumOfZero; i++)
    {
        if (Row == DH[i].Row && Col == DH[i].Col)
        {
            DH[i].IsSet = 1;

            for (int j = 0; j < NumOfZero; j++)
            {
                if (DH[i].Row == DH[j].Row || DH[i].Col == DH[j].Col || (DH[i].Row / 3 == DH[j].Row / 3 && DH[i].Col / 3 == DH[j].Col / 3))
                {
                    DH[j].degree--;
                }
            }
            sort();
            break;
        }
    }
}


//=============================================

void UnSet(int matrix[N][N], int Row, int Col)
{
    for (int i = 0; i < NumOfZero; i++)
    {
        if (Row == DH[i].Row && Col == DH[i].Col)
        {
            DH[i].IsSet = 0;

            for (int j = 0; j < NumOfZero; j++)
            {
                if (DH[i].Row == DH[j].Row || DH[i].Col == DH[j].Col || (DH[i].Row / 3 == DH[j].Row / 3 && DH[i].Col / 3 == DH[j].Col / 3))
                {
                    DH[j].degree++;
                }
            }
            sort();
            break;
        }
    }
}

//=============================================

bool Sudoku(int matrix[N][N])
{
    int Row, Col;
    if (!Heuristic(matrix, Row, Col))
        return true;

    for (int num = 1; num <= N; num++)
    {
        if (isSafe(matrix, Row, Col, num))
        {
            Set(matrix, Row, Col);

            matrix[Row][Col] = num;

//            PrintSudoku(matrix, Row, Col);

            if (Sudoku(matrix))
                return true;

            UnSet(matrix, Row, Col);

            matrix[Row][Col] = UNASSIGNED;

//            PrintSudoku(matrix, Row, Col);
        }
    }
    return false;
}

//=============================================

bool UsedInRow(int matrix[N][N], int Row, int num)
{
    for (int Col = 0; Col < N; Col++)
    if (matrix[Row][Col] == num)
        return false;
    return true;
}

//=============================================

bool UsedInCol(int matrix[N][N], int Col, int num)
{
    for (int Row = 0; Row < N; Row++)
    if (matrix[Row][Col] == num)
        return false;
    return true;
}

//=============================================

bool UsedInBox(int matrix[N][N], int boxStartRow, int boxStartCol, int num)
{
    for (int Row = 0; Row < 3; Row++)
    for (int Col = 0; Col < 3; Col++)
    if (matrix[Row + boxStartRow][Col + boxStartCol] == num)
        return false;
    return true;
}

//=============================================

bool isSafe(int matrix[N][N], int Row, int Col, int num)
{
    return UsedInRow(matrix, Row, num) && UsedInCol(matrix, Col, num) && UsedInBox(matrix, Row - Row % 3, Col - Col % 3, num);
}


int main(int argc, char *argv[])
{
    int matrix[N][N];

//	input(matrix);

//	DegreeCalculation(matrix);

//	if (Sudoku(matrix) == true)
//	{
//		PrintSudoku(matrix, N, N);
//		output(matrix);
//	}

//	else cout << "No solution exists" << endl;


    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
