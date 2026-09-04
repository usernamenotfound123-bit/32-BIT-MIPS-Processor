# =============================================================
# Test program: array sum + max (via function call) + bitwise
# checksum manipulation. Exercises every implemented
# instruction at least once: add, sub, and, or, slt, nor, xor,
# sll, srl, sra, jr, addi, andi, ori, xori, lui, slti, lw, sw,
# beq, bne, j, jal
# =============================================================

        addi $s0, $zero, 64     # s0 = array base address (0x40)

        # --- initialize array: {4, 9, 2, 7, 5} ---
        addi $t0, $zero, 4
        sw   $t0, 0($s0)
        addi $t0, $zero, 9
        sw   $t0, 4($s0)
        addi $t0, $zero, 2
        sw   $t0, 8($s0)
        addi $t0, $zero, 7
        sw   $t0, 12($s0)
        addi $t0, $zero, 5
        sw   $t0, 16($s0)

        addi $s3, $zero, 5      # s3 = array length
        addi $s1, $zero, 0      # s1 = sum accumulator
        addi $s2, $zero, 0      # s2 = loop index

loop_sum:
        beq  $s2, $s3, end_sum
        sll  $t1, $s2, 2        # t1 = index * 4
        add  $s4, $s0, $t1      # s4 = element address
        lw   $t0, 0($s4)
        add  $s1, $s1, $t0
        addi $s2, $s2, 1
        j    loop_sum
end_sum:

        # --- find max via function call ---
        add  $a0, $s0, $zero    # a0 = array base
        addi $a1, $s3, 0        # a1 = length
        jal  find_max
        # v0 = max on return

        sub  $t4, $s1, $v0      # t4 = sum - max

        # --- bitwise checksum section ---
        lui  $t5, 0x1234
        ori  $t5, $t5, 0xABCD   # t5 = 0x1234ABCD
        xor  $t6, $s1, $t5      # t6 = sum XOR t5
        andi $t7, $v0, 0xFF     # t7 = max AND 0xFF
        and  $s5, $t6, $t7      # s5 = t6 AND t7
        or   $s5, $s5, $t7      # s5 = s5 OR t7
        nor  $s6, $s5, $zero    # s6 = NOT(s5)
        xori $s7, $t5, 0x00FF   # s7 = t5 XOR 0x00FF
        srl  $t8, $s6, 4        # t8 = s6 >> 4 (logical)
        sra  $t9, $s6, 4        # t9 = s6 >> 4 (arithmetic)
        slti $t2, $s1, 100      # t2 = (sum < 100) ? 1 : 0

        # --- store results to memory ---
        addi $t3, $zero, 128    # t3 = results base address (0x80)
        sw   $s1, 0($t3)        # sum
        sw   $v0, 4($t3)        # max
        sw   $s6, 8($t3)        # checksum
        sw   $t4, 12($t3)       # sum - max

done:
        j    done               # halt

# -----------------------------------------------------------
# find_max(a0 = base address, a1 = length) -> v0 = max value
# -----------------------------------------------------------
find_max:
        lw   $v0, 0($a0)        # v0 = array[0]
        addi $t0, $zero, 1      # index = 1
        add  $t1, $a0, $zero    # current address = base
loop_max:
        addi $t1, $t1, 4
        lw   $t2, 0($t1)
        slt  $t3, $v0, $t2
        beq  $t3, $zero, skip_update
        add  $v0, $t2, $zero
skip_update:
        addi $t0, $t0, 1
        bne  $t0, $a1, loop_max
        jr   $ra
