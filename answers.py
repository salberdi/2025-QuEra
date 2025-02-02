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
    
    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi*.25,axis_phase_exponent=0.0,indices=[3])
    
    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi*.25,axis_phase_exponent=0.0,indices=[1])

    state.gate[[3]] = move.Move(state.gate[[1]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi*.25,axis_phase_exponent=0.0,indices=[3])

    state.gate[[1]] = move.Move(state.gate[[3]])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=pi*.25,axis_phase_exponent=0.0,indices=[1])

    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.LocalRz(atom_state=state, phi = -pi * .25, indices = [2])
    state = local_H(state, indices=[2])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent=-pi*.25,axis_phase_exponent=0.0,indices=[2])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalRz(atom_state=state, phi = pi * .25, indices = [3])
    state = local_H(atom_state=state, indices=[2])
    state = move.LocalRz(atom_state=state, phi= pi * .5, indices = [2])

    return state


@move.vmove()
def answer_2():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0,2,3]] = move.Move(state.storage[[0,1,2]])
    state = local_H(atom_state = state, indices = [3])
    #state = local_CS(atom_state=state,indices=[2,3],target=[3])
    state = local_CP(atom_state=state,phi = pi*.5,indices=[2,3],target =[3],control = [2])
    state.gate[[1]] = move.Move(state.gate[[3]])
    #state = local_CT(atom_state=state, indices=[0,1],target=[1])
    state = local_CP(atom_state=state,phi = pi*.25,indices=[0,1],target =[1],control = [0])
    state = local_H(atom_state = state, indices = [2])
    state.gate[[3]] = move.Move(state.gate[[0]])
    #state = local_CS(atom_state = state, indices = [2,3], target=[2])
    state = local_CP(atom_state=state,phi = pi*.5,indices=[2,3],target =[2],control = [3])
    state = local_H(atom_state=state, indices=[3])

    return state

@move.vmove()
def answer_3():
    return 0

@move.vmove()
def answer_4():
    q = move.NewQubitRegister(9)
    state = move.Init(qubits=[q[0],q[3],q[6],q[4],q[7],q[1],q[5],q[8],q[2]], indices=[0,1,2,3,4,5,6,7,8])
    state.gate[[0,1,2,4,6,8,10,12,14]] = move.Move(state.storage[[0,1,2,3,4,5,6,7,8]])
    state = local_H(state,[1,2])
    state = move.GlobalCZ(state)
    state.gate[[3]] = move.Move(state.gate[[0]])
    state = move.GlobalCZ(state)
    state = local_H(state,[3,4,6,8])
    state.gate[[5,7,9]] = move.Move(state.gate[[1,2,3]])
    state = move.GlobalCZ(state)
    state = local_H(state,[4,6,8,10,12,14])
    state.gate[[11,13,15]] = move.Move(state.gate[[5,7,9]])
    state = move.GlobalCZ(state)
    state = local_H(state,[10,12,14])
    return state

@move.vmove()
def answer_5():
    q = move.NewQubitRegister(7)
    state = move.Init(qubits=[q[0],q[1],q[2],q[4],q[5],q[6],q[3]], indices=[0,1,2,3,4,5,6])
    state.gate[[0,1,4,5,8,9,12]] = move.Move(state.storage[[0,1,2,3,4,5,6]])
    state = local_H(state,[0,1,4,5,8,12])
    state = move.GlobalCZ(state)
    state.gate[[5,6,13]] = move.Move(state.gate[[0,5,8]])
    state = move.GlobalCZ(state)
    state.gate[[6,8]] = move.Move(state.gate[[5,6]])
    state.gate[[0]] = move.Move(state.gate[[13]])
    state = move.GlobalCZ(state)
    state = local_H(state,[9])
    state.gate[[2,8,13]] = move.Move(state.gate[[1,4,8]])
    state = move.GlobalCZ(state)
    state.gate[[3,7]] = move.Move(state.gate[[9,12]])
    state = move.GlobalCZ(state)
    state = local_H(state,[0,3,6,13])
    return state