main:
        addi $s0, $zero,3        # length = 3
        addi $s1, $zero,1        # dx = 1
        addi $s2, $zero,0        # dy = 0
        addi $s6, $zero,5        # head x = 5
        addi $s7, $zero,16       # head y = 16

        # initial body: head (5,16), then (4,16), (3,16)
        addi $t0, $zero, 5
        sw   $t0, 0($zero)
        addi $t0, $zero, 16
        sw   $t0, 4($zero)
        addi $t0, $zero, 4
        sw   $t0, 8($zero)
        addi $t0, $zero, 16
        sw   $t0, 12($zero)
        addi $t0, $zero, 3
        sw   $t0, 16($zero)
        addi $t0, $zero, 16
        sw   $t0, 20($zero)

        addi $s5, $zero,12345    # RNG seed
        jal  place_food         

        # draw the initial body
        addi $t4, $zero, 0
        addi $t5, $zero, 0
        ori  $t6, $zero, 65280   
init_draw_loop:
        beq  $t4, $s0, init_draw_done
        lw   $a0, 0($t5)
        lw   $a1, 4($t5)
        add  $a2, $t6, $zero
        jal  plot_pixel
        addi $t4, $t4, 1
        addi $t5, $t5, 8
        j    init_draw_loop
init_draw_done:

game_loop:
        jal  read_input            # drains keyboard, may update s1/s2

        add  $t0, $s6, $s1
        andi $t0, $t0, 31          
        add  $t1, $s7, $s2
        andi $t1, $t1, 31          
        add  $s6, $t0, $zero      
        add  $s7, $t1, $zero     

        # self-collision check
        add  $a0, $s6, $zero
        add  $a1, $s7, $zero
        jal  check_collision
        bne  $v0, $zero, game_over

        # growing?
        addi $t2, $zero, 0
        bne  $s6, $s3, not_food
        bne  $s7, $s4, not_food
        addi $t2, $zero, 1
not_food:
        beq  $t2, $zero, shift_normal
        addi $t3, $zero, 480       # length cap so body can't overrun
        beq  $s0, $t3, shift_normal 
        j    shift_grow

shift_grow:
        add  $t3, $s0, $zero       # t3 = i, counting down from length
sg_loop:
        beq  $t3, $zero, sg_done
        sll  $t4, $t3, 3
        addi $t5, $t4, -8
        lw   $t6, 0($t5)
        lw   $t7, 4($t5)
        sw   $t6, 0($t4)
        sw   $t7, 4($t4)
        addi $t3, $t3, -1
        j    sg_loop
sg_done:
        addi $s0, $s0, 1           # length++
        j    after_shift

shift_normal:
        addi $t3, $s0, -1          # t3 = index of current tail
        sll  $t4, $t3, 3
        lw   $t8, 0($t4)           # remember old tail position
        lw   $t9, 4($t4)           
sn_loop:
        beq  $t3, $zero, sn_done
        sll  $t4, $t3, 3
        addi $t5, $t4, -8
        lw   $t6, 0($t5)
        lw   $t7, 4($t5)
        sw   $t6, 0($t4)
        sw   $t7, 4($t4)
        addi $t3, $t3, -1
        j    sn_loop
sn_done:
        add  $a0, $t8, $zero
        add  $a1, $t9, $zero
        addi $a2, $zero, 0         
        jal  plot_pixel
        j    after_shift

after_shift:
        sw   $s6, 0($zero)         
        sw   $s7, 4($zero)

        add  $a0, $s6, $zero
        add  $a1, $s7, $zero
        ori  $a2, $zero, 65280     
        jal  plot_pixel

        beq  $t2, $zero, skip_new_food
        jal  place_food
skip_new_food:

        jal  delay
        j    game_loop
game_over:
        addi $t5, $zero, 32
        addi $t0, $zero, 0
go_y:
        beq  $t0, $t5, go_done
        addi $t1, $zero, 0
go_x:
        beq  $t1, $t5, go_x_done
        add  $a0, $t1, $zero
        add  $a1, $t0, $zero
        lui  $a2, 255              
        jal  plot_pixel
        addi $t1, $t1, 1
        j    go_x
go_x_done:
        addi $t0, $t0, 1
        j    go_y
go_done:
halt_loop:
        j    halt_loop

plot_pixel:
        sw   $a0, 8192($zero)
        sw   $a1, 8196($zero)
        sw   $a2, 8200($zero)
        jr   $ra

# check_collision
check_collision:
        addi $t0, $zero, 0         # i
        addi $t1, $zero, 0         # body pointer
cc_loop:
        beq  $t0, $s0, cc_no
        lw   $t2, 0($t1)
        lw   $t3, 4($t1)
        bne  $t2, $a0, cc_next
        bne  $t3, $a1, cc_next
        addi $v0, $zero, 1
        jr   $ra
cc_next:
        addi $t0, $t0, 1
        addi $t1, $t1, 8
        j    cc_loop
cc_no:
        addi $v0, $zero, 0
        jr   $ra

# read_input() -- drains the keyboard buffer
read_input:
ri_loop:
        lw   $t0, 4096($zero)
        beq  $t0, $zero, ri_done
        lw   $t1, 4100($zero)

        addi $t2, $zero, 119       # 'w'
        bne  $t1, $t2, ri_check_a
        addi $s1, $zero, 0
        addi $s2, $zero, -1
        j    ri_loop
ri_check_a:
        addi $t2, $zero, 97        # 'a'
        bne  $t1, $t2, ri_check_s
        addi $s1, $zero, -1
        addi $s2, $zero, 0
        j    ri_loop
ri_check_s:
        addi $t2, $zero, 115       # 's'
        bne  $t1, $t2, ri_check_d
        addi $s1, $zero, 0
        addi $s2, $zero, 1
        j    ri_loop
ri_check_d:
        addi $t2, $zero, 100       # 'd'
        bne  $t1, $t2, ri_loop
        addi $s1, $zero, 1
        addi $s2, $zero, 0
        j    ri_loop
ri_done:
        jr   $ra

place_food:
        sw   $ra, 3900($zero)
        addi $t9, $zero, 20        # bounded retry count
pf_retry:
        sll  $t0, $s5, 13          # xorshift32
        xor  $s5, $s5, $t0
        srl  $t0, $s5, 17
        xor  $s5, $s5, $t0
        sll  $t0, $s5, 5
        xor  $s5, $s5, $t0

        andi $t4, $s5, 31          
        srl  $t5, $s5, 5           
        andi $t5, $t5, 31

        add  $a0, $t4, $zero
        add  $a1, $t5, $zero
        jal  check_collision
        beq  $v0, $zero, pf_found

        addi $t9, $t9, -1
        beq  $t9, $zero, pf_found  # give up retrying, accept overlap
        j    pf_retry
pf_found:
        add  $s3, $t4, $zero
        add  $s4, $t5, $zero

        add  $a0, $s3, $zero
        add  $a1, $s4, $zero
        lui  $a2, 255             
        jal  plot_pixel

        lw   $ra, 3900($zero)
        jr   $ra

# delay()
delay:
        addi $t0, $zero, 1
delay_loop:
        beq  $t0, $zero, delay_done
        addi $t0, $t0, -1
        j    delay_loop
delay_done:
        jr   $ra
