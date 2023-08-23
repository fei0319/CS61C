.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 64
# - If you receive an fwrite error or eof,
#   this function terminates the program with error code 67
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 65
# ==============================================================================
write_matrix:
    addi sp sp -24
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    sw s3 16(sp)
    sw s4 20(sp)

    mv s0 a0
    mv s1 a1
    mv s2 a2
    mv s3 a3

    # Get the file descriptor
    mv a1 s0
    li a2 1
    jal ra fopen
    mv s0 a0

    # s0: file descriptor
    # s1: matrix pointer
    # s2: #rows
    # s3: #cols
    # s4:

    # Allocate memory of 8 bytes and save its pointer to s4
    li a0 8
    jal ra malloc
    mv s4 a0

    # Put #rows and #cols to s4
    sw s2 0(s4)
    sw s3 4(s4)

    # Write rows and cols
    mv a1 s0
    mv a2 s4
    li a3 2
    li a4 4
    jal ra fwrite

    # Free s4
    mv a0 s4
    jal ra free

    # Write matrix data
    mv a1 s0
    mv a2 s1
    mul a3 s2 s3
    li a4 4
    jal ra fwrite

    # Close the file
    mv a1 s0
    jal ra fclose
    
    lw ra 0(sp)
    lw s0 4(sp)
    lw s1 8(sp)
    lw s2 12(sp)
    lw s3 16(sp)
    lw s4 20(sp)
    addi sp sp 24

    ret
