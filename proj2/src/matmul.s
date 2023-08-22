.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 34
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 34
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 34
# =======================================================
matmul:
    bge zero a1 exit34
    bge zero a2 exit34
    bge zero a4 exit34
    bge zero a5 exit34
    bne a2 a4 exit34

    # s0: d
    # s1: n
    # s2: m
    # s3: k
    # s4: m0
    # s5: m1
    # (n, k) * (k, m) -> (n, m)

    addi sp sp -36
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    sw ra 24(sp)
    sw s6 28(sp)
    sw s7 32(sp)

    mv s0 a6
    mv s1 a1
    mv s2 a5
    mv s3 a2
    mv s4 a0
    mv s5 a3

    li s6 0

outer_loop_start:
    bge s6 s1 outer_loop_end
    li s7 0

inner_loop_start:
    bge s7 s2 inner_loop_end
    # Calculating m(s6, s7) -> s0

    # Get the s6-th row of m0(s4) and put it into a0
    mul t2 s6 s3
    slli t2 t2 2
    add a0 t2 s4

    # Get the s7-th col of m1(s5) and put it into a1
    slli t2 s7 2
    add a1 t2 s5

    # Put k(s3) into a2
    mv a2 s3

    # Stride for v0, a3, should be 1
    li a3 1

    # Stride for v1, a4, should be m(s2)
    mv a4 s2

    jal ra dot
    sw a0 0(s0)

    addi s7 s7 1
    addi s0 s0 4
    j inner_loop_start

inner_loop_end:
    addi s6 s6 1
    j outer_loop_start


outer_loop_end:
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw ra 24(sp)
    lw s6 28(sp)
    lw s7 32(sp)
    addi sp sp 36

    ret

exit34:
    li a1 34
    j exit2
