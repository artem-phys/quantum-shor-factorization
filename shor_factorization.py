from math import gcd, ceil
import numpy as np

from qof import qof


def shor_factorization(N, max_attempts=10):

    # Case N is even
    if N % 2 == 0:
        return 2, N // 2

    # Case N is prime power
    for b in range(2, ceil(np.log2(N))):
        a = N ** (1 / b)
        if a == int(a):
            return int(a), N // int(a)

    for attempt in range(max_attempts):
        print(f'Attempt {attempt}')

        # Chose random a value
        a = np.random.randint(2, N)
        while gcd(a, N) != 1:
            a = (a + 1) % N
        print(f'a = {a}')

        # Quantum order finding algorithm - take only one shot
        r_list = qof(a, N, 0.9, 10)
        print(f'r = {r_list}')

        for r in r_list:
            # Check if r is really period and also good value for shor factorization algorithm
            if r != 0 and r % 2 == 0 and (a ** (r / 2) + 1) % N != 0 and a ** r % N == 1:
                print(f'r = {r}')

                guesses = [gcd(a ** (r // 2) - 1, N), gcd(a ** (r // 2) + 1, N)]

                # Test guesses
                for guess in guesses:
                    if guess != 1 and guess != N and N % guess == 0:
                        return guess, N // guess

    else:
        return 1, N
