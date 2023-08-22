.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 32
# ==============================================================================
relu:
    # Prologue
    addi sp sp -8
    sw ra 0(sp)
    sw s0 4(sp)

    li s0 1
    bge a1 s0 loop_start
    # exit with error code 32
    li a1 32
    j exit2

loop_start:

    bge zero a1 loop_end
    lw s0 0(a0)
    bge s0 zero loop_continue
    sw zero 0(a0)

loop_continue:
    addi a0 a0 4
    addi a1 a1 -1
    j loop_start

loop_end:


    # Epilogue

    lw ra 0(sp)
    lw s0 4(sp)
    addi sp sp 8
    
	ret
