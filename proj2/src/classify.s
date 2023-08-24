.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # Exceptions:
    # - If there are an incorrect number of command line args,
    #   this function terminates the program with exit code 35
    # - If malloc fails, this function terminates the program with exit code 48
    #
    # Usage:
    #   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>

    li t0 5
    bne a0 t0 exit35

    # Prologue
    addi sp sp -40
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    sw s3 16(sp)
    sw s4 20(sp)
    sw s5 24(sp)
    sw s6 28(sp)
    sw s7 32(sp)
    sw s8 36(sp)

    lw s0 4(a1)
    lw s1 8(a1)
    lw s4 12(a1)
    lw s8 16(a1)

    # s0: M0_PATH
    # s1: M1_PATH
    # s2: Shape of m0
    # s3: Shape of m1
    # s4: input matrix path
    # s5: Shape of input matrix
    # s6
    # s7
    # s8: output matrix path

	# =====================================
    # LOAD MATRICES
    # =====================================

    # Load pretrained m0
    li a0 8
    jal ra malloc
    mv s2 a0

    mv a0 s0
    mv a1 s2
    addi a2 s2 4
    jal ra read_matrix
    mv s0 a0

    # Load pretrained m1
    li a0 8
    jal ra malloc
    mv s3 a0
    
    mv a0 s1
    mv a1 s3
    addi a2 s3 4
    jal ra read_matrix
    mv s1 a0

    # Load input matrix
    li a0 8
    jal ra malloc
    mv s5 a0
    
    mv a0 s4
    mv a1 s5
    addi a2 s5 4
    jal ra read_matrix
    mv s4 a0

    # s0: m0
    # s1: m1
    # s2: Shape of m0
    # s3: Shape of m1
    # s4: input matrix
    # s5: Shape of input matrix

    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)
    
    # s6: Current layer (1, 2)
    # s7: Final layer (3)
    li a0 65536
    jal ra malloc
    mv s6 a0
    li a0 65536
    jal ra malloc
    mv s7 a0

    # Calculate layer 1
    mv a0 s0
    lw a1 0(s2)
    lw a2 4(s2)
    mv a3 s4
    lw a4 0(s5)
    lw a5 4(s5)
    mv a6 s6
    jal ra matmul

    # Calculate layer 2
    mv a0 s6
    lw t0 0(s2)
    lw t1 4(s5)
    mul a1 t0 t1
    jal ra relu

    # Calculate layer 3
    mv a0 s1
    lw a1 0(s3)
    lw a2 4(s3)
    mv a3 s6
    lw a4 0(s2)
    lw a5 4(s5)
    mv a6 s7
    jal ra matmul

    # The shape of the score is *0(s3), *4(s5)

    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Free s0, s1
    mv a0 s0
    jal ra free
    mv a0 s1
    jal ra free

    # Then load #rows and #cols of the output matrix to s0, s1
    lw s0 0(s3)
    lw s1 4(s5)

    # Write output matrix
    mv a0 s8
    mv a1 s7
    mv a2 s0
    mv a3 s1
    jal ra write_matrix

    # Free all memory except s0, s1
    mv a0 s2
    jal ra free
    mv a0 s3
    jal ra free
    mv a0 s4
    jal ra free
    mv a0 s5
    jal ra free
    mv a0 s6
    jal ra free

    # s0: #rows
    # s1: #cols
    # s7: matrix

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax
    mv a0 s7
    mul a1 s0 s1
    jal ra argmax

    # s2: result
    mv s2 a0

    # Print classification
    mv a1 s2
    jal ra print_int

    # Print newline afterwards for clarity
    li a1 '\n'
    jal ra print_char

    # Epilogue
    lw ra 0(sp)
    lw s0 4(sp)
    lw s1 8(sp)
    lw s2 12(sp)
    lw s3 16(sp)
    lw s4 20(sp)
    lw s5 24(sp)
    lw s6 28(sp)
    lw s7 32(sp)
    lw s8 36(sp)
    addi sp sp 40

    ret

exit35:
    li a1 35
    j exit2
