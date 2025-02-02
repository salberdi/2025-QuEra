from bloqade import move
from numpy import pi

@move.vmove()
def global_H(atom_state:move.core.AtomState):
    state = move.GlobalXY(atom_state=atom_state,x_exponent=-1/2,axis_phase_exponent=1.0)
    state = move.GlobalXY(atom_state=state,x_exponent=1,axis_phase_exponent=0.0)
    return state

@move.vmove()
def local_H(atom_state:move.core.AtomState,indices):
    state = move.GlobalXY(atom_state=atom_state,x_exponent=1/4,axis_phase_exponent=1/2)
    state = move.LocalRz(atom_state=state,phi=1,indices=indices)
    state = move.GlobalXY(atom_state=state,x_exponent=-1/4,axis_phase_exponent=1/2)
    return state

@move.vmove()
def local_CX(atom_state:move.core.AtomState,target_indices):
    state = local_H(atom_state=atom_state,indices=target_indices)
    state = move.GlobalCZ(atom_state=state)
    state = local_H(atom_state=state,indices=target_indices)
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
def local_T(atom_state:move.core.AtomState,indices, dag=False):
    state = move.LocalRz(atom_state=atom_state,phi=1/4 * (-1**dag),indices=indices)
    return state

@move.vmove()
def global_T(atom_state:move.core.AtomState):
    state = move.GlobalRz(atom_state=atom_state,phi=1/4)
    return state

@move.vmove()
def local_S(atom_state:move.core.AtomState,indices):
    state = move.LocalRz(atom_state=atom_state,phi=1/2,indices=indices)
    return state

@move.vmove()
def global_S(atom_state:move.core.AtomState):
    state = move.GlobalRz(atom_state=atom_state,phi=1/2)
    return state

@move.vmove()
def local_HTH(atom_state:move.core.AtomState,indices, dag=False):
    theta = 1/4 * (-1**dag)
    state = local_RX(atom_state=atom_state,angle=theta,indices=indices)
    return state