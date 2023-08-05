T = int(input())

while T:
    N_str, M_str = input().split(' ')
    N, M = int(N_str), int(M_str)

    cont_command_R = []
    cont_command_C = []
    lomd = 0 # lighting on the main diagonal
    cont_command_D = 0

    while M:
        # input the command
        try:
            command, x = input().split(' ')
        except ValueError:
            command = 'D'

        # command R
        if command == 'R':
            if x not in cont_command_R:
                cont_command_R.append(x)
                if x in cont_command_C:
                    lomd -= 1
                else:
                    lomd += 1

            else:
                cont_command_R.remove(x)
                if x in cont_command_C:
                    lomd += 1
                else:
                    lomd -= 1

        # command C
        elif command == 'C':
            if x not in cont_command_C:
                cont_command_C.append(x)
                if x in cont_command_R:
                    lomd -= 1
                else:
                    lomd += 1

            else:
                cont_command_C.remove(x)
                if x in cont_command_R:
                    lomd += 1
                else:
                    lomd -= 1

        # command D
        elif command == 'D':
            cont_command_D += 1


        lighting = N*(len(cont_command_R) + len(cont_command_C)) - 2*(len(cont_command_R)*len(cont_command_C))\
            + (cont_command_D % 2)*(N - 2*lomd)

        print(lighting)

        M -= 1

    T -= 1