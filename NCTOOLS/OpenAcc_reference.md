# OpenACC Directives Study Guide

## 1. Parallel Loop Directives

- **`#pragma acc parallel loop`**
  - **Purpose:** Parallelizes a loop across multiple threads on an accelerator.
  - **Example:**
    ```c
    #pragma acc parallel loop
    for (int i = 0; i < N; i++) {
        // loop body
    }
    ```

## 2. Parallel Loop Collapse

- **`#pragma acc parallel loop collapse(n)`**
  - **Purpose:** Collapses nested loops into a single parallel loop to enhance parallelization.
  - **Example:**
    ```c
    #pragma acc parallel loop collapse(2)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            // nested loop body
        }
    }
    ```

## 3. Loop Vectorization

- **`#pragma acc loop vector`**
  - **Purpose:** Requests the compiler to vectorize the loop for SIMD (Single Instruction, Multiple Data) execution.
  - **Example:**
    ```c
    #pragma acc parallel loop vector
    for (int i = 0; i < N; i++) {
        // loop body
    }
    ```

## 4. Reduction

- **`#pragma acc parallel loop reduction(operator:variable)`**
  - **Purpose:** Performs a reduction operation (e.g., sum, product) on a variable within a parallel loop.
  - **Example:**
    ```c
    #pragma acc parallel loop reduction(+:sum)
    for (int i = 0; i < N; i++) {
        sum += array[i];
    }
    ```

## 5. Data Management

- **`#pragma acc data copyin(variable)`**
  - **Purpose:** Copies data from the host to the accelerator.
  - **Example:**
    ```c
    #pragma acc data copyin(A)
    {
        #pragma acc parallel loop
        for (int i = 0; i < N; i++) {
            // loop body using A
        }
    }
    ```

- **`#pragma acc data copyout(variable)`**
  - **Purpose:** Copies data from the accelerator to the host.
  - **Example:**
    ```c
    #pragma acc data copyout(B)
    {
        #pragma acc parallel loop
        for (int i = 0; i < N; i++) {
            // loop body modifying B
        }
    }
    ```

- **`#pragma acc data create(variable)`**
  - **Purpose:** Allocates and initializes data on the accelerator.
  - **Example:**
    ```c
    #pragma acc data create(C)
    {
        #pragma acc parallel loop
        for (int i = 0; i < N; i++) {
            // loop body using C
        }
    }
    ```

## 6. Routine Directive

- **`#pragma acc routine(function)`**
  - **Purpose:** Directs the compiler to offload a specific function to the accelerator.
  - **Example:**
    ```c
    #pragma acc routine(myFunction)
    void myFunction(int *array, int size) {
        // function body
    }
    ```

## 7. Async Directive

- **`#pragma acc parallel async(n)`**
  - **Purpose:** Executes parallel loops asynchronously with respect to the host.
  - **Example:**
    ```c
    #pragma acc parallel loop async(1)
    for (int i = 0; i < N; i++) {
        // loop body
    }
    ```

## 8. Gang Worker Vector

- **`#pragma acc kernels`**
  - **Purpose:** Specifies that the enclosed code block is a kernels region, allowing the compiler to parallelize across gangs, workers, and vectors.
  - **Example:**
    ```c
    #pragma acc kernels
    {
        #pragma acc loop
        for (int i = 0; i < N; i++) {
            // loop body
        }
    }
    ```

## 9. Tile Directive

- **`#pragma acc loop tile(tile_size)`**
  - **Purpose:** Divides the iteration space into tiles, improving data locality.
  - **Example:**
    ```c
    #pragma acc parallel loop tile(16, 32)
    for (int i = 0; i < N; i++) {
        // loop body
    }
    ```

## 10. Cache Directive

- **`#pragma acc cache(variables)`**
  - **Purpose:** Directs the compiler to cache specified variables in shared memory.
  - **Example:**
    ```c
    #pragma acc parallel loop cache(A, B)
    for (int i = 0; i < N; i++) {
        // loop body using A and B
    }
    ```

## General Tips:

- Ensure that your compiler supports OpenACC directives and has OpenACC support enabled.
- Experiment with different directives and configurations to find the optimal performance for your specific application and hardware.

This study guide provides a starting point for understanding and using OpenACC directives. For more in-depth information, refer to the official OpenACC documentation and tutorials.

