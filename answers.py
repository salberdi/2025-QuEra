from bloqade import move
from helper_functions import *

def main():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1])
    state. = local_H(state=state,target_indices=[2])
    state.storage[[0,1,2]] = move.Move(state.gate[[0,2,3]])
    move.Execute(state)
    return state