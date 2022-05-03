using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace Sudoku_AI
{
    public partial class Form1 : Form
    {
        TextBox[,] textboxes;
        String[,] memory = new String[9, 9];

        public Form1()
        {
            InitializeComponent();
            textboxes = new TextBox[9, 9];

            for (int i = 0, ui_i = 0; i < 9; i++, ui_i++)
            {
                if (i == 3 || i == 6) ui_i++;

                for (int j = 0, ui_j = 0; j < 9; j++, ui_j++)
                {
                    if (j == 3 || j == 6) ui_j++;

                    textboxes[i, j] = new TextBox();
                    textboxes[i, j].Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right | AnchorStyles.Left;
                    textboxes[i, j].Font = new Font("Arial", 24);
                    textboxes[i, j].TextAlign = HorizontalAlignment.Center;
                    textboxes[i, j].Multiline = true;
                    textboxes[i, j].TextChanged += Check;

                    tableLayoutPanel1.Controls.Add(textboxes[i, j], ui_i, ui_j);
                }
            }
        }

        private void resetGame()
        {
            for (int i = 0, k = 0; i < 9; i++)
            {
                for (int j = 0; j < 9; j++, k++)
                {
                    textboxes[i, j].Text = "";
                    textboxes[i, j].BackColor = Color.White;
                    textboxes[i, j].ReadOnly = false;
                }
            }
        }

        private void startGame(String[] numbers)
        {
            resetGame();
            for (int i = 0, k = 0; i < 9; i++)
            {
                for (int j = 0; j < 9; j++, k++)
                {
                    textboxes[i, j].TextChanged -= Check;
                    memory[i, j] = numbers[k];
                    if (numbers[k].CompareTo("0") != 0)
                    {
                        textboxes[i, j].Text = numbers[k];
                        textboxes[i, j].BackColor = Color.LightGray;
                        textboxes[i, j].ReadOnly = true;
                    }
                    textboxes[i, j].TextChanged += Check;
                }
            }
        }

        private void Check(object sender, EventArgs e)
        {
            Boolean sw;

            for (int i = 0; i < 9; i++)
            {
                for (int j = 0; j < 9; j++)
                {
                    if (memory[i, j] == "0" && textboxes[i, j].Text != "")
                    {
                        sw = true;

                        // rows
                        for (int k = 0; k < 9; k++)
                        {
                            if (textboxes[i, k].Text == textboxes[i, j].Text && k != j)
                            {
                                sw = false;
                            }
                        }

                        // cols
                        for (int k = 0; k < 9; k++)
                        {
                            if (textboxes[k, j].Text == textboxes[i, j].Text && k != i)
                            {
                                sw = false;
                            }
                        }

                        // 3x3 squares
                        for (int k = 0; k < 3; k++)
                        {
                            for (int l = 0; l < 3; l++)
                            {
                                if (i >= 3 * k && i <= 3 * k + 2 && j >= 3 * l && j <= 3 * l + 2)
                                {
                                    for (int n = 3 * k; n < 3 * k + 2; n++)
                                    {
                                        for (int m = 3 * l; m < 3 * l + 2; m++)
                                        {
                                            if (textboxes[n, m].Text == textboxes[i, j].Text && (n != i || m != j))
                                            {
                                                sw = false;
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        if (sw == false)
                        {
                            textboxes[i, j].BackColor = Color.Red;
                        }
                        else
                        {
                            textboxes[i, j].BackColor = Color.LightGreen;
                        }
                    }
                }
            }
        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Sudoku v 3.5 \nProgrammer: Sajjad Aemmi \nAll Rights Reserved!", "About", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            String s;
            String[] numbers;
            Char[] sep = { ' ', '\r' };
            StreamReader openfile;
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Title = "Open input file";

            if (ofd.ShowDialog() == DialogResult.OK)
            {
                openfile = new StreamReader(ofd.FileName);
                s = openfile.ReadToEnd();
                s = s.Replace("\n", "");
                numbers = s.Split(sep);
                startGame(numbers);
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (MessageBox.Show("Do you want to exit?", "Exit", MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.No)
                e.Cancel = true;
        }
    }
}