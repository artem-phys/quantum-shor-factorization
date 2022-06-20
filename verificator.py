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
        print('Verification result: FAIL')
    elif N != p * q:
        print('N != p * q')
        print('Verification result: FAIL')
    else:
        print(f'{N} == {p} * {q}')
        print('Verification result: PASS')
