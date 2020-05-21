import numpy as np

y = { "l":"f", "li":"fi", "r":"b", "ri":"bi", "f":"r", "fi":"ri", "b":"l", "bi":"li", "u":"u","ui":"ui", "d":"d", "di":"di" }
yi = { "l":"b", "li":"bi", "r":"f", "ri":"fi", "f":"l", "fi":"li", "b":"r", "bi":"ri", "u":"u","ui":"ui", "d":"d", "di":"di" }

x = { "l":"l", "li":"li", "r":"r", "ri":"ri", "f":"d", "fi":"di", "b":"u", "bi":"ui", "u":"f","ui":"fi", "d":"b", "di":"bi" }
xi = { "l":"l", "li":"li", "r":"r", "ri":"ri", "f":"u", "fi":"ui", "b":"d", "bi":"di", "u":"b","ui":"bi", "d":"f", "di":"fi" }

z = { "l":"d", "li":"di", "r":"u", "ri":"ui", "f":"f", "fi":"fi", "b":"b", "bi":"bi", "u":"l","ui":"li", "d":"r", "di":"ri" }
zi = { "l":"u", "li":"ui", "r":"d", "ri":"di", "f":"f", "fi":"fi", "b":"b", "bi":"bi", "u":"r","ui":"ri", "d":"l", "di":"li" }

mat = np.array([[0, 0,0,0, 0],\

                [0, 1,1,1, 0],\
                [0, 1,1,1, 0],\
                [0, 1,1,1, 0],\

                [0, 0,0,0, 0]],np.uint8)


algo = np.array([])

file = 'OLL/solved.npz'

np.savez(file,mat,algo)


"""
cross: 1234567
line: 1234
dot: 12345678
4corners: 12
shapeLi: 123456
shapeL: 123456
shape7: 1234
shape7i: 1234
C: 12
L: 1234
P: 1234
T: 12
W: 12
Z: 12
"""

