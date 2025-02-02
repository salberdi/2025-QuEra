from bloqade import move
from helper_functions import *

@move.vmove()
def answer_1a():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0,1,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1]])
    state = local_CX(atom_state=state,target_indices=[2])
    return state

@move.vmove()
def answer_1b():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0], q[1], q[2]], indices=[0, 1, 2])
    
    state.gate[[2,1,0]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi*.25,axis_phase_exponent=0,indices=[1])
    
    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi*.25,axis_phase_exponent=0,indices=[3])

    state.gate[[1]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi*.25,axis_phase_exponent=0,indices=[1])

    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi*.25,axis_phase_exponent=0,indices=[3])

state.gate[[4,5]] = move.Move(state.gate[[0,2]])

    

    return state


@move.vmove()
def answer_2():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])
    state = move.LocalRz(atom_state=state, phi = pi * .125, indices=[2])
    state = local_RX(atom_state=state, angle = pi * .125, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, angle = -pi *.125, indices=[3])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, angle = pi *.25, indices=[3])
    
    state = move.LocalRz(atom_state=state, phi = pi * .25, indices = [0])
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, angle = -pi *.25, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = local_RX(atom_state=state, angle = pi *.25, indices=[2])
    state = move.LocalRz(atom_state=state, phi = pi * .25, indices = [3])
    state = move.GlobalCZ(atom_state=state)
    state = local_RX(atom_state=state, angle = -pi *.25, indices=[2])
    state = move.GlobalCZ(atom_state=state)
    state = global_H(atom_state=state)
    return state

@move.vmove()
def answer_3():
    return 0

@move.vmove()
def answer_4():
    return 0

@move.vmove()
def answer_5():
    return 0