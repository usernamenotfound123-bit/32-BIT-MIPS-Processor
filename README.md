# 32BIT MIPS PROCESSOR
This repository contains all the files used in designing a **32bit single cycle MIPS processor** in logisim evolution v4.1.0.
---
This project was created as part of my digital design and computer architecture learning.

## A quick explanation of files used in this project:
- In the main folder, all parts used in building the data path and control unit of the processor exists which are used as libraries in the final project. 
- In the `singals_tables` folder two Excel files of all control signals exists for easy designing. 
- In the `assembler` folder there is a simple assembler written in python for this processor and some examples of its input and output (the program for the snake game). 
- In the `imagecoder` folder, there is a program written in python that using the pillow library of python, turns an image into a readable hex file for the logism built-in RAM. 
- Finally in the `modified cpu` folder, the final versions of the processor exists. Currently there is three of them, the full Single cycle processor itself, one where it is modified to take the the data of an image turned into hex with the help of the `image.py` and loaded into it's data memory and draw it onto the RGB video component and a modified version that is connected to the logism built-in keyboard and RGB video and you can play a classic game of snake on it.


## Instructions
Below is a table of all supported MIPS instructions by this processor. All instructions are completely similar (OPcode and Funct) to standard MIPS insturctions.

| INSTRUCTION | FUNCTION |
|-------|--------------|
| add    | [rd] = [rs] + [rt]  |  
| sub   | [rd] = [rs] - [rt]       |
| addi   | [rt] = [rs] + signImm         | 
| and  | [rd] = [rs] AND [rt]         |
| or   | [rd] = [rs] OR [rt]         | 
| andi    | [rt] = [rs] AND zeroImm         |
| ori  | [rt] = [rs] OR zeroImm         |
| lui   | [rt] = {Imm, 16'b0}      |  
| slt   | [rs] < [rt] ? [rd]=1 : [rd]=0       |
| slti   | [rs] < [signImm ? [rd]=1 : [rd]=0         | 
| lw  | [rt] = [Address]         |
| sw    | [Address] = [rt]         | 
| beq    | if([rs] == [rt]) PC = BTA         |
| bne   | if([rs] != [rt]) PC = BTA         |
| j   | PC = JTA       |  
| jr    | PC = [rs]       |
| jal    | $ra = PC+4 , PC = JTA         | 
| sll   | [rd] = [rt] << shamt         |
| srl   | [rd] = [rt] >> shamt         | 
| sra   | [rd] = [rt] >>> shamt         |
| nor   | [rd] = ~([rs]|[rt])         |
| xor   | [rd] = [rs] ^ [rt]         |
| xori   | [rt] = [rs] ^ zeroImm         |

