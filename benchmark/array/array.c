#include <stdio.h>

#define SIZE 16

volatile int A[SIZE][SIZE];

void baseline(void)
{
    int i, j;

    for (i = 0; i < SIZE; i++)
        for (j = 0; j < SIZE; j++)
            A[i][j] = i + j;
}

int main(void)
{
    baseline();
    return 0;
}
