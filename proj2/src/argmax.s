.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 32
# =================================================================
argmax:

    # Prologue

    blt zero a1 init
    li a0 32
    li a1 0
    j exit

init:
    
    # s0: index of the greatest value
    # s1: greatest value
    # s2: current index
    # s3: current value
    addi sp sp -16
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)

    li s0 0
    lw s1 0(a0)
    li s2 1
    addi a0 a0 4
    addi a1 a1 -1

loop_start:
    
    bge zero a1 loop_end
    lw s3 0(a0)
    bge s1 s3 loop_continue
    mv s0 s2
    mv s1 s3


loop_continue:

    addi a0 a0 4
    addi a1 a1 -1
    addi s2 s2 1
    j loop_start


loop_end:
    

    # Epilogue
    mv a0 s0
    
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    addi sp sp 16


    ret
