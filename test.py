from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
from answers import *

# @move.vmove()
# def main():
#     q = move.NewQubitRegister(1)
#     state = move.Init(qubits=[q[0]], indices=[0])
#     state = move.GlobalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0)
#     # state = move.GlobalRz(atom_state=state,phi=1/2)

#     move.Execute(state)

@move.vmove()
def main():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1]])

    # state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    # state = move.LocalRz(atom_state=state,phi=pi,indices=[2])
    # state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)

    state = move.LocalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=pi/2,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0,indices=[2])
    
    # state = local_CX(atom_state=state,target_indices=[2])

    state = move.GlobalCZ(atom_state=state)

    state = move.LocalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=pi/2,indices=[2])
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0,indices=[2])
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(10):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


cz q[0],q[1];
cx q[2],q[1];
"""
# h q[1];
# cx q[2],q[1];


scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)