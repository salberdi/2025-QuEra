from bloqade import move
from numpy import pi

@move.vmove()
def global_H(state:move.core.AtomState):
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/2,axis_phase_exponent=1.0)
    state = move.GlobalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0)
    return state

@move.vmove()
def local_H(state:move.core.AtomState,indices):
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=indices)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    return state

@move.vmove()
def local_CX(state:move.core.AtomState,target_indices):
    state = local_H(state=state,indices=[target_indices])
    state = move.GlobalCZ(atom_state=state)
    state = local_H(state=state,indices=[target_indices])
    return state

@move.vmove()
def global_RX(atom_state:move.core.AtomState,angle):
    state = move.GlobalXY(atom_state=atom_state,x_exponent=angle,axis_phase_exponent=0)
    return state

@move.vmove()
def local_RX(atom_state:move.core.AtomState,angle,indices):
    state = move.LocalXY(atom_state=atom_state,x_exponent=angle,axis_phase_exponent=0,indices=indices)
    return state

@move.vmove()
def local_T(state:move.core.AtomState,indices):
    state = move.LocalRz(atom_state=state,phi=pi/4,indices=indices)
    return state

@move.vmove()
def global_T(state:move.core.AtomState):
    state = move.GlobalRz(atom_state=state,phi=pi/4)
    return state

@move.vmove()
def local_S(state:move.core.AtomState,indices):
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=indices)
    return state

@move.vmove()
def global_S(state:move.core.AtomState):
    state = move.GlobalRz(atom_state=state,phi=pi/2)
    return state