#include <stdio.h>

#define SIZE 128

volatile int A[SIZE][SIZE];

void baseline(void){
    int i, j;
    for (j = 0; j < SIZE; j++) {
        for (i = 0; i < SIZE; i++) {
            A[i][j] = i + j;
        }
    }
}

int main(void)
{
    baseline();
    return 0;
}
