addi s0 x0 256

lui t0 123212
addi t0 t0 1399
mul t0 t0 t0
addi t0 t0 902

sw t0 0(s0)
mul t0 t0 t0
sw t0 4(s0)

lw t0 0(s0)
lw t0 0(s0)

lb t0 0(s0)
lb t0 1(s0)
lb t0 2(s0)
lb t0 3(s0)
lb t0 4(s0)
lb t0 5(s0)

lh t0 0(s0)
lh t0 1(s0)
lh t0 2(s0)

lw t0 0(s0)
addi t0 t0 1145
mul t0 t0 t0
addi t0 t0 1321
mul t1 t0 t0
xor t0 t0 t1
add t0 t0 t1

sb t0 0(s0)
sh t0 1(s0)
sb t0 3(s0)

lw t0 0(s0)
lw t0 0(s0)

lb t0 0(s0)
lb t0 1(s0)
lb t0 2(s0)
lb t0 3(s0)
lb t0 4(s0)
lb t0 5(s0)

lh t0 0(s0)
lh t0 1(s0)
lh t0 2(s0)