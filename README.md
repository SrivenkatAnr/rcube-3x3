# A 3x3 Rubik's cube Solver and Simulator

#### This program creates a 3D simulation of the rubik's cube and includes and an inbuilt solver tool that uses Beginner's method for solving.

### Demo:
On running the main python file, a separate window opens, rendering the 3D view of the cube. 


<img src = https://raw.githubusercontent.com/SrivenkatAnr/rcube-3x3/master/README-pics/starting.png width = "75%" />

It also opens up a secondary cmd prompt in the default terminal window, where the user can enter specific commands for specific functions like **_scramble_**, **_solve_**, **_r_**, **_ri_** etc.

On scrambling, the window will look like:

<img src = https://raw.githubusercontent.com/SrivenkatAnr/rcube-3x3/master/README-pics/scrambled.png width = "75%" />

To create a specific scramble, enter the code for each rotation in a new line.
### Dependencies:
1. opencv==3.4.2
2. numpy==1.15.2
3. PyOpenGL==3.1.5
4. PyOpenGL-accelerate==3.1.5
5. scikit-learn==0.20.0
6. pygame==1.9.2

You can install the above dependencies manually or you can creating a new virtual environment(recommended) and cd into rcube-3x3 folder and run, `pip install requirements.txt`

### To run this file in your local machine:
##### Method (a): (For those who do not know to use the command line)
   1. Click on the green button (Clone or Download) on the top-right corner of this page.
   2. Extract the zip file and run the game3D-with-GL.py file
   
##### Method (b): (For those who are comfortable using the command line)
   1. Copy the url of this repo. [https://github.com/SrivenkatAnr/rcube-3x3.git](https://github.com/SrivenkatAnr/rcube-3x3.git)
   2. Make sure git is installed on your local machine. If not, check out this [link](https://git-scm.com/downloads) to install it.
   3. Open terminal and change to the directory where you want to have a local copy and clone this repo using `git clone <url>`
   4. Run the game python file using `python game3D-with-GL.py`
