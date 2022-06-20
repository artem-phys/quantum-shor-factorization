import numpy as np
from math import gcd, ceil
from fractions import Fraction

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit.library import QFT
from qiskit.extensions import UnitaryGate


def c_amodn(a, x, N):
    """Controlled multiplication by a mod N repeated x times"""

    if gcd(a, N) != 1:
        raise ValueError(f'a = {a} and N = {N} are not co-prime')

    L = ceil(np.log2(N))
    n_states = 2 ** L

    # Classical modular exponentiation
    outputs = np.zeros(n_states)
    for y in range(n_states):
        if y < N:
            outputs[y] = (y * a ** x) % N
        else:
            outputs[y] = y

    # Unitary matrix building by columns
    U = np.zeros((n_states, n_states), dtype=int)
    for y in range(n_states):
        for i in range(n_states):
            U[i][y] = 1 if outputs[y] == i else 0

    # Controlled
    c_U = UnitaryGate(U, label=f'{a}^{x} mod {N}').control()

    return c_U


def qof(a, N, eps, shots):

    L = ceil(np.log2(N))

    t = 2 * L + 1 + ceil(np.log(2 + 1 / (2 * eps)))
    qc = QuantumCircuit(t + L, t)

    # Initialize evaluation qubits
    for q in range(t):
        qc.h(q)

    # Auxiliary register in state |1>
    qc.x(t + L - 1)

    qc.barrier()

    # Controlled-U operations
    for q in range(t):
        qc.append(c_amodn(a, 2 ** q, N), [q] + list(range(t, t + L)))

    # Do inverse-QFT
    qc.barrier()
    inverse_QFT_gate = QFT(t, inverse=True, name='  IQFT').to_gate()
    qc.append(inverse_QFT_gate, range(t))

    print(qc)
    # Measure circuit
    qc.measure(range(t), range(t))

    # Simulate
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(transpile(qc, backend), shots=shots, memory=True)

    counts = job.result().get_memory()

    guess_list = []
    for output in counts:
        decimal = int(output, 2)
        phase = decimal / (2 ** t)
        frac = Fraction(phase).limit_denominator(N)
        guess_list.append(frac.denominator)

    return guess_list
