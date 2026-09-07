# 32BIT MIPS PROCESSOR
This repository contains all the files used in designing a **32bit single cycle MIPS processor** in logisim evolution v4.1.0.
---
This project was created as part of my digital design and computer architecture learning.

## A quick explanation of files used in this project:
In the main folder, all parts used in building the data path and control unit of the processor exists which are used as libraries in the final project. 
In the `singals_tables` folder two Excel files of all control signals exists for easy designing. 
In the `assembler` folder there is a simple assembler written in python for this processor and some examples of its input and output (the program for the snake game). I
n the `imagecoder` folder, there is a program written in python that using the pillow library of python, turns an image into a readable hex file for the logism built-in RAM. 
Finally in the `modified cpu` folder, the final versions of the processor exists. Currently there is three of them, the full Single cycle processor itself, one where it is modified to take the the data of an image turned into hex with the help of the `image.py` and loaded into it's data memory and draw it onto the RGB video component and a modified version that is connected to the logism built-in keyboard and RGB video and you can play a classic game of snake on it.


## Instructions
Below is a table of all supported MIPS instructions by this processor. All instructions are completely similar (OPcode and Funct) to standard MIPS insturctions.

| INSTRUCTION | FUNCTION |
|-------|--------------|
| add    | [rd] = [rs] + [rt]  |  
| sub   | xxxxxx       |
| addi   | 0000         | 
| and  | 0010         |
| or   | 0100         | 
| andi    | 0101         |
| ori  | 1010         |
| lui   | xxxxxx       |  
| slt   | xxxxxx       |
| slti   | 0000         | 
| lw  | 0010         |
| sw    | 0100         | 
| beq    | 0101         |
| bne   | 1010         |
| j   | xxxxxx       |  
| jr    | xxxxxx       |
| jal    | 0000         | 
| sll   | 0010         |
| srl   | 0100         | 
| sra   | 0101         |
| nor   | 1010         |
| xor   | 0101         |
| xori   | 1010         |

