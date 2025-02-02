from helper_functions import *
from bloqade import move
from numpy import pi

def storage_to_gate(start:list[int],end:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state.gate[end] = move.Move(state.storage[start])
        return state
    return kernel

def gate_to_storage(start:list[int],end:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state.storage[end] = move.Move(state.gate[start])
        return state
    return kernel

def do_H(indices:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = local_H(atom_state=state,indices=indices)
        return state
    return kernel

def do_CX(target_indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = local_CX(atom_state=state,target_indices=target_indices)
        return state
    return kernel

def do_U3(a:float, b:float, c:float, indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state, phi=a, indices=indices)
        state = move.LocalXY(atom_state=state, x_exponent=b,axis_phase_exponent=pi/2, indices=indices)
        state = move.LocalRz(atom_state=state, phi=c, indices=indices)
        return state
    return kernel

def do_CZ(target_indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.GlobalCZ(atom_state=state)
        return state
    return kernel

def do_X(indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0,indices=indices)
        return state
    return kernel

def do_Y(indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def do_Z(indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=pi,indices=indices)
        return state
    return kernel

def do_Rx(angle:float, indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=0.0,indices=indices)
        return state
    return kernel

def do_Ry(angle:float, indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def do_Rz(angle:float, indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=angle,indices=indices)
        return state
    return kernel

def do_S(indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=pi/2,indices=indices)
        return state
    return kernel

def do_T(indices:list[int]):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=pi/4,indices=indices)
        return state
    return kernel

def do_sqrtX(indices:list[int], dag):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**dag,axis_phase_exponent=0.0,indices=indices)
        return state
    return kernel

def do_sqrtY(indices:list[int], dag):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**dag,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def join_ops(op1, op2):
    @move.vmove
    def kernel(state:move.core.AtomState):
        state = op1(state)
        state = op2(state)
        return state
    return kernel