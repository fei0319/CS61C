#include "matrix.h"
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>

// Include SSE intrinsics
#if defined(_MSC_VER)
#include <intrin.h>
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
#include <immintrin.h>
#include <x86intrin.h>
#endif

/* Below are some intel intrinsics that might be useful
 * void _mm256_storeu_pd (double * mem_addr, __m256d a)
 * __m256d _mm256_set1_pd (double a)
 * __m256d _mm256_set_pd (double e3, double e2, double e1, double e0)
 * __m256d _mm256_loadu_pd (double const * mem_addr)
 * __m256d _mm256_add_pd (__m256d a, __m256d b)
 * __m256d _mm256_sub_pd (__m256d a, __m256d b)
 * __m256d _mm256_fmadd_pd (__m256d a, __m256d b, __m256d c)
 * __m256d _mm256_mul_pd (__m256d a, __m256d b)
 * __m256d _mm256_cmp_pd (__m256d a, __m256d b, const int imm8)
 * __m256d _mm256_and_pd (__m256d a, __m256d b)
 * __m256d _mm256_max_pd (__m256d a, __m256d b)
*/

/* Generates a random double between low and high */
double rand_double(double low, double high) {
    double range = (high - low);
    double div = RAND_MAX / range;
    return low + (rand() / div);
}

/* Generates a random matrix */
void rand_matrix(matrix *result, unsigned int seed, double low, double high) {
    srand(seed);
    for (int i = 0; i < result->rows; i++) {
        for (int j = 0; j < result->cols; j++) {
            set(result, i, j, rand_double(low, high));
        }
    }
}

/*
 * Allocates space for a matrix struct pointed to by the double pointer mat with
 * `rows` rows and `cols` columns. You should also allocate memory for the data array
 * and initialize all entries to be zeros. `parent` should be set to NULL to indicate that
 * this matrix is not a slice. You should also set `ref_cnt` to 1.
 * You should return -1 if either `rows` or `cols` or both have invalid values. Return -2 if any
 * call to allocate memory in this function fails. Remember to set the error messages in numc.c.
 * Return 0 upon success.
 */
int allocate_matrix(matrix **mat, int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        return -1;
    }

    *mat = malloc(sizeof(matrix));
    if (*mat == NULL) {
        return -2;
    }
    (*mat)->rows = rows;
    (*mat)->cols = cols;
    (*mat)->data = malloc(rows * cols * sizeof(double));
    (*mat)->ref_cnt = 1;
    (*mat)->parent = NULL;

    if ((*mat)->data == NULL) {
        return -2;
    }
    memset((*mat)->data, 0, rows * cols * sizeof(double));

    return 0;
}

/*
 * Allocates space for a matrix struct pointed to by `mat` with `rows` rows and `cols` columns.
 * Its data should point to the `offset`th entry of `from`'s data (you do not need to allocate memory)
 * for the data field. `parent` should be set to `from` to indicate this matrix is a slice of `from`.
 * You should return -1 if either `rows` or `cols` or both have invalid values. Return -2 if any
 * call to allocate memory in this function fails.
 * Remember to set the error messages in numc.c.
 * Return 0 upon success.
 */
int allocate_matrix_ref(matrix **mat, matrix *from, int offset, int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        return -1;
    }

    *mat = malloc(sizeof(matrix));
    if (*mat == NULL) {
        return -2;
    }
    (*mat)->rows = rows;
    (*mat)->cols = cols;
    (*mat)->data = from->data + offset;
    (*mat)->ref_cnt = 1;
    (*mat)->parent = from;

    while (from != NULL) {
        from->ref_cnt += 1;
        from = from->parent;
    }

    return 0;
}

/*
 * You need to make sure that you only free `mat->data` if `mat` is not a slice and has no existing slices,
 * or that you free `mat->parent->data` if `mat` is the last existing slice of its parent matrix and its parent matrix has no other references
 * (including itself). You cannot assume that mat is not NULL.
 */
void deallocate_matrix(matrix *mat) {
    if (mat == NULL) {
        return;
    }
    mat->ref_cnt -= 1;
    if (mat->parent == NULL && mat->ref_cnt == 0) {
        free(mat->data);
    }
    if (mat->parent != NULL) {
        deallocate_matrix(mat->parent);
    }
}

/*
 * This function will call `deallocate_matrix` on the specified matrix and reallocate memory to its `data`
 * as well as reset its other members.
 */
void reallocate_matrix(matrix *mat, int rows, int cols) {
    deallocate_matrix(mat);
    mat->rows = rows;
    mat->cols = cols;
    mat->data = NULL;
    mat->ref_cnt = 1;
    mat->parent = NULL;
}

/*
 * Deallocates the specified matrix and sets its data.
 */
void reallocate_matrix_with(matrix *mat, int rows, int cols, double *data) {
    reallocate_matrix(mat, rows, cols);
    mat->data = data;
}

/*
 * Returns the double value of the matrix at the given row and column.
 * You may assume `row` and `col` are valid.
 */
double get(matrix *mat, int row, int col) {
    return mat->data[mat->cols * row + col];
}

/*
 * Sets the value at the given row and column to val. You may assume `row` and
 * `col` are valid
 */
void set(matrix *mat, int row, int col, double val) {
    mat->data[mat->cols * row + col] = val;
}

/*
 * Sets all entries in mat to val
 */
void fill_matrix(matrix *mat, double val) {
    for (int i = mat->rows * mat->cols - 1; i >= 0; --i) {
        mat->data[i] = val;
    }
}

/*
 * Store the result of adding mat1 and mat2 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int add_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    int rows = mat1->rows, cols = mat2->cols;
    if (mat2->rows != rows || mat2->cols != cols) {
        return -100;
    }
    double *data = malloc(rows * cols * sizeof(data));

    for (int i = rows * cols - 1; i >= 0; --i) {
        data[i] = mat1->data[i] + mat2->data[i];
    }
    reallocate_matrix_with(result, rows, cols, data);
    return 0;
}

/*
 * (OPTIONAL)
 * Store the result of subtracting mat2 from mat1 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int sub_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    /* TODO: YOUR CODE HERE */
    return 0;
}

/*
 * Store the result of multiplying mat1 and mat2 to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 * Remember that matrix multiplication is not the same as multiplying individual elements.
 */
int mul_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    if (mat1->cols != mat2->rows) {
        return -101;
    }
    int rows = mat1->rows, mids = mat1->cols, cols = mat2->cols;
    double *data = malloc(rows * cols * sizeof(double));

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            double t = 0;
            for (int k = 0; k < mids; ++k)
                t += get(mat1, i, k) * get(mat2, k, j);
            data[i * rows + j] = t;
        }
    }
    reallocate_matrix_with(result, rows, cols, data);
    return 0;
}

/*
 * Store the result of raising mat to the (pow)th power to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 * Remember that pow is defined with matrix multiplication, not element-wise multiplication.
 */
int pow_matrix(matrix *result, matrix *mat, int pow) {
    if (pow == 1) {
        int rows = mat->rows, cols = mat->cols;
        double *data = malloc(rows * cols * sizeof(double));
        memcpy(data, mat->data, rows * cols * sizeof(double));
        reallocate_matrix_with(result, rows, cols, data);
        return 0;
    }
    if (mat->rows != mat->cols) {
        return -102;
    }
    int n = mat->rows;

    matrix *p, *temp_result;
    allocate_matrix_ref(&p, mat, 0, n, n);
    allocate_matrix(&temp_result, n, n);
    for (int i = 0; i < n; ++i) {
        set(temp_result, i, i, 1);
    }

    while (pow) {
        if (pow & 1) {
            mul_matrix(temp_result, temp_result, p);
        }
        pow >>= 1, mul_matrix(p, p, p);
    }

    reallocate_matrix_with(result, n, n, temp_result->data);
    deallocate_matrix(p);
    free(temp_result);
    free(p);
    return 0;
}

/*
 * (OPTIONAL)
 * Store the result of element-wise negating mat's entries to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int neg_matrix(matrix *result, matrix *mat) {
    /* TODO: YOUR CODE HERE */
    return 0;
}

/*
 * Store the result of taking the absolute value element-wise to `result`.
 * Return 0 upon success and a nonzero value upon failure.
 */
int abs_matrix(matrix *result, matrix *mat) {
    int rows = mat->rows, cols = mat->cols;
    double *data = malloc(rows * cols * sizeof(double));

    for (int i = rows * cols - 1; i >= 0; --i) {
        data[i] = mat->data[i] >= 0 ? mat->data[i] : -mat->data[i];
    }

    reallocate_matrix_with(result, rows, cols, data);
    return 0;
}
