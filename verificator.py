import json

with open('input.json') as fin:
    input_data = json.load(fin)

    N = input_data['N']
    max_attempts = input_data['max_attempts']

with open('output.json') as fout:
    output_data = json.load(fout)

    p = output_data['p']
    q = output_data['q']

    if p == 1 or q == 1:
        print('Factors are trivial')
        print('Program is NOT OK')
    elif N != p * q:
        print('N != p * q')
        print('Program is NOT OK')
    else:
        print(f'{N} == {p} * {q}')
        print('Program is OK')
