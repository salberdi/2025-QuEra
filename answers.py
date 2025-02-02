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

    def one_to_two():
        state.gate[[0,1]] = move.Move(state.storage[[1,2]]) # 0 is 1, 1 is 2 
        state = move.GlobalCZ(atom_state=state)
        # state = local_HTH(atom_state=state, indices=[1], dag=True)
        # helper broken bc of type inference

        dag = True
        theta = pi/4 * (-1**dag)
        state = move.LocalXY(atom_state=state,x_exponent=theta, axis_phase_exponent = 0.0, indices=[1])

        
        state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])


    def zero_to_two():
        state.gate[[0, 1]] = move.Move(state.storage[[0, 2]]) 
        state = move.GlobalCZ(atom_state=state)
       # state = local_HTH(atom_state=state, indices=[1], dag=False)

        dag = False
        theta = pi/4 * (-1**dag)
        state = move.LocalXY(atom_state=state,x_exponent=theta, axis_phase_exponent = 0.0, indices=[1])

        
        state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])

    one_to_two()
    zero_to_two()
    one_to_two()
    zero_to_two()

    state.gate[[0,1]] = move.Move(state.storage[[0,1]])
    state = local_T(atom_state=state, indices=[1], dag=True)

    state = local_H(atom_state=state, indices=[1])
    state = move.GlobalCZ(atom_state=state)
    #state = local_HTH(atom_state=state, indices=[1], dag=True)

    dag = True
    theta = pi/4 * (-1**dag)
    state = move.LocalXY(atom_state=state,x_exponent=theta, axis_phase_exponent = 0.0, indices=[1])

    state = move.GlobalCZ(atom_state=state)

    state = move.local_S(atom_state=state, indices=[1])
    state = move.local_T(atom_state=state, indices=[0])

    return state


@move.vmove()
def answer_2():
    return 0

@move.vmove()
def answer_3():
    return 0

@move.vmove()
def answer_4():
    return 0

@move.vmove()
def answer_5():
    return 0