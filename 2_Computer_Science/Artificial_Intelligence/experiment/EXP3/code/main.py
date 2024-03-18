from mgu import most_general_unifier, UnificationError 


def first_order_logical_resolution(clauses_set: set) -> None:

    import re

    clauses_list = list(clauses_set)
    clauses_list.sort()

    step_record = [clauses_list,]
    step = 0

    generate_record = {}

    while True:
        step_record.append([])
        step += 1

        for i in range(len(step_record[step-1])):
            for s in range(step):
                for j in range(len(step_record[s])):
                    # find a pair of clauses to resolve
                    clause1 = step_record[step-1][i]
                    clause2 = step_record[s][j]
                    for m in range(len(clause1)):
                        for n in range(len(clause2)):
                            atomic_rule1 = clause1[m]
                            atomic_rule2 = clause2[n]
                            if not ((atomic_rule1.startswith('~') ^ atomic_rule2.startswith('~')) or
                                    (atomic_rule1.startswith('¬') ^ atomic_rule2.startswith('¬'))):
                                continue
                            try:
                                mgu_res = most_general_unifier(atomic_rule1, atomic_rule2)
                            except UnificationError:
                                continue
                            new_clause = list(clause1 + clause2)
                            new_clause.remove(atomic_rule1)
                            new_clause.remove(atomic_rule2)

                            # substitute the variable in the clause
                            for var, value in mgu_res.items():
                                new_clause = [re.sub(r'\b' + var + r'\b', value, clause) for clause in new_clause]
                            
                            # remove duplicate
                            new_temp = list(set(new_clause))
                            new_temp.sort(key=lambda x: new_clause.index(x))
                            new_clause = tuple(new_temp)

                            # check if the new clause is already in the record
                            for k in range(step+1):
                                for l in range(len(step_record[k])):
                                    if step_record[k][l] == new_clause:
                                        break
                                else:
                                    continue
                                break
                            else: # if the new clause is not in the record
                                step_record[step].append(new_clause)
                                generate_record[new_clause] = (step-1, i, m, s, j, n, mgu_res)

                            # if the new_clause is an empty clause, then the resolution is done
                            if new_clause == ():
                                resolution_path = []
                                temp_queue = [()]
                                while temp_queue:
                                    temp = temp_queue.pop(0)
                                    if temp in generate_record:

                                        s1, i, m, s2, j, n, mgu_res = generate_record[temp]

                                        parent_clause1 = step_record[s1][i]
                                        parent_clause2 = step_record[s2][j]

                                        temp_queue.append(parent_clause1)
                                        temp_queue.append(parent_clause2)

                                        # the way to print the resolution path, you can adjust it by yourself
                                        parent_clause1_str = ', '.join([f'\033[92m{clause}\033[0m' if i != m else f'\033[91m{clause}\033[0m' for i, clause in enumerate(parent_clause1)])
                                        parent_clause2_str = ', '.join([f'\033[92m{clause}\033[0m' if j != n else f'\033[91m{clause}\033[0m' for j, clause in enumerate(parent_clause2)])
                                        var_assign_str     = ', '.join([f'\033[94m{key} = {value}\033[0m' for key, value in mgu_res.items()])
                                        temp_str           = f'\033[93m{temp}\033[0m'
                                        resolution_path.append(f'({parent_clause1_str}) + ({parent_clause2_str}) [{var_assign_str}] => {temp_str}')

                                resolution_path = resolution_path[::-1]

                                for clause in resolution_path:
                                    print(clause)
                                return

        if step_record[step] == []:
            print('Do not have a resolution path.')
            return


def ResolutionFOL() -> None:

    import re

    # input:

    # num: the number of clauses.

    # clauses input pattern:
    # input pattern1 example: (A(x, b), B(a, y))
    # input pattern2 example: A(x)

    num = int(input())

    clause_pattern1 = re.compile(r'\(([¬~]?[A-Z][A-Za-z0-9_]*\(.*\)[ ]?[,]?[ ]?)*\)')
    clause_pattern2 = re.compile(r'[¬~]?[A-Z][A-Za-z0-9_]*\(.*\)')

    clauses_set = set()

    for i in range(num):
        clause = input()
        if clause_pattern1.match(clause):
            # ungreedy match
            atomic_clauses = re.findall(r'¬?[A-Z][A-Za-z0-9_]*\(.*?\)', clause)
            clause = tuple(atomic_clauses)
        elif clause_pattern2.match(clause):
            clause = (clause,)
        else:
            raise ValueError('The clause is not in a valid form.')

        clauses_set.add(clause)

    first_order_logical_resolution(clauses_set)


def test1():
    num = 4
    clause_exm = [
        'GradStudent(sue)',
        '(¬GradStudent(x), Student(x))',
        '(¬Student(x), HardWorker(x))',
        '¬HardWorker(sue)'
    ]

    import io
    import sys

    print('num:', num)
    print('clauses:')
    for clause in clause_exm:
        print(clause)

    sys.stdin = io.StringIO(f'{num}\n' + '\n'.join(clause_exm) + '\n')

def test2():
    num = 11
    clause_exm = [
        'A(tony)',
        'A(mike)',
        'A(john)',
        'L(tony, rain)',
        'L(tony, snow)',
        '(¬A(x), S(x), C(x))',
        '(¬C(y), ¬L(y, rain))',
        '(L(z, snow), ¬S(z))',
        '(¬L(tony, u), ¬L(mike, u))',
        '(L(tony, v), L(mike, v))',
        '(¬A(w), ¬C(w), S(w))'
    ]

    import io
    import sys

    print('num:', num)
    print('clauses:')
    for clause in clause_exm:
        print(clause)

    sys.stdin = io.StringIO(f'{num}\n' + '\n'.join(clause_exm) + '\n')


if __name__ == '__main__':
    import sys

    print('-- First Order Logical Resolution --')

    print('-'*10 + 'Test 1' + '-'*10)
    test1()
    ResolutionFOL()

    sys.stdin = sys.__stdin__

    print('-'*10 + 'Test 2' + '-'*10)
    test2()
    ResolutionFOL()

    sys.stdin = sys.__stdin__
