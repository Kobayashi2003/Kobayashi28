import matplotlib.pyplot as plt


def findRoots(array : list):

    n = len(array)
    roots = []
    for i in range(n):
        if array[i] < 0:
            roots.append(i)

    for root in roots:
        drawSets(array, root)
    

def drawSets(array : list, root : int):

    n = len(array)
    nodes1 = []
    nodes2 = []
    nodes1.append(root)
    level = 0

    plt.figure(figsize=(10, 10))
    plt.title("Disjoint Sets")
    plt.plot([root], [level], 'o')
    plt.text(root, level+0.05, str(root), ha='center', va='bottom', fontsize=10)

    while nodes1 or nodes2:
        if abs(level) % 2 == 0:
            while nodes1:
                node = nodes1.pop()
                for i in range(n):
                    if array[i] == node:
                        nodes2.append(i)
                        plt.plot([node, i], [level, level-1], '-o')
                        plt.text(i, level-1+0.05, str(i), ha='center', va='bottom', fontsize=10)
        else:
            while nodes2:
                node = nodes2.pop()
                for i in range(n):
                    if array[i] == node:
                        nodes1.append(i)
                        plt.plot([node, i], [level, level-1], '-o')
                        plt.text(i, level-1+0.05, str(i), ha='center', va='bottom', fontsize=10)
        level -= 1
        print(nodes1, nodes2)

    xlabel = [ i for i in range(n) ]
    plt.xticks(xlabel)

    plt.grid()
    plt.show()


if __name__ == "__main__":
    array = [16, -4, 1, 1, 3, 3, 3, 1, 1, 8, 3, 3, 3, 3, 1, 14, 14]
    findRoots(array)