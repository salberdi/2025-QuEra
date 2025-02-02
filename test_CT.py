from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
# from answers import *


@move.vmove()
def main():
    q = move.NewQubitRegister(2)

    state = move.Init(qubits=[q[0],q[1]], indices=[0,1])
    state.gate[[0,1]] = move.Move(state.storage[[0,1]])
    state = local_CP(atom_state=state,phi = pi*.25,indices=[0,1],target =[1],control = [0])
    
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(10):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];

// Operation: CRz(0.25π)(q(0), q(1))
cx q[0],q[1];
u3(0,pi*1.375,pi*0.5) q[1];
cx q[0],q[1];
u3(0,pi*1.625,pi*0.5) q[1];
"""

scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)

animation = scorer.animate()
animation.save("animation.gif", writer=PillowWriter(fps=1))