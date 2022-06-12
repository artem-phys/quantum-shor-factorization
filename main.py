import json

from shor_factorization import shor_factorization

with open('input.json') as fin:
    input_data = json.load(fin)

    N = input_data['N']
    max_attempts = input_data['max_attempts']

    p, q = shor_factorization(N, max_attempts)

    print(f'Factors found for N = {N}')
    print(f'{N} = {p} * {q}')

with open('output.json', 'w') as fout:
    json.dump({'p': p, 'q': q}, fout)
