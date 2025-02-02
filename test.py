from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
from answers import *

@move.vmove()
def main():
    state = answer_1()
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(10):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];



ccx q[0],q[1],q[2];
"""

scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)

animation = scorer.animate()
animation.save("animation.gif", writer=PillowWriter(fps=1))