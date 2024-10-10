import sys
import io
import signal
import time

# The code to test (your original script)
code_to_test = """
import sys
import itertools

def left_shift(x):
    return (x << 1) & ((1 << B) - 1)

def right_shift(x):
    return x >> 1

def simulate_circuit(inputs, nodes, B):
    operations = {
        'NOT': lambda x: ~x & ((1 << B) - 1),
        'LEFT_SHIFT': left_shift,
        'RIGHT_SHIFT': right_shift,
        'AND': lambda x, y: x & y,
        'OR': lambda x, y: x | y,
        'XOR': lambda x, y: x ^ y,
        'SUM': lambda x, y: (x + y) & ((1 << B) - 1)
    }

    values = {idx: value for idx, value in enumerate(inputs)}
    for op, idx, *args in nodes:
        if op == 'INPUT':
            continue
        elif op == 'OUTPUT':
            return values[args[0]]
        elif op in operations:
            values[idx] = operations[op](*[values[arg] for arg in args])
    return values[nodes[-1][1]]  # Return the value of the OUTPUT node

def find_inputs(B, S, nodes):
    input_count = sum(1 for node in nodes if node[0] == 'INPUT')
    for inputs in itertools.product(range(1 << B), repeat=input_count):
        if simulate_circuit(inputs, nodes, B) == S:
            return inputs
    return None

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\\n'))

B = int(lines[0])
S = int(lines[1], 2)
N = int(lines[2])
nodes = []
for line in lines[3:]:
    parts = line.split()
    op = parts[0]
    idx = int(parts[1])
    args = list(map(int, parts[3:]))
    nodes.append((op, idx, *args))

# Find inputs
result = find_inputs(B, S, nodes)

# Print result
if result:
    for input_value in result:
        print(f"{input_value:0{B}b}")
else:
    print("No solution found", file=sys.stderr)
"""

# Test input
test_input = """16
0011111111101011
15
INPUT 0
INPUT 1
INPUT 2
INPUT 3
INPUT 4
INPUT 5
INPUT 6
LEFT_SHIFT 7 - 4
SUM 8 - 5 3
OR 9 - 0 1
XOR 10 - 2 6
AND 11 - 7 10
SUM 12 - 8 9
OR 13 - 11 12
OUTPUT 14 - 13
"""

# Expected output
expected_output = """1110010001001100
1000111101100001
1101100100000100
1000001000111011
0000101100001100
1011111000111011
0000001111001111
"""

# Timeout handler
def timeout_handler(signum, frame):
    raise TimeoutError("Code execution took more than 2 seconds")

# Redirect stdin and stdout
sys.stdin = io.StringIO(test_input)
sys.stdout = io.StringIO()

# Set up the timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(2)  # 2 second timeout

try:
    # Run the code
    start_time = time.time()
    exec(code_to_test)
    end_time = time.time()

    # Cancel the alarm
    signal.alarm(0)

    # Get the output
    actual_output = sys.stdout.getvalue()

    # Compare the actual output with the expected output
    if actual_output.strip() == expected_output.strip():
        print("Test passed! The output matches the expected output.")
    else:
        print("Test failed. The output does not match the expected output.")
        print("Expected output:")
        print(expected_output)
        print("Actual output:")
        print(actual_output)

    print(f"Execution time: {end_time - start_time:.2f} seconds")

except TimeoutError as e:
    print(f"Test failed: {e}")

except Exception as e:
    print(f"An error occurred during execution: {e}")

finally:
    # Reset stdin and stdout
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
