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
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = local_CX(atom_state=state,target_indices=target_indices)
        return state
    return kernel

def do_U3(a:float, b:float, c:float, indices:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state, phi=a, indices=indices)
        state = move.LocalXY(atom_state=state, x_exponent=b,axis_phase_exponent=pi/2, indices=indices)
        state = move.LocalRz(atom_state=state, phi=c, indices=indices)
        return state
    return kernel

def do_CZ(target_indices:list[int]):
    @move.vmove()
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
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def do_Z(indices:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=pi,indices=indices)
        return state
    return kernel

def do_Rx(angle:float, indices:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=0.0,indices=indices)
        return state
    return kernel

def do_Ry(angle:float, indices:list[int]):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=angle,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def do_Rz(angle:float, indices:list[int]):
    @move.vmove()
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
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalRz(atom_state=state,phi=pi/4,indices=indices)
        return state
    return kernel

def do_sqrtX(indices:list[int], dag):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**dag,axis_phase_exponent=0.0,indices=indices)
        return state
    return kernel

def do_sqrtY(indices:list[int], dag):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**dag,axis_phase_exponent=pi/2,indices=indices)
        return state
    return kernel

def join_ops(op1, op2):
    @move.vmove()
    def kernel(state:move.core.AtomState):
        state = op1(state)
        state = op2(state)
        return state
    return kernel


def storage_to_gate2(start:list[int],end:list[int]):
    return f'state.gate[{end}] = move.Move(state.storage[{start}])'

def gate_to_storage2(start:list[int],end:list[int]):
    return f'state.storage[{end}] = move.Move(state.gate[{start}])'

def do_H2(indices:list[int]):
    if type(indices) == int:
        indices = [indices]
    return f'state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)' + "\n" + \
    f'state = move.LocalRz(atom_state=state,phi=pi,indices={list(indices)})' + "\n" + \
    f'state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)'
    # return f'state = local_H(atom_state=state,indices={indices})'

def do_CX2(target_indices:list[int]):
    if type(target_indices) == int:
        target_indices = [target_indices]
    return f'state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)' + "\n" + \
    f'state = move.LocalRz(atom_state=state,phi=pi,indices={target_indices})' + "\n" + \
    f'state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)' + "\n" + \
    f'state = move.GlobalCZ(atom_state=state)' + "\n" + \
    f'state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)' + "\n" + \
    f'state = move.LocalRz(atom_state=state,phi=pi,indices={target_indices})' + "\n" + \
    f'state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)'
    # return f'state = local_CX(atom_state=state,target_indices={target_indices})'

def do_U32(theta:float, phi:float, lmda:float, indices:list[int]):
    return f'state = move.LocalRz(atom_state=state, phi={lmda}*pi, indices={indices})' + "\n" + \
    f'state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices={indices})' + "\n" + \
    f'state = move.LocalRz(atom_state=state, phi=({theta}*pi) + pi, indices={indices})' + "\n" + \
    f'state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices={indices})' + "\n" + \
    f'state = move.LocalRz(atom_state=state, phi=({phi}*pi) + pi, indices={indices})'

def do_CZ2(target_indices:list[int]):
    return f'state = move.GlobalCZ(atom_state=state)'

def do_X2(indices:list[int]):
    return f'state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=0.0,indices={indices})'

def do_Y2(indices:list[int]):
    return f'state = move.LocalXY(atom_state=state,x_exponent=pi,axis_phase_exponent=pi/2,indices={indices})'

def do_Z2(indices:list[int]):
    return f'state = move.LocalRz(atom_state=state,phi=pi,indices={indices})'

def do_Rx2(angle:float, indices:list[int]):
    return f'state = move.LocalXY(atom_state=state,x_exponent={angle}*pi,axis_phase_exponent=0.0,indices={indices})'

def do_Ry2(angle:float, indices:list[int]):
    return f'state = move.LocalXY(atom_state=state,x_exponent=-{angle}*pi,axis_phase_exponent=pi/2,indices={indices})'

def do_Rz2(angle:float, indices:list[int]):
    return f'state = move.LocalRz(atom_state=state,phi={angle}*pi,indices={indices})'

def do_S2(indices:list[int]):
    return f'state = move.LocalRz(atom_state=state,phi=pi/2,indices={indices})'

def do_T2(indices:list[int]):
    return f'state = move.LocalRz(atom_state=state,phi=pi/4,indices={indices})'

def do_sqrtX2(indices:list[int], dag):
    return f'state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**{dag},axis_phase_exponent=0.0,indices={indices})'

def do_sqrtY2(indices:list[int], dag):
    return f'state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**{dag},axis_phase_exponent=pi/2,indices={indices})'