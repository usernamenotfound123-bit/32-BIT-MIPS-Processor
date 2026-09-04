import sys
import re

REGISTERS = {
    "$zero": 0, "$at": 1, "$v0": 2, "$v1": 3,
    "$a0": 4, "$a1": 5, "$a2": 6, "$a3": 7,
    "$t0": 8, "$t1": 9, "$t2": 10, "$t3": 11,
    "$t4": 12, "$t5": 13, "$t6": 14, "$t7": 15,
    "$s0": 16, "$s1": 17, "$s2": 18, "$s3": 19,
    "$s4": 20, "$s5": 21, "$s6": 22, "$s7": 23,
    "$t8": 24, "$t9": 25, "$k0": 26, "$k1": 27,
    "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31,
}

def parse_register(token):
    """Turn '$t0' or '$8' into the register number 8."""
    token = token.strip()
    if token in REGISTERS:
        return REGISTERS[token]
    if token.startswith("$") and token[1:].isdigit():
        num = int(token[1:])
        if 0 <= num <= 31:
            return num
    raise ValueError(f"Unknown register: {token}")

R_TYPE_FUNCT = {
    "add": 0b100000,
    "sub": 0b100010,
    "and": 0b100100,
    "or": 0b100101,
    "slt": 0b101010,
    "nor": 0b100111,
    "xor": 0b100110,
}

SHIFT_FUNCT = {
    "sll": 0b000000,
    "srl": 0b000010,
    "sra": 0b000011,
}

I_TYPE_OPCODE = {
    "addi": 0b001000,
    "andi": 0b001100,
    "ori": 0b001101,
    "slti": 0b001010,
    "xori": 0b001110,
}

LOAD_STORE_OPCODE = {
    "lw": 0b100011,
    "sw": 0b101011,
}

LOAD_UPPER_IMMIDIATE_OPCODE = {
    "lui": 0b001111,
}

BRANCH_OPCODE = {
    "beq": 0b000100,
    "bne": 0b000101,
}

JUMP_OPCODE = {
    "j": 0b000010,
    "jal": 0b000011,
}

def strip_comment(line):
    return line.split("#", 1)[0]

def parse_line(line):
    line = strip_comment(line).strip()
    if not line:
        return None
    parts = line.split(None, 1)
    mnemonic = parts[0].lower()
    operands = []
    if len(parts) > 1:
        operands = [op.strip() for op in parts[1].split(",")]

    return mnemonic, operands

def parse_immediate(token):
    return int(token.strip(), 0)

def encode_instruction(mnemonic, operands, address, symbol_table):
    if mnemonic in R_TYPE_FUNCT:
        if len(operands) != 3:
            raise ValueError(f"'{mnemonic}' expects 3 operands, got {operands}")
        rd = parse_register(operands[0])
        rs = parse_register(operands[1])
        rt = parse_register(operands[2])
        funct = R_TYPE_FUNCT[mnemonic]
        shamt = 0
        opcode = 0

        word = (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct
        return word
    
    if mnemonic in SHIFT_FUNCT:
        if len(operands) != 3:
            raise ValueError(f"'{mnemonic}' expects 3 operands, got {operands}")
        rd = parse_register(operands[0])
        rs = 0
        rt = parse_register(operands[1])
        funct = SHIFT_FUNCT[mnemonic]
        shamt = parse_immediate(operands[2])
        opcode = 0

        word = (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct
        return word
    
    elif mnemonic in I_TYPE_OPCODE:
        if len(operands) != 3:
            raise ValueError(f"'{mnemonic}' expects 3 operands, got {operands}")
        rt = parse_register(operands[0])
        rs = parse_register(operands[1])
        imm = parse_immediate(operands[2]) & 0xFFFF
        opcode = I_TYPE_OPCODE[mnemonic]

        word = (opcode << 26) | (rs << 21) | (rt << 16) | imm
        return word

    elif mnemonic in LOAD_STORE_OPCODE:
        if len(operands) != 2:
            raise ValueError(f"'{mnemonic}' expects 2 operands, got {operands}")
        rt = parse_register(operands[0])
        match = re.match(r"(-?\d+)\((\$\w+)\)", operands[1])
        if not match:
            raise ValueError(f"Bad offset(base) syntax for '{mnemonic}': '{operands[1]}'")
        imm = parse_immediate(match.group(1)) & 0xFFFF
        rs = parse_register(match.group(2))
        opcode = LOAD_STORE_OPCODE[mnemonic]

        word = (opcode << 26) | (rs << 21) | (rt << 16) | imm
        return word

    elif mnemonic in LOAD_UPPER_IMMIDIATE_OPCODE:
        if len(operands) != 2:
            raise ValueError(f"'{mnemonic}' expects 2 operands, got {operands}")
        rt = parse_register(operands[0])
        imm = parse_immediate(operands[1])
        rs = 0
        opcode = LOAD_UPPER_IMMIDIATE_OPCODE[mnemonic]

        word = (opcode << 26) | (rs << 21) | (rt << 16) | imm
        return word
    
    elif mnemonic in BRANCH_OPCODE:
        if len(operands) != 3:
            raise ValueError(f"'{mnemonic}' expects 3 operands, got {operands}")
        rs = parse_register(operands[0])
        rt = parse_register(operands[1])
        label = operands[2]
        if label not in symbol_table:
            raise ValueError(f"Undefined label: '{label}'")
        offset = (symbol_table[label] - (address + 4)) // 4
        imm = offset & 0xFFFF
        opcode = BRANCH_OPCODE[mnemonic]

        word = (opcode << 26) | (rs << 21) | (rt << 16) | imm
        return word
    
    if mnemonic in JUMP_OPCODE:
        if len(operands) != 1:
            raise ValueError(f"'{mnemonic}' expects 1 operand, got {operands}")
        label = operands[0]
        if label not in symbol_table:
            raise ValueError(f"Undefined label: '{label}'")
        target = (symbol_table[label] >> 2) & 0x03FFFFFF
        opcode = JUMP_OPCODE[mnemonic]

        word = (opcode << 26) | target
        return word
    
    elif mnemonic == "jr":
        if len(operands) != 1:
            raise ValueError(f"'jr' expects 1 operand, got {operands}")
        rs = parse_register(operands[0])
        rt = rd = shamt = 0
        funct = 0b001000
        opcode = 0

        word = (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct
        return word
    
    raise ValueError(f"Unsupported instruction: '{mnemonic}' "f"(only {list(R_TYPE_FUNCT.keys())} and {list(I_TYPE_OPCODE.keys())} implemented so far)")

def assemble(lines):
    symbol_table = {}
    address = 0
    for raw_line in lines:
        line = strip_comment(raw_line).strip()
        if not line:
            continue
        if line.endswith(":"):
            label = line[:-1].strip()
            symbol_table[label] = address
            print(f"[pass 1] label '{label}' -> address {address}")
            continue
        address += 4

    words = []
    address = 0
    for raw_line in lines:
        parsed = parse_line(raw_line)
        if parsed is None:
            continue
        mnemonic, operands = parsed
        if mnemonic.endswith(":"):
            continue

        word = encode_instruction(mnemonic, operands, address, symbol_table)
        print(f"[pass 2] {address:04x}: {raw_line.strip():<28} -> {word:08x}")
        words.append(word)
        address += 4

    return words

def write_logisim_image(words, out_path):
    with open(out_path, "w") as f:
        f.write("v2.0 raw\n")
        f.write(" ".join(f"{w:08x}" for w in words))
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mips_assembler.py <input.asm> <output.hex>")
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    with open(in_path) as f:
        lines = f.readlines()

    words = assemble(lines)
    write_logisim_image(words, out_path)
    print(f"\nWrote {len(words)} instruction(s) to {out_path}")
