addi x1 x0 12
addi x2 x0 -149
addi x3 x0 2

add s0 x1 x2
add s0 x1 x3
add x3 x2 x2

mul x3 x1 x2
mul x1 x2 x3
mul x2 x1 x3

sub s0 x1 x2
sub x3 x1 x2
sub x1 x2 x3

addi x2 x2 3
sll x1 x1 x2
addi x1 x1 3
sll x2 x2 x1

mulh x2 x1 x2
mulh x1 x2 x2

sub x2 x0 x2
mulhu x2 x2 x2

slt s0 x1 x2
slt s0 x2 x1
slt s0 x1 x1

xor s0 x1 x2

srl s0 x2 x1

sub x2 x0 x2
sra s0 x2 x1
sub x2 x0 x2
sra s0 x2 x1

or s0 x1 x2

and s0 x1 x2