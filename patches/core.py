from assembler import ASM
from roomEditor import RoomEditor


def removeGhost(rom):
    ## Ghost patch
    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E1B, ASM("LD [$DB79], A"), "", fill_nop=True)

def alwaysAllowSecretBook(rom):
    rom.patch(0x15, 0x3F23, ASM("ld a, [$DB0E]\ncp $0E"), ASM("xor a\ncp $00"), fill_nop=True)

def cleanup(rom):
    # Remove unused rooms to make some space in the rom
    re = RoomEditor(rom, 0x2C4)
    re.objects = []
    re.entities = []
    re.store(rom, 0x2C4)
    re.store(rom, 0x2D4)
    re.store(rom, 0x277)
    re.store(rom, 0x278)
    re.store(rom, 0x279)

    rom.texts[0x02B] = b'' # unused text

def quickswap(rom, button):
    rom.patch(0x00, 0x1094, ASM("jr c, $49"), ASM("jr nz, $49"))  # prevent agressive key repeat
    rom.patch(0x00, 0x10BC,  # Patch the open minimap code to swap the your items instead
        ASM("xor a\nld [$C16B], a\nld [$C16C], a\nld [$DB96], a\nld a, $07\nld [$DB95], a"), ASM("""
        ld a, [$DB%02X]
        ld e, a
        ld a, [$DB%02X]
        ld [$DB%02X], a
        ld a, e
        ld [$DB%02X], a
        ret
    """ % (button, button + 2, button, button + 2)))

# 0x10DB might be a good point to inject a "always running" piece of code.

