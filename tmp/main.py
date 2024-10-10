import sys
import random
from enum import Enum

# Global variable for bit size
B = 0

class OperationType(Enum):
    NOT = 'NOT'
    LEFT_SHIFT = 'LEFT_SHIFT'
    RIGHT_SHIFT = 'RIGHT_SHIFT'
    AND = 'AND'
    OR = 'OR'
    XOR = 'XOR'
    SUM = 'SUM'
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

class Node:
    def __init__(self, operation, node_id):
        self.operation = operation
        self.node_id = node_id
        self.inputs = []
        self.value = 0  # Initialize with 0 instead of None

    def reverse(self):
        if self.operation == OperationType.NOT:
            return [[self.value], [~self.value & ((1 << B) - 1)]]
        elif self.operation == OperationType.LEFT_SHIFT:
            return [[self.value >> 1]]
        elif self.operation == OperationType.RIGHT_SHIFT:
            return [[self.value << 1 & ((1 << B) - 1)]]
        elif self.operation == OperationType.AND:
            return [(x, self.value) for x in range(1 << B)]
        elif self.operation == OperationType.OR:
            return [(x, self.value) for x in range(self.value + 1)]
        elif self.operation == OperationType.XOR:
            return [(x, self.value ^ x) for x in range(1 << B)]
        elif self.operation == OperationType.SUM:
            return [(x, (self.value - x) & ((1 << B) - 1)) for x in range(1 << B)]
        else:
            return []

def binary_to_int(b_str):
    return int(b_str, 2)

def int_to_binary(n, bits):
    return format(n, f'0{bits}b')

def solve_circuit(nodes, target):
    nodes[-1].value = target
    for i in range(len(nodes) - 1, -1, -1):
        node = nodes[i]
        if node.operation == OperationType.INPUT:
            continue
        possible_values = node.reverse()
        if possible_values:
            choice = random.choice(possible_values)
            for j, input_node in enumerate(node.inputs):
                input_node.value = choice[j]
    return [node.value for node in nodes if node.operation == OperationType.INPUT]

def main():
    global B
    B = int(sys.stdin.readline().strip())
    S = binary_to_int(sys.stdin.readline().strip())
    N = int(sys.stdin.readline().strip())

    nodes = []
    for i in range(N):
        parts = sys.stdin.readline().strip().split()
        operation = OperationType(parts[0])
        node = Node(operation, int(parts[1]))
        if operation != OperationType.INPUT:
            node.inputs = [nodes[int(parts[3])]]
            if operation not in [OperationType.NOT, OperationType.LEFT_SHIFT, OperationType.RIGHT_SHIFT, OperationType.OUTPUT]:
                node.inputs.append(nodes[int(parts[4])])
        nodes.append(node)

    inputs = solve_circuit(nodes, S)
    for inp in inputs:
        sys.stdout.write(int_to_binary(inp, B) + '\n')
    sys.stdout.flush()

if __name__ == "__main__":
    main()
