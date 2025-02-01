from bloqade import move
from numpy import pi

def global_H(state:move.core.AtomState):
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=1.0)
    state = move.GlobalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0)
    return state

def local_H(state:move.core.AtomState, indices):
    state = move.LocalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=1.0,indices=indices)
    state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0,indices=indices)
    return state

def local_CX(state:move.core.AtomState,target_indices):
    state = local_H(atom_state=state,indices=[target_indices])
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state,indices=[target_indices])
    return state

def global_RX(state:move.core.AtomState,angle,target_indices):
    state = move.GlobalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=0,indices=indices)
    return state

def local_RX(state:move.core.AtomState,angle,target_indices):
    state = move.LocalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=0,indices=indices)
    return state