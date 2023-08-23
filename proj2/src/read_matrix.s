.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 48
# - If you receive an fopen error or eof, 
#   this function terminates the program with error code 64
# - If you receive an fread error or eof,
#   this function terminates the program with error code 66
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 65
# ==============================================================================
read_matrix:
    addi sp sp -28
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    sw s3 16(sp)
    sw s4 20(sp)
    sw s5 24(sp)

    mv s0 a0
    mv s1 a1
    mv s2 a2

    # Set s0 to the file descriptor and handle the error
    mv a1 s0
    li a2 0
    jal ra fopen
    li s0 -1
    beq a0 s0 exit64
    mv s0 a0

    # Allocate memory to store 2 integers, pointer to which is s3
    li a0 8
    jal ra malloc
    beq a0 zero exit48
    mv s3 a0

    # Read the row and column from the file
    mv a1 s0
    mv a2 s3
    li a3 8
    mv s4 a3
    jal ra fread
    bne s4 a0 exit66

    # Save the row and column to s4 and s5, as well as storing them
    lw s4 0(s3)
    lw s5 4(s3)
    sw s4 0(s1)
    sw s5 0(s2)

    # Free s3
    mv a0 s3
    jal ra free

    # Allocate memory to store the whole matrix, pointer to which is s3
    mul a0 s4 s5
    slli a0 a0 2
    jal ra malloc
    mv s3 a0

    # Read the matrix
    mv a1 s0
    mv a2 s3
    mul a3 s4 s5
    slli a3 a3 2
    mv s1 a3
    jal ra fread
    bne a0 s1 exit66

    # Close the file
    mv a1 s0
    jal ra fclose
    li t0 -1
    beq t0 a0 exit65

    mv a0 s3
    
    lw ra 0(sp)
    lw s0 4(sp)
    lw s1 8(sp)
    lw s2 12(sp)
    lw s3 16(sp)
    lw s4 20(sp)
    lw s5 24(sp)
    addi sp sp 28

    ret

exit48:
    li a1 48
    j exit2

exit64:
    li a1 64
    j exit2

exit66:
    li a1 66
    j exit2

exit65:
    li a1 65
    j exit2