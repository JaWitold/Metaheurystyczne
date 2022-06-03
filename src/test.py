import numpy as np

def main():
    t1 = np.array([1,2,3,4,5,6,7,8,9])
    t2 = np.array([9,1,2,3,4,5,6,7,8])
    dimension = 4
    cycle1 = []
    cycle2 = []
    parent1 = t1.tolist()
    parent2 = t2.tolist()
    first = parent1[0]
    first_index = parent1.index(first)
    print(first_index)
    cycle1.append(first)
    second = -1
    while second != cycle1[0]:
        second = parent2[first_index]
        first_index = parent1.index(second)
        first = parent1[first_index]
        cycle1.append(first)
    cycle1 = cycle1[:len(cycle1)-1]
    print(cycle1)

    first = parent1[1]
    first_index = parent1.index(first)
    print(first_index)
    cycle2.append(first)
    second = -1
    while second != cycle2[0]:
        second = parent2[first_index]
        first_index = parent1.index(second)
        first = parent1[first_index]
        cycle2.append(first)
    cycle2 = cycle2[:len(cycle2)-1]
    print(cycle2)

    child1 = parent1[:]
    child2 = parent2[:]

    for element in cycle2:
        index = parent2.index(element)
        child1[index] = element
    print(child1)

    for element in cycle2:
        index = parent1.index(element)
        child2[index] = element
    print(child2)
if __name__ == '__main__':
    main()