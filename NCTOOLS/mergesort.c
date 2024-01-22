#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void merge(int array[], int left, int middle, int right) {
// do the parallelization here
  int l_len = middle - left + 1;
  int r_len = right - middle;

  int l_array[l_len];                           // create temp l/r arrays
  int r_array[r_len];

  for(int i = 0; i < l_len; i++) {              // populate left array
    l_array[i] = array[left + i];
  }
  for(int i = 0; i < r_len; i++) {              // populate right array
    r_array[i] = array[middle + 1 + i];
  }

  // initialize
  int i = 0;              // left half index
  int j = 0;              // right half index
 


  for (int idx = left; i < l_len || j < r_len; idx++) {
    if (i < l_len && (j >= r_len || l_array[i] <= r_array[j])) {
      array[idx] = l_array[i];
      i++;
    } else {
      array[idx] = r_array[j];
      j++;
    }
  }
}


void mergeSort(int array[], int left, int right) {
  // while there is more than 2 items in the half keep iterating
  if (left < right) {
    int middle = (left + right) / 2;

    mergeSort(array, left, middle);
    mergeSort(array, middle + 1, right);

    merge(array, left, middle, right);
  }
}


void display(int arr[], int size) {
  for (int i = 0; i < size; i++) {
    printf("sorted[%d] = %d\n", i, arr[i]);
  }
  printf("\n");
}

int main() {
  
  srand(time(NULL));

  int size = 10;
  int arr[size];

  for(int i = 0; i < size; i++) {
    arr[i] = rand() % (size * size);  
  }

  printf("\n\n **********Original array**********\n\n");
 
  display(arr, size);
  
  mergeSort(arr, 0, size - 1);

  printf("\n\n **********Sorted array**********\n\n");
  display(arr, size);
}

