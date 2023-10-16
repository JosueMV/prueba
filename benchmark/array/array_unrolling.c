#include <stdio.h>

#define SIZE 128

volatile int A[SIZE][SIZE];

void baseline(void){
    int i, j;
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j += 4) {
            A[i][j] = i + j;
            A[i][j + 1] = i + j + 1;
            A[i][j + 2] = i + j + 2;
            A[i][j + 3] = i + j + 3;
        }
    }
}

int main(void)
{
    baseline();
    return 0;
}
