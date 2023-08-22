.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 32
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 33
# =======================================================
dot:

    # Prologue

    bge zero a2 exit32
    bge zero a3 exit33
    bge zero a4 exit33

    slli a3 a3 2
    slli a4 a4 2

    # s0: result
    # s1: tmp
    # s2: tmp
    addi sp sp -12
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)

    li s0 0

loop_start:

    bge zero a2 loop_end
    lw s1 0(a0)
    lw s2 0(a1)
    mul s1 s1 s2
    add s0 s0 s1

    add a0 a0 a3
    add a1 a1 a4
    addi a2 a2 -1
    j loop_start

loop_end:


    # Epilogue
    mv a0 s0
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    addi sp sp 12

    
    ret

exit32:
    li a0 32
    j exit

exit33:
    li a0 33
    j exit