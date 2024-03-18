from mgu import most_general_unifier

def first_order_logical_resolution_recursion(clauses_list: list, memo: list) -> list:
    for i in range(len(clauses_list)):
        for j in range(i+1, len(clauses_list)):
            for m in range(len(clauses_list[i])):
                for n in range(len(clauses_list[j])):
                    atomic_rule1 = clauses_list[i][m]
                    atomic_rule2 = clauses_list[j][n]
                    try:
                        mgu_res = most_general_unifier(atomic_rule1, atomic_rule2)
                    except:
                        continue
                    memo.append(f'{i+1}{m+1} {j+1}{n+1}: {mgu_res}')
    print(clauses_list)
    print(memo)


def first_order_logical_resolution(clauses_set: set) -> list:
    memo = []
    clauses_list = list(clauses_set)
    clauses_list.sort()
    return first_order_logical_resolution_recursion(clauses_list, memo)


def main():

    import re

    # num = int(input('Enter the number of clauses: '))
    num = 4
    clause_exm = [
        'GradStudent(sue)',
        '(¬GradStudent(x), Student(x))',
        '(¬Student(x), HardWorker(x))',
        '¬HardWorker(sue)'
    ]


    # input pattern1: '(A(x), B(a, y))' -> ('A(x)', 'B(a, y)')
    clause_pattern1 = re.compile(r'\((.+)\)')
    # input pattern2: 'A(x)' -> ('A(x)',)
    clause_pattern2 = re.compile(r'¬?~?([A-Za-z][A-Za-z0-9_]*)\((.*)\)')

    clauses_set = set()

    for i in range(num):
        # clause = input(f'Enter clause {i + 1}: ')
        clause = clause_exm[i]
        if clause_pattern1.match(clause):
            clause = tuple(arg.strip() for arg in clause_pattern1.match(clause).group(1).split(','))
        elif clause_pattern2.match(clause):
            clause = (clause,)
        else:
            raise ValueError('The clause is not in a valid form.')

        clauses_set.add(clause)

    # print(clauses_set)

    first_order_logical_resolution(clauses_set)

if __name__ == '__main__':
    main()
