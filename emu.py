# https://massung.github.io/CHIP-8/

import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()


red = (255, 0, 0)
green = (0, 255, 0)
surface = pygame.display.set_mode((500, 400))
surface.set_at((20, 20), green)
# pygame.draw.rect(surface, red, (0,0,10,10), 0)
pygame.display.update()

registers = {}
memory = [0] * 4096
stack = []

delay_timer = 0
sound_timer = 0

pc = 0
I = 0


def printh(x, y=None):
    print("\\x{:02x}".format(x), "\\x{:02x}".format(y))


print(input)


def load_rom():
    # input = open('chip8pic.ch8', 'rb').read()
    # input = open('pong.rom', 'rb').read()
    input = open('zd.ch8', 'rb').read()
    #input = open('tetris.rom', 'rb').read()
    # input = open('invaders.rom', 'rb').read()
    # input = open("breakout.rom", "rb").read()
    # input = open('ibmlogo.ch8', 'rb').read()
    # input = open('ibmlogo.ch8', 'rb').read()
    i = 0
    while i < len(input):
        memory[i + 0x200] = input[i]
        i += 1


def set_pixel(x, y):
    pass


load_rom()
pc = 0x200
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    op = memory[pc]
    op1 = memory[pc + 1]

    opa = (op & 0xF0) >> 4
    opb = op & 0x0F

    op1a = (op1 & 0xF0) >> 4
    op1b = op1 & 0x0F

    printh(op, op1)
    # printh(opa, opb)
    # printh(op1a, op1b)

    if op == 0x0:
        if op1 == 0xe0:
            print("cls scr")
        elif op1 == 0xee:
            print("return subroutine")
            addr = stack.pop()
            pc = addr
            continue
    else:

        if opa == 0x1:
            addr = (opb << 8) | op1
            print("JMP to {0}".format(addr))
            pc = addr
            continue
        elif opa == 0x2:
            addr = (opb << 8) | op1
            print("Call subroutine at {0}".format(addr))
            stack.append(pc + 2)
            pc = addr
            continue
        elif opa == 0x3:
            print("Skip next instr if register opb == op1")
            print(registers)
            if registers.get(opb, 0) == op1:
                pc += 2
        elif opa == 0x4:
            print("Skip next instr if register opb != op1")
            if registers[opb] != op1:
                pc += 2
        elif opa == 0x6:
            print("Set REG {0} to {1}".format(opb, op1))
            registers[opb] = op1
        elif opa == 0x7:
            print("Add {0} to REG {1}".format(op1, opb))
            registers[opb] = (registers[opb] + op1) & 0xFF
        elif opa == 0x8:
            print("Various arithmetic commands... {0}, {1}, {2}".format(opb, op1a, op1b))
            

        elif opa == 0xA:
            addr = (opb << 8) | op1
            print("Set I to {0}".format(addr))
            I = addr
        elif opa == 0xC:
            import random

            print("Set opb to random ")
            r = random.randint(0, 255)
            registers[opb] = r & op1

        elif opa == 0xD:

            x = registers[opb]
            y = registers[op1a]
            height = op1b
            width = 8
            print("Draw sprite at {0}, {1} with height {2}".format(x, y, height))
            for i in range(height):
                printh(memory[I + i], 0)
                for idx, v in enumerate(map(int, "{0:08b}".format(memory[I + i]))):
                    if v:
                        print(x + idx, y + i)
                        surface.set_at((x + idx, y + i), green)
                        pygame.display.update()
        elif opa == 0xE:
            print(opa, op1)
            if op1 == 0x9e:
                print("9e")
            elif op1 == 0xa1:
                print("a1: Skips the next instruction if the key stored in VX is not pressed")
                print(registers[opb])

            else:
                a+=1
            #a+=1
        elif opa == 0xF:
            if op1 == 0x33:
                val = registers[opb]
                print("BCD, val = ".format(val))
                h = int(val / 100)
                t = int((val - 100 * h) / 10)
                o = val - 100 * h - 10 * t
                memory[I] = h
                memory[I + 1] = t
                memory[I + 2] = o
            elif op1 == 0x65:
                for i in range(opb + 1):
                    registers[i] = memory[I]
                    I += 1

        else:
            print(opa)
            break

    pc += 2
