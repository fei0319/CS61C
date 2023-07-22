#include "hashtable.h"
#include <stdio.h>
#include <stdlib.h>

unsigned int hashInt(void *data) {
    return *(int *)(data);
}

int equalInt(void *a, void *b) {
    return *(int *)(a) == *(int *)(b);
}

int main() {
    HashTable *table = createHashTable(3, &hashInt, &equalInt);

    while (1) {
        int op;
        scanf("%d", &op);
        if (op == 1) {
            int *k = malloc(sizeof(int)), *v = malloc(sizeof(int));
            scanf("%d%d", k, v);
            insertData(table, k, v);
        } else {
            int *k = malloc(sizeof(int));
            scanf("%d", k);
            int *result = findData(table, k);
            if (result == NULL) {
                puts("NOT FOUND");
            } else {
                printf("%d\n", *result);
            }
        }
    }
}