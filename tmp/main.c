/*******
* Read input from STDIN
* Use: printf(...) or fprintf( stdout, ...) to output your result to stdout.
* Use: fprintf(stderr, ...);  to output debugging information to stderr.
* ***/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define MAX_NODES 1000

int B = 0;

typedef enum {
    NOT, LEFT_SHIFT, RIGHT_SHIFT, AND, OR, XOR, SUM, INPUT, OUTPUT
} OperationType;

typedef struct {
    OperationType operation;
    int node_id;
    int inputs[2];
    int input_count;
    unsigned int value;
} Node;

Node nodes[MAX_NODES];
int node_count = 0;

unsigned int binary_to_int(char* b_str) {
    return strtoul(b_str, NULL, 2);
}

void int_to_binary(unsigned int n, int bits, char* result) {
    for (int i = bits - 1; i >= 0; i--) {
        result[bits - 1 - i] = ((n >> i) & 1) ? '1' : '0';
    }
    result[bits] = '\0';
}

void reverse_node(Node* node, unsigned int** possible_values, int* count) {
    *count = 0;
    *possible_values = malloc(sizeof(unsigned int) * (1 << B) * 2);

    switch (node->operation) {
        case NOT:
            (*possible_values)[(*count)++] = node->value;
            (*possible_values)[(*count)++] = ~node->value & ((1 << B) - 1);
            break;
        case LEFT_SHIFT:
            (*possible_values)[(*count)++] = node->value >> 1;
            break;
        case RIGHT_SHIFT:
            (*possible_values)[(*count)++] = (node->value << 1) & ((1 << B) - 1);
            break;
        case AND: case OR: case XOR: case SUM:
            for (unsigned int x = 0; x < (1 << B); x++) {
                unsigned int y;
                switch (node->operation) {
                    case AND: y = node->value; break;
                    case OR:  y = node->value; if (x > node->value) continue; break;
                    case XOR: y = node->value ^ x; break;
                    case SUM: y = (node->value - x) & ((1 << B) - 1); break;
                    default: continue;
                }
                (*possible_values)[(*count)++] = x;
                (*possible_values)[(*count)++] = y;
            }
            break;
        default:
            break;
    }
}

void solve_circuit(unsigned int target) {
    nodes[node_count - 1].value = target;
    for (int i = node_count - 1; i >= 0; i--) {
        if (nodes[i].operation == INPUT) continue;

        unsigned int* possible_values;
        int count;
        reverse_node(&nodes[i], &possible_values, &count);

        if (count > 0) {
            int choice = rand() % (count / 2);
            for (int j = 0; j < nodes[i].input_count; j++) {
                nodes[nodes[i].inputs[j]].value = possible_values[choice * 2 + j];
            }
        }

        free(possible_values);
    }
}

int main() {
    char s[1024];
    srand(time(NULL));

    // Read B
    if (scanf("%d", &B) != 1) {
        fprintf(stderr, "Error reading B\n");
        return 1;
    }

    // Read S
    unsigned int S = 0;
    if (scanf("%s", s) != 1) {
        fprintf(stderr, "Error reading S\n");
        return 1;
    }
    S = binary_to_int(s);

    // Read N
    int N = 0;
    if (scanf("%d", &N) != 1) {
        fprintf(stderr, "Error reading N\n");
        return 1;
    }

    // Read nodes
    for (int i = 0; i < N; i++) {
        Node* node = &nodes[node_count];
        node->node_id = node_count;
        node->input_count = 0;

        if (scanf("%s", s) != 1) {
            fprintf(stderr, "Error reading operation for node %d\n", node_count);
            return 1;
        }

        if (strcmp(s, "NOT") == 0) node->operation = NOT;
        else if (strcmp(s, "LEFT_SHIFT") == 0) node->operation = LEFT_SHIFT;
        else if (strcmp(s, "RIGHT_SHIFT") == 0) node->operation = RIGHT_SHIFT;
        else if (strcmp(s, "AND") == 0) node->operation = AND;
        else if (strcmp(s, "OR") == 0) node->operation = OR;
        else if (strcmp(s, "XOR") == 0) node->operation = XOR;
        else if (strcmp(s, "SUM") == 0) node->operation = SUM;
        else if (strcmp(s, "INPUT") == 0) node->operation = INPUT;
        else if (strcmp(s, "OUTPUT") == 0) node->operation = OUTPUT;

        if (node->operation != INPUT) {
            int dummy;
            if (scanf("%d %d %d", &dummy, &dummy, &node->inputs[0]) != 3) {
                fprintf(stderr, "Error reading input for node %d\n", node_count);
                return 1;
            }
            node->input_count++;
            if (node->operation != NOT && node->operation != LEFT_SHIFT &&
                node->operation != RIGHT_SHIFT && node->operation != OUTPUT) {
                if (scanf("%d", &node->inputs[1]) != 1) {
                    fprintf(stderr, "Error reading second input for node %d\n", node_count);
                    return 1;
                }
                node->input_count++;
            }
        }

        node_count++;
    }

    solve_circuit(S);

    for (int i = 0; i < node_count; i++) {
        if (nodes[i].operation == INPUT) {
            char result[33];
            int_to_binary(nodes[i].value, B, result);
            printf("%s\n", result);
        }
    }

    return 0;
}
Eric PASCUAL <eric.g.pascual@gmail.com>
Dorian Mazauric <dorian.mazauric@inria.fr>
Mael Riviere <mael.riviere@inria.fr>
frederic havet <frederic.havet@i3s.unice.fr>
"Joanna Moulierac" <Joanna.MOULIERAC@univ-cotedazur.fr>
Nisse Nicolas <nicolas.nisse@inria.fr>
Luc Hogie <luc.hogie@cnrs.fr>
Caroline Chollet <caroline.chollet@inria.fr>
JAUME Denis <denis.jaume@wanadoo.fr>
