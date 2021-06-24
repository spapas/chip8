# https://massung.github.io/CHIP-8/
from io import TextIOWrapper
import random
import pygame, sys
from pygame.locals import *

WIDTH = 64 # 0x00 - 0x3F
HEIGHT = 32 # 0x00 - 0x1F
BLOCK_SIZE = 10 

# set up pygame
pygame.init()


black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
surface = pygame.display.set_mode((640, 320))
#surface.set_at((20, 20), green)
#surface.set_at((25, 25), green)
# pygame.draw.rect(surface, red, (0,0,10,10), 0)
pygame.display.update()

registers = {}
memory = [0] * 4096
display = [0] * 64 * 32
keys = {}

stack = []

delay_timer = 0
sound_timer = 0

pc = 0
I = 0

def printh(x, y=None):
    print("\\x{:02x}".format(x), "\\x{:02x}".format(y))

def load_rom():
    # input = open('chip8pic.ch8', 'rb').read()
    input = open('pong.rom', 'rb').read()
    # input = open('c8_test.c8', 'rb').read()
    # input = open('test_opcode.ch8', 'rb').read()
    #input = open('zd.ch8', 'rb').read()
    #input = open('tetris.rom', 'rb').read()
    # input = open('invaders.rom', 'rb').read()
    # input = open("breakout.rom", "rb").read()
    # input = open('ibmlogo.ch8', 'rb').read()
    # input = open('ibmlogo.ch8', 'rb').read()
    # input = open('random_number_test.ch8', 'rb').read()
    i = 0
    while i < len(input):
        memory[i + 0x200] = input[i]
        i += 1


def draw():
    for idx, l in enumerate(display):
        if l:
            pygame.draw.rect(surface, green, ((idx % WIDTH) * BLOCK_SIZE, (idx // WIDTH) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        else:
            pygame.draw.rect(surface, black, ((idx % WIDTH) * BLOCK_SIZE, (idx // WIDTH) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()

def read_key_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                keys[1] = 1
            elif event.key == pygame.K_2:
                keys[2] = 1
            elif event.key == pygame.K_3:
                keys[3] = 1
            elif event.key == pygame.K_4:
                keys[0xc] = 1
            elif event.key == pygame.K_q:
                keys[4] = 1
            elif event.key == pygame.K_w:
                keys[5] = 1
            elif event.key == pygame.K_e:
                keys[6] = 1
            elif event.key == pygame.K_r:
                keys[0xd] = 1
            elif event.key == pygame.K_a:
                keys[7] = 1
            elif event.key == pygame.K_s:
                keys[8] = 1
            elif event.key == pygame.K_d:
                keys[9] = 1
            elif event.key == pygame.K_f:
                keys[0xe] = 1
            elif event.key == pygame.K_z:
                keys[0xa] = 1
            elif event.key == pygame.K_x:
                keys[0] = 1
            elif event.key == pygame.K_c:
                keys[0xb] = 1
            elif event.key == pygame.K_v:
                keys[0xf] = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                keys[1] = 0
            elif event.key == pygame.K_2:
                keys[2] = 0
            elif event.key == pygame.K_3:
                keys[3] = 0
            elif event.key == pygame.K_4:
                keys[0xc] = 0
            elif event.key == pygame.K_q:
                keys[4] = 0
            elif event.key == pygame.K_w:
                keys[5] = 0
            elif event.key == pygame.K_e:
                keys[6] = 0
            elif event.key == pygame.K_r:
                keys[0xd] = 0
            elif event.key == pygame.K_a:
                keys[7] = 0
            elif event.key == pygame.K_s:
                keys[8] = 0
            elif event.key == pygame.K_d:
                keys[9] = 0
            elif event.key == pygame.K_f:
                keys[0xe] = 0
            elif event.key == pygame.K_z:
                keys[0xa] = 0
            elif event.key == pygame.K_x:
                keys[0] = 0
            elif event.key == pygame.K_c:
                keys[0xb] = 0
            elif event.key == pygame.K_v:
                keys[0xf] = 0

load_rom()
pc = 0x200
while True:
    import time
    draw()
    read_key_state()
    

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
            
            if registers.get(opb, 0) == op1:
                pc += 2
        elif opa == 0x4:
            print("Skip next instr if register opb != op1")
            if registers.get(opb) != op1:
                pc += 2
        elif opa == 0x6:
            print("Set REG {0} to {1}".format(opb, op1))
            registers[opb] = op1
        elif opa == 0x7:
            print("Add {0} to REG {1}".format(op1, opb))
            registers[opb] = (registers[opb] + op1) & 0xFF
        elif opa == 0x8:
            print("Various arithmetic commands... {0}, {1}, {2}".format(opb, op1a, op1b))
            if op1b == 0x0:
                registers[opb] = registers[op1a]
            elif op1b == 0x1:
                registers[opb] = registers[opb] | registers[op1a]
            elif op1b == 0x2:
                registers[opb] = registers[opb] & registers[op1a]
            elif op1b == 0x3:
                registers[opb] = registers[opb] ^ registers[op1a]
            elif op1b == 0x4:
                res = registers[opb] + registers[op1a]
                if res > 255:
                    res = res & 0xff
                    registers[0xf] = 1
                else:
                    registers[0xf] = 0
                registers[opb] = res
            elif op1b == 0x5:
                vx = registers[opb]
                vy = registers[op1a]
                if vx > vy:
                    registers[0xf] = 1
                else:
                    registers[0xf] = 0
                registers[opb] = (vx - vy)&0xff
            elif op1b == 0x6:
                vx = registers[opb]
                if vx & 0x1:
                    registers[0xf] = 1
                else:
                    registers[0xf] = 0
                registers[opb] = vx >> 1
            elif op1b == 0xe:
                vx = registers[opb]
                if vx & 0x8:
                    registers[0xf] = 1
                else:
                    registers[0xf] = 0
                registers[opb] = (vx << 1)&0xff

        elif opa == 0xA:
            addr = (opb << 8) | op1
            print("Set I to {0}".format(addr))
            I = addr
        elif opa == 0xC:

            print("Set opb to random ")
            r = random.randint(0, 255)
            registers[opb] = r & op1

        elif opa == 0xD:

            x = registers[opb]
            y = registers[op1a]
            height = op1b
            width = 8
            print("Draw sprite at {0}, {1} with height {2}".format(x, y, height))
            for iy in range(height):
                for ix, v in enumerate(map(int, "{0:08b}".format(memory[I + iy]))):
                    if v:
                        display_idx = 64*(y+iy) + x + ix
                        if display_idx >= 64 * 32:
                            continue 
                        existing = display[display_idx]
                        if existing:
                            display[display_idx] = 0
                        else:
                            display[display_idx] = 1
                            

        elif opa == 0xE:
            print(opa, op1)
            if op1 == 0x9e:
                print("9e")
                if keys.get(opb):
                    pc += 2
            elif op1 == 0xa1:
                print("a1: Skips the next instruction if the key stored in VX is not pressed")
                
                if not keys.get(opb):
                    pc += 2
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
            elif op1 == 0x55:
                for i in range(opb + 1):
                    memory[I] = registers[i]
                    I += 1
            elif op1 == 0x65:
                for i in range(opb + 1):
                    registers[i] = memory[I]
                    I += 1


        else:
            print(opa)
            #break

    pc += 2

