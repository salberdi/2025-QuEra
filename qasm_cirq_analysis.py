from iquhack_scoring import MoveScorer
from bloqade import move
from matplotlib.animation import FuncAnimation, PillowWriter
from numpy import pi
from helper_functions import *
import numpy as np
import cirq
from cirq.contrib.qasm_import import circuit_from_qasm
import re
import copy
from math import floor
from circ_builder_helpers import *

f_name = "QAOA_qasm_str.txt"
with open(f_name, "r") as f:
    prog = f.read()
# print(prog)

circ = circuit_from_qasm(prog)

n_qubits = len(circ.moments[0].qubits)

regen = False
do_print = False
run = True

if regen:
    all_moment_ops = []
    all_op_qubits = []
    for i, moment in enumerate(circ.moments):
        # names of operators
        moment_ops = []
        # numbers of qubits corresponding to moment_ops
        op_qubits = [[] for i in range(n_qubits)]
        # op_qubits = np.zeros((len(moment.operations), 0))
        # loops through all operators
        for j, op1 in enumerate(moment.operations):
            # if operator is not in moment_ops, add it and add self to op_qubits, else, add self to op_qubits
            if str(op1.gate) not in moment_ops:
                moment_ops.append(str(op1.gate))
            for k, qubit in enumerate(op1.qubits):
                op_qubits[moment_ops.index(str(op1.gate))].append(int(qubit.name[2:]))
    
        for j in range(len(moment_ops)):
            all_moment_ops.append(moment_ops[j])
            if moment_ops[j] == "CNOT":
                all_op_qubits.append(op_qubits[j])
            else:
                op_qubits[j].sort()
                all_op_qubits.append(op_qubits[j])
    
    if do_print:
        for i in range(len(all_moment_ops)):
            print(f'{i}: op: {all_moment_ops[i]}, qubits: {all_op_qubits[i]}')
    
    # This is the worst code I've ever written and I feel like throwing up just looking at it
    
    n_ops = len(all_moment_ops)
    na_ops = []
    for i, op in enumerate(all_moment_ops):
    
        # move qubits to gate area
        if op == "CNOT":
            qbs = copy.deepcopy(all_op_qubits[i])
            qbs.sort()
            na_ops.append(storage_to_gate2(qbs, [0, 1]))
        else:
            na_ops.append(storage_to_gate2(all_op_qubits[i], all_op_qubits[i]))
    
        # do gate
        if op == "H":
            na_ops.append(do_H2(indices=all_op_qubits[i]))
        elif "QasmUGate" in op:
            theta, phi, lmda = re.findall(r"[-+]?(?:\d*\.*\d+)", op)
            na_ops.append(do_U32(theta, phi, lmda, indices=all_op_qubits[i]))
        elif op == "CNOT":
            if all_op_qubits[i][0] < all_op_qubits[i][1]:
                target = 1
            else:
                target = 0
            na_ops.append(do_CX2(target_indices=target))
        elif op == "X**0.5":
            na_ops.append(do_sqrtX2(indices=all_op_qubits[i],dag=False))
        elif op == "X**-0.5":
            na_ops.append(do_sqrtX2(indices=all_op_qubits[i],dag=True))
        elif op == "Y**0.5":
            na_ops.append(do_sqrtY2(indices=all_op_qubits[i],dag=False))
        elif op == "Y**-0.5":
            na_ops.append(do_sqrtY2(indices=all_op_qubits[i],dag=True))
        elif op == "S":
            na_ops.append(do_S2(indices=all_op_qubits[i]))
        elif op == "T":
            na_ops.append(do_T2(indices=all_op_qubits[i]))
        elif op[:2] == "Rx":
            angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
            na_ops.append(do_Rx2(angle,indices=all_op_qubits[i]))
        elif op[:2] == "Ry":
            angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
            na_ops.append(do_Ry2(angle,indices=all_op_qubits[i]))
        elif op[:2] == "Rz":
            angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
            na_ops.append(do_Rz2(angle,indices=all_op_qubits[i]))
    
        # move qubits back
        if op == "CNOT":
            qbs = copy.deepcopy(all_op_qubits[i])
            qbs.sort()
            na_ops.append(gate_to_storage2([0, 1], qbs))
        else:
            na_ops.append(gate_to_storage2(all_op_qubits[i], all_op_qubits[i]))
    
    # temp_op_arr = []
    # for i in range(0, floor(len(na_ops) / 2), 2):
    #     temp_op_arr.append(join_ops(na_ops[2 * i], na_ops[(2 * i)+1]))
    # if len(na_ops) % 2 == 1:
    #     temp_op_arr.append(na_ops[-1])
    
    # temp_op_arr2 = []
    # for i in range(floor(len(temp_op_arr) / 2)):
    #     temp_op_arr2.append(join_ops(temp_op_arr[2 * i], temp_op_arr[(2 * i)+1]))
    # if len(temp_op_arr) % 2 == 1:
    #     temp_op_arr2.append(temp_op_arr[-1])
    
    # temp_op_arr3 = []
    # for i in range(floor(len(temp_op_arr2) / 2)):
    #     temp_op_arr3.append(join_ops(temp_op_arr2[2 * i], temp_op_arr2[(2 * i)+1]))
    # if len(temp_op_arr2) % 2 == 1:
    #     temp_op_arr3.append(temp_op_arr2[-1])
    
    # temp_op_arr4 = []
    # for i in range(floor(len(temp_op_arr3) / 2)):
    #     temp_op_arr4.append(join_ops(temp_op_arr3[2 * i], temp_op_arr3[(2 * i)+1]))
    # if len(temp_op_arr3) % 2 == 1:
    #     temp_op_arr4.append(temp_op_arr3[-1])
    
    # temp_op_arr5 = []
    # for i in range(floor(len(temp_op_arr4) / 2)):
    #     temp_op_arr5.append(join_ops(temp_op_arr4[2 * i], temp_op_arr4[(2 * i)+1]))
    # if len(temp_op_arr4) % 2 == 1:
    #     temp_op_arr5.append(temp_op_arr4[-1])
    
    # temp_op_arr6 = []
    # for i in range(floor(len(temp_op_arr5) / 2)):
    #     temp_op_arr6.append(join_ops(temp_op_arr5[2 * i], temp_op_arr5[(2 * i)+1]))
    # if len(temp_op_arr5) % 2 == 1:
    #     temp_op_arr6.append(temp_op_arr5[-1])
    
    # temp_op_arr7 = []
    # for i in range(floor(len(temp_op_arr6) / 2)):
    #     temp_op_arr7.append(join_ops(temp_op_arr6[2 * i], temp_op_arr6[(2 * i)+1]))
    # if len(temp_op_arr6) % 2 == 1:
    #     temp_op_arr7.append(temp_op_arr6[-1])
    
    # temp_op_arr8 = []
    # for i in range(floor(len(temp_op_arr7) / 2)):
    #     temp_op_arr8.append(join_ops(temp_op_arr7[2 * i], temp_op_arr7[(2 * i)+1]))
    # if len(temp_op_arr7) % 2 == 1:
    #     temp_op_arr8.append(temp_op_arr8[-1])
    
    
    # print(len(temp_op_arr8))
    # print(temp_op_arr8)
    
    circ_string = "\n".join(na_ops)
    
    print(circ_string)
    
    print(len(na_ops))

indices = list(range(n_qubits))


@move.vmove()
def main():
    q = move.NewQubitRegister(4)
    
    state = move.Init(qubits=[q[0],q[1],q[2],q[3]], indices=[0,1,2,3])
    
    state.gate[[0, 1, 2, 3]] = move.Move(state.storage[[0, 1, 2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0, 1, 2, 3])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1, 2, 3]] = move.Move(state.gate[[0, 1, 2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1, 2, 3]] = move.Move(state.storage[[1, 2, 3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[1, 2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[1, 2, 3])
    state.storage[[1, 2, 3]] = move.Move(state.gate[[1, 2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalRz(atom_state=state, phi=0.25*pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=0.4223785852*pi,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.8276214148*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.3276214148*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalXY(atom_state=state,x_exponent=0.1766811937*pi,axis_phase_exponent=0.0,indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0, 1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0, 1])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2, 3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2, 3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2, 3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0, 1])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 1]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[0, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[0])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[0])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[0])
    state.storage[[0]] = move.Move(state.gate[[0]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 2]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalRz(atom_state=state, phi=0.75*pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1, 2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1, 2])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[1, 2]] = move.Move(state.storage[[1, 2]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**False,axis_phase_exponent=0.0,indices=[1, 2])
    state.storage[[1, 2]] = move.Move(state.gate[[1, 2]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[1, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[1])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[1])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=1.25*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.0*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[1])
    state.storage[[1]] = move.Move(state.gate[[1]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalXY(atom_state=state,x_exponent=0.3570808194*pi,axis_phase_exponent=0.0,indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=-0.5*pi,axis_phase_exponent=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[0])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalXY(atom_state=state,x_exponent=pi/2 * (-1)**True,axis_phase_exponent=0.0,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state,phi=pi/2,indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[0, 1]] = move.Move(state.storage[[2, 3]])
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state = move.GlobalCZ(atom_state=state)
    state = move.GlobalXY(atom_state=state,x_exponent=pi/4,axis_phase_exponent=pi/2)
    state = move.LocalRz(atom_state=state,phi=pi,indices=[1])
    state = move.GlobalXY(atom_state=state,x_exponent=-pi/4,axis_phase_exponent=pi/2)
    state.storage[[2, 3]] = move.Move(state.gate[[0, 1]])
    state.gate[[2]] = move.Move(state.storage[[2]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[2])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[2])
    state = move.LocalRz(atom_state=state, phi=(0.3929191806*pi) + pi, indices=[2])
    state.storage[[2]] = move.Move(state.gate[[2]])
    state.gate[[3]] = move.Move(state.storage[[3]])
    state = move.LocalRz(atom_state=state, phi=0.0*pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(0.5*pi) + pi, indices=[3])
    state = move.LocalXY(atom_state=state, x_exponent=pi/2,axis_phase_exponent=0.0, indices=[3])
    state = move.LocalRz(atom_state=state, phi=(1.8929191806*pi) + pi, indices=[3])
    state.storage[[3]] = move.Move(state.gate[[3]])
    state.gate[[2, 3]] = move.Move(state.storage[[2, 3]])
    state = move.LocalXY(atom_state=state,x_exponent=0.0931081293*pi,axis_phase_exponent=0.0,indices=[2, 3])
    state.storage[[2, 3]] = move.Move(state.gate[[2, 3]])
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(15):
    aggressive.Fold(move.vmove)(main)

expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3)]
qreg q[4];


h q[0];
h q[1];
h q[2];
h q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[1];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

rx(pi*0.1766811937) q[0];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[2];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.4223785852) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[2];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

rx(pi*0.1766811937) q[1];
rx(pi*0.1766811937) q[2];
rx(pi*0.1766811937) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[1];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[2];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[2];

rx(pi*0.0931081293) q[0];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[2];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.3570808194) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[2];
u3(pi*0.5,pi*1.8929191806,0) q[3];

rx(pi*0.0931081293) q[1];
rx(pi*0.0931081293) q[2];
rx(pi*0.0931081293) q[3];
"""

if run:
    scorer = MoveScorer(main, expected_qasm)
    score = scorer.score()
    print(score)