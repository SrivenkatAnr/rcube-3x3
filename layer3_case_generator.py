import numpy as np

y = { "l":"f", "li":"fi", "r":"b", "ri":"bi", "f":"r", "fi":"ri", "b":"l", "bi":"li", "u":"u","ui":"ui", "d":"d", "di":"di" }
yi = { "l":"b", "li":"bi", "r":"f", "ri":"fi", "f":"l", "fi":"li", "b":"r", "bi":"ri", "u":"u","ui":"ui", "d":"d", "di":"di" }

x = { "l":"l", "li":"li", "r":"r", "ri":"ri", "f":"d", "fi":"di", "b":"u", "bi":"ui", "u":"f","ui":"fi", "d":"b", "di":"bi" }
xi = { "l":"l", "li":"li", "r":"r", "ri":"ri", "f":"u", "fi":"ui", "b":"d", "bi":"di", "u":"b","ui":"bi", "d":"f", "di":"fi" }

z = { "l":"d", "li":"di", "r":"u", "ri":"ui", "f":"f", "fi":"fi", "b":"b", "bi":"bi", "u":"l","ui":"li", "d":"r", "di":"ri" }
zi = { "l":"u", "li":"ui", "r":"d", "ri":"di", "f":"f", "fi":"fi", "b":"b", "bi":"bi", "u":"r","ui":"ri", "d":"l", "di":"li" }

mat = np.array([],np.uint8)


algo = np.array([])
file = 'PLL/solved.npz'

np.savez(file,mat,algo)


temp = [[ 1,  2,  3 ],\

		[ 4,  5,  6 ],\

		[ 7,  8,  9 ]]

"""
A: 1,2
U: 1,2
H, T
J: 1,2
R: 1,2
G: 1,2,3,4
F, Z, Y
N: 1,2
E
"""