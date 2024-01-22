/*
 *
 * Compile with nvc -acc matrix.c -o matrix_acc -Minfo=all
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 100

void populate(int arr[N][N]) {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      arr[i][j] = rand() % (N*N);
    }
  }
}

void zero(int arr[N][N]) {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      arr[i][j] = 0;
    }
  }
}


void display(int arr[][N]) {
  for (int i = 0; i < N; i++) {
    printf("        ");
    for (int j = 0; j < N; j++) {
      if (arr[i][j] < 10) {
        printf(" ");
      }
      if (arr[i][j] < 100) {
        printf(" ");
      }
      printf("%d ", arr[i][j]);
    }
    printf("\n");
  }
  printf("\n");
}

void multiply(int A[][N], int B[][N], int C[][N]) {

#pragma acc data copyin(A[0:N][0:N], B[0:N][0:N]) copyout(C[0:N][0:N])
#pragma acc parallel loop collapse(2)
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
#pragma acc loop
      for (int k = 0; k < N; k++) {
	C[i][j] = A[i][k] * B[k][j];
      }
    }
  }
#pragma acc exit data delete(A, B)
}

int main() {
 
  srand(time(NULL));

  int A[N][N], B[N][N], C[N][N];
  
  populate(A);
  populate(B);

  printf("\n\n*************MATRIX A***************\n\n");
  display(A);
  printf("\n\n*************MATRIX B***************\n\n");
  display(B);

  multiply(A,B,C);

  printf("\n\n*************MATRIX C***************\n\n");
  display(C);


}
