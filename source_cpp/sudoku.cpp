#include "iostream"
#include "QtDebug"
#include <source_cpp/sudoku.h>


using namespace std;


Sudoku::Sudoku()
{
    delay = 10;
    preview = false;
}


Sudoku::~Sudoku()
{

}


void Sudoku::run()
{
    DH.clear();
    degreeCalculation();

    if (solve() == true)
    {
        qDebug() << "solved";
        emit solved();
    }
    else
        qDebug() << "No solution exists";
}


void Sudoku::sort()
{
    for (int i = 0; i < DH_size; i++)
    {
        for (int j = i + 1; j < DH_size; j++)
        {
            if (DH[i].degree > DH[j].degree)
                swap(DH[i], DH[j]);
        }
    }
}


void Sudoku::degreeCalculation()
{
    int cntr;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (matrix[i][j] == UNASSIGNED)
            {
                cntr = 0;
                DegreeHeuristic dh;
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
                dh.degree = cntr;
                dh.Row = i;
                dh.Col = j;
                dh.IsSet = 0;
                DH.push_back(dh);
            }
        }
    }
    DH_size = DH.size();
    sort();
}


bool Sudoku::heuristic(int &Row, int &Col)
{
    for (int i = 0; i < DH_size; i++)
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


void Sudoku::set(int Row, int Col)
{
    for (int i = 0; i < DH_size; i++)
    {
        if (Row == DH[i].Row && Col == DH[i].Col)
        {
            DH[i].IsSet = 1;

            for (int j = 0; j < DH_size; j++)
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


void Sudoku::unSet(int Row, int Col)
{
    for (int i = 0; i < DH_size; i++)
    {
        if (Row == DH[i].Row && Col == DH[i].Col)
        {
            DH[i].IsSet = 0;

            for (int j = 0; j < DH_size; j++)
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


void Sudoku::setPreview(bool b)
{
    preview = !preview;
}


bool Sudoku::solve()
{
    int row, col;
    if (!heuristic(row, col))
        return true;

    for (int num = 1; num <= N; num++)
    {
        if (isSafe(row, col, num))
        {
            set(row, col);
            matrix[row][col] = num;

            if(preview)
            {
                msleep(delay);
                emit signalShowCell(row, col, num);
            }

            if (solve())
                return true;

            unSet(row, col);
            matrix[row][col] = UNASSIGNED;

            if(preview)
            {
                msleep(delay);
                emit signalHideCell(row, col);
            }
        }
    }
    return false;
}


bool Sudoku::usedInRow(int Row, int num)
{
    for (int Col = 0; Col < N; Col++)
        if (matrix[Row][Col] == num)
            return false;
    return true;
}


bool Sudoku::usedInCol(int Col, int num)
{
    for (int Row = 0; Row < N; Row++)
        if (matrix[Row][Col] == num)
            return false;
    return true;
}


bool Sudoku::usedInBox(int boxStartRow, int boxStartCol, int num)
{
    for (int Row = 0; Row < 3; Row++)
        for (int Col = 0; Col < 3; Col++)
            if (matrix[Row + boxStartRow][Col + boxStartCol] == num)
                return false;
    return true;
}


bool Sudoku::isSafe(int Row, int Col, int num)
{
    return usedInRow(Row, num) && usedInCol(Col, num) && usedInBox(Row - Row % 3, Col - Col % 3, num);
}
