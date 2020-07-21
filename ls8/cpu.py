"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = False

    def ram_read(self, MAR):
        return self.ram[MAR]
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    def hlt(self):
        self.running = False
    def ldi(self, a, b):
        self.reg[a] = b
        self.pc += 2
    def prn(self, a):
        print(self.reg[a])
        self.pc += 1

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # reg 0
            0b00001000, # Value assigned
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                self.hlt()
            elif IR == LDI:
                self.ldi(operand_a, operand_b)
            elif IR == PRN:
                self.prn(operand_a)
            else:
                print("Automatically Exited")
                self.hlt()
            self.pc += 1
            #Figure out how to implement instructions

        # Need to read memory address at PC
        # Instruction Register (local variable here) stores what's held at the address
        # Use ram_read to get bytes at PC+1 and PC+2 from RAM into vars operand_a and operand_b
        #then perform actions need for the instruction
        #update PC needs to then be updated
