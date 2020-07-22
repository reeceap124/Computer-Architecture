"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.branchTable = {
            HLT : self.hlt,
            LDI : self.ldi,
            PRN : self.prn,
            MUL : self.mul
        }

    def ram_read(self, MAR):
        return self.ram[MAR]
        
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def hlt(self, a = None , b = None):
        self.running = False

    def ldi(self, a, b):
        self.reg[a] = b
        self.pc += 2

    def prn(self, a, b = None):
        print(self.reg[a])
        self.pc += 1

    def mul(self, a, b):
        self.reg[a] = self.reg[a] * self.reg[b]
        self.pc += 2

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = program
        with open(program) as f:
            for line in f:
                command = line.split('#')
                command = command[0].strip()
                if command == '':
                    continue #if line is empty string skip to next iteration of loop
                command = int(command, 2)
                self.ram[address] = command
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
            if IR in self.branchTable:
                self.branchTable[IR](operand_a, operand_b)
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
