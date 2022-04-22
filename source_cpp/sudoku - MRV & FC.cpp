/*
* C++ Program to Solve Sudoku Problem using BackTracking & CSP
*
* Nilufar Tabaee
*/

#include <iostream>
#include <Windows.h>
#include <fstream>

using namespace std;

class Sudoku
{
public:
	Sudoku();
	~Sudoku();
	void input();
	void output();
	void init();
	void LCV();
	void MRV(int*, int*);
	bool SolveSudoku();
	void Constraint();
	bool ForwardChecking();
	void MaxDegree(int *, int *);
	bool isfinish();
	void PrintSudoku(int, int);
	bool isSafe(int, int, int);
	friend class node;
private:

};

Sudoku::Sudoku()
{
}

Sudoku::~Sudoku()
{
}

class node
{
public:
	node();
	~node();
	friend class Sudoku;
private:
	int value;
	int list[10];
	bool fixed;
};

node::node()
{
	
}

node::~node()
{
}

node matrix[9][9];
node temp[9][9];

long int BackTrackCounter = 0;

//=============================================

void gotoxy(int x, int y)
{
	COORD pos;
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

	if (INVALID_HANDLE_VALUE != hConsole)
	{
		pos.X = x;
		pos.Y = y;
		SetConsoleCursorPosition(hConsole, pos);
	}
}

//=============================================

void Color(int number)
{
	HANDLE Color;
	Color = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(Color, number);
}

//=============================================

void Sudoku::input()
{
	fstream f;

	f.open("d://s2.txt", ios::in);

	if (!f)
	{
		cout << "no file available\n";
		system("pause");
		exit(0);
	}

	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			f >> matrix[i][j].value;
		}
	}
	f.close();
	init();
}

//=============================================

void Sudoku::output()
{
	fstream f;

	f.open("d://out.txt", ios::out);

	if (!f)
	{
		cout << "no file available\n";
		system("pause");
		exit(0);
	}

	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			f << matrix[i][j].value << " ";
		}
		f << "\n";
	}
	f.close();
}

//=============================================

void Sudoku::init()
{
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			if(matrix[i][j].value == 0)
				matrix[i][j].fixed = false;
			else
				matrix[i][j].fixed = true;
		}
	}
}

void Sudoku::MRV(int *Row, int *Col)
{
	Constraint();
	int min = INT_MAX;
	int cntr;

	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			if (matrix[i][j].value == 0)
			{
				cntr = 0;
				for (int l = 1; l <= 9; l++)
				{
					if (matrix[i][j].list[l] == 1)
						cntr++;
				}
				if (cntr <= min)
				{
					min = cntr;
					*Row = i;
					*Col = j;
				}
			}
		}
	}
}

void Sudoku::LCV()
{

}

void Sudoku::Constraint()
{
	
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			if (matrix[i][j].value == 0)
			{
				for (int l = 1; l <= 9; l++)
				{
					matrix[i][j].list[l] = 1;
				}

				for (int l = 1; l <= 9; l++)
				{
					for (int k = 0; k < 9; k++)
					{
						if (matrix[i][k].value == l && k != j)
						{
							matrix[i][j].list[l] = 0;
						}
						if (matrix[k][j].value == l && k != i)
						{
							matrix[i][j].list[l] = 0;
						}
					}
					for (int k = (i / 3) * 3; k < ((i / 3) * 3) + 3; k++)
					{
						for (int m = (j / 3) * 3; m < ((j / 3) * 3) + 3; m++)
						{
							if (matrix[k][m].value == l && k != i && m != j)
							{
								matrix[i][j].list[l] = 0;
							}
						}
					}
				}
			}
		}
	}
}

bool Sudoku::ForwardChecking()
{
	Constraint();
	bool sw;

	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			if (matrix[i][j].value == 0)
			{
				sw = false;

				for (int l = 1; l <= 9; l++)
				{
					if (matrix[i][j].list[l] == 1)
					{
						sw = true;
						break;
					}
				}
				if (sw == false)
				{
					return false;
				}
			}
		}
	}
	return true;
}

void Sudoku::MaxDegree(int *Row, int *Col)
{
	//int max = 0;
	int max = INT_MAX;
	int cntr;

	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			cntr = 0;
			if (matrix[i][j].value == 0)
			{
				for (int k = 0; k < 9; k++)
				{
					if (matrix[i][k].value == 0 && k != j)
					{
						cntr++;
					}
					if (matrix[k][j].value == 0 && k != i)
					{
						cntr++;
					}
				}
				for (int k = (i / 3) * 3; k < ((i / 3) * 3) + 3; k++)
				{
					for (int m = (j / 3) * 3; m < ((j / 3) * 3) + 3; m++)
					{
						if (matrix[k][m].value == 0 && k != i && m != j)
						{
							cntr++;
						}
					}
				}
				if (cntr <= max)
				{
					max = cntr;
					*Row = i;
					*Col = j;
				}
			}
		}
	}
}

//=============================================

bool Sudoku::isfinish()
{
	for (int i = 0; i < 9; i++)
		for (int j = 0; j < 9; j++)
			if (matrix[i][j].value == 0)
				return false;

	return true;
}

//=============================================

bool Sudoku::SolveSudoku()
{
	if (isfinish())
		return true;

	int Row, Col;

	//MaxDegree(&Row, &Col);
	MRV(&Row, &Col);

	for (int num = 1; num <= 9; num++)
	{
		if (isSafe(Row, Col, num))
		{
			matrix[Row][Col].value = num;

			//PrintSudoku(Row, Col);

			if (ForwardChecking())
			{
				if (SolveSudoku())
					return true;
			}
			matrix[Row][Col].value = 0;

			//PrintSudoku(Row, Col);
		}
	}
	BackTrackCounter++;

	return false;
}

//=============================================

bool Sudoku::isSafe(int Row, int Col, int num)
{
	for (int i = 0; i < 9; i++)
		if (matrix[Row][i].value == num)
			return false;

	for (int i = 0; i < 9; i++)
		if (matrix[i][Col].value == num)
			return false;
	
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
			if (matrix[i + (Row - Row % 3)][j + (Col - Col % 3)].value == num)
				return false;
	
	return true;
}

//=============================================

void Sudoku::PrintSudoku(int Row, int Col)
{
	Sleep(100);
	system("cls");

	for (int i = 0; i < 9; i++)
	{
		if (i % 3 == 0)
		{
			cout << "_ _ _ _ _ _ _ _ _ _ _ _ _" << endl << endl;
		}


		for (int j = 0; j < 9; j++)
		{
			Color(14);

			if (j % 3 == 0)
			{
				cout << "| ";
			}

			if (matrix[i][j].fixed == true)
				Color(11);
			else if (i == Row && j == Col)
				Color(10);
			else
				Color(15);

			if (matrix[i][j].value == 0)
				cout << "_";
			else
				cout << matrix[i][j].value;

			cout << " ";
		}
		Color(14);
		cout << "| ";

		if (i % 3 == 2)
			cout << endl;
		else
			cout << endl << endl;
	}
	cout << "_ _ _ _ _ _ _ _ _ _ _ _ _";
	cout << "\n" << "BackTrackCounter: " << BackTrackCounter;
}

//=============================================

int main()
{
	Sudoku sdk;

	sdk.input();

	if (sdk.SolveSudoku() == true)
	{
		sdk.PrintSudoku(9, 9);
		sdk.output();
	}

	else cout << "No solution exists" << endl;

	cout << "\n";
	system("pause");
	return 0;
}