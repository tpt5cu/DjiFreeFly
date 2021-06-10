import pygame



def init():
    pygame.init()
    window = pygame.display.set_mode((400, 400))


def getKey(keyName):
    pygame.event.pump()
    keyInput = pygame.key.get_pressed()
    myKey = pygame.key.key_code(keyName)
    pygame.display.update()
    return keyInput[myKey]

def main():
    if getKey("LEFT"):
        print("Left key pressed")
    elif getKey("RIGHT"):
        print("Right key pressed")

if __name__ == '__main__':
    init()
    while True:
        main()
