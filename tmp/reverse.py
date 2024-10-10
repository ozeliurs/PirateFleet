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
        self.value = None

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
