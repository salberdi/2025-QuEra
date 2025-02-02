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

do_print = True

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
        na_ops.append(storage_to_gate([0, 1], qbs))
    else:
        na_ops.append(storage_to_gate(all_op_qubits[i], all_op_qubits[i]))

    # do gate
    if op == "H":
        na_ops.append(do_H(indices=all_op_qubits[i]))
    elif "QasmUGate" in op:
        theta, phi, lmda = re.findall(r"[-+]?(?:\d*\.*\d+)", op)
        na_ops.append(do_U3(theta, phi, lmda, indices=all_op_qubits[i]))
    elif op == "CNOT":
        if all_op_qubits[i][0] < all_op_qubits[i][0]:
            target = 1
        else:
            target = 0
        na_ops.append(do_CX(target_indices=target))
    elif op == "X**0.5":
        na_ops.append(do_sqrtX(indices=all_op_qubits[i],dag=False))
    elif op == "X**-0.5":
        na_ops.append(do_sqrtX(indices=all_op_qubits[i],dag=True))
    elif op == "Y**0.5":
        na_ops.append(do_sqrtY(indices=all_op_qubits[i],dag=False))
    elif op == "Y**-0.5":
        na_ops.append(do_sqrtY(indices=all_op_qubits[i],dag=True))
    elif op == "S":
        na_ops.append(do_S(indices=all_op_qubits[i]))
    elif op == "T":
        na_ops.append(do_T(indices=all_op_qubits[i]))
    elif op[:2] == "Rx":
        angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
        na_ops.append(do_Rx(angle,indices=all_op_qubits[i]))
    elif op[:2] == "Ry":
        angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
        na_ops.append(do_Ry(angle,indices=all_op_qubits[i]))
    elif op[:2] == "Rz":
        angle = re.findall(r"[-+]?(?:\d*\.*\d+)", op)[0]
        na_ops.append(do_Rz(angle,indices=all_op_qubits[i]))

    # move qubits back
    if op == "CNOT":
        qbs = copy.deepcopy(all_op_qubits[i])
        qbs.sort()
        na_ops.append(gate_to_storage(qbs, [0, 1]))
    else:
        na_ops.append(gate_to_storage(all_op_qubits[i], all_op_qubits[i]))

temp_op_arr = []
for i in range(0, floor(len(na_ops) / 2), 2):
    temp_op_arr.append(join_ops(na_ops[2 * i], na_ops[(2 * i)+1]))
if len(na_ops) % 2 == 1:
    temp_op_arr.append(na_ops[-1])

temp_op_arr2 = []
for i in range(floor(len(temp_op_arr) / 2)):
    temp_op_arr2.append(join_ops(temp_op_arr[2 * i], temp_op_arr[(2 * i)+1]))
if len(temp_op_arr) % 2 == 1:
    temp_op_arr2.append(temp_op_arr[-1])

temp_op_arr3 = []
for i in range(floor(len(temp_op_arr2) / 2)):
    temp_op_arr3.append(join_ops(temp_op_arr2[2 * i], temp_op_arr2[(2 * i)+1]))
if len(temp_op_arr2) % 2 == 1:
    temp_op_arr3.append(temp_op_arr2[-1])

temp_op_arr4 = []
for i in range(floor(len(temp_op_arr3) / 2)):
    temp_op_arr4.append(join_ops(temp_op_arr3[2 * i], temp_op_arr3[(2 * i)+1]))
if len(temp_op_arr3) % 2 == 1:
    temp_op_arr4.append(temp_op_arr3[-1])

temp_op_arr5 = []
for i in range(floor(len(temp_op_arr4) / 2)):
    temp_op_arr5.append(join_ops(temp_op_arr4[2 * i], temp_op_arr4[(2 * i)+1]))
if len(temp_op_arr4) % 2 == 1:
    temp_op_arr5.append(temp_op_arr4[-1])

temp_op_arr6 = []
for i in range(floor(len(temp_op_arr5) / 2)):
    temp_op_arr6.append(join_ops(temp_op_arr5[2 * i], temp_op_arr5[(2 * i)+1]))
if len(temp_op_arr5) % 2 == 1:
    temp_op_arr6.append(temp_op_arr5[-1])

temp_op_arr7 = []
for i in range(floor(len(temp_op_arr6) / 2)):
    temp_op_arr7.append(join_ops(temp_op_arr6[2 * i], temp_op_arr6[(2 * i)+1]))
if len(temp_op_arr6) % 2 == 1:
    temp_op_arr7.append(temp_op_arr6[-1])

temp_op_arr8 = []
for i in range(floor(len(temp_op_arr7) / 2)):
    temp_op_arr8.append(join_ops(temp_op_arr7[2 * i], temp_op_arr7[(2 * i)+1]))
if len(temp_op_arr7) % 2 == 1:
    temp_op_arr8.append(temp_op_arr8[-1])


print(len(temp_op_arr8))
print(temp_op_arr8)

indices = list(range(n_qubits))


@move.vmove()
def main():
    q = move.NewQubitRegister(n_qubits)

    state = move.Init(qubits=q, indices=indices)

    state = temp_op_arr8[0](state)
    
    move.Execute(state)

from kirin.passes import aggressive
for passive in range(15):
    aggressive.Fold(move.vmove)(main)