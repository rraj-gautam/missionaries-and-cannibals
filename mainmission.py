#Missionaries and Cannibal Problem
#Solved by using BFS algorithm and Pygame library
import pygame
import sys
from pygame.locals import *
from PIL import Image
from collections import Counter

global var1
global var2
global var3
var3= False


print (var3) #debug code
'''''
while var3:
    print (var3) #debug code
    if __name__ == "__main__":
        main()
'''

def main():
    print ("entered main function") #debug code
    pygame.init()
    WHITE = (255, 255, 255)
    window = 1000, 680
    background = pygame.image.load('background.jpg')
    background = pygame.transform.scale(background, window)
    screen = pygame.display.set_mode(window, HWSURFACE | DOUBLEBUF | RESIZABLE)

    boat = pygame.image.load("boat.png").convert_alpha() #for boat
    cannibal = pygame.image.load("cannibal.png").convert_alpha() #for cannibal
    missionary = pygame.image.load("missionary.png").convert_alpha() #for missionary

    background_position = [0, 0]
    boatleft_position = [250, 250]
    boatright_position = [500, 250]

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, background_position)

        solution = BFS()
        path = []
        path.append(solution)
        parent = solution.parent
        while parent:
            path.append(parent)
            parent = parent.parent

        for t in range(len(path)):

            state = path[len(path) - t - 1]

            if state.boat == 'left':
                screen.blit(boat, boatleft_position)

            if state.boat == 'right':
                screen.blit(boat, boatright_position)

            if state.cannibalLeft > 0:
                for i in range(1, state.cannibalLeft + 1):
                    screen.blit(cannibal, [i * 20 + 50, 300])

            if state.cannibalRight > 0:
                for j in range(1, state.cannibalRight + 1):
                    screen.blit(cannibal, [750 + (j * 20), 350])

            if state.missionaryLeft > 0:
                for i in range(1, state.missionaryLeft + 1):
                    screen.blit(missionary, [i * 20 + 30, 150])

            if state.missionaryRight > 0:
                for j in range(1, state.missionaryRight + 1):
                    screen.blit(missionary, [700 + (j * 20), 200])

            pygame.display.update()
            pygame.time.delay(2000)
            screen.fill(WHITE)

            screen.blit(background, background_position)

        print ("exited program")  # debug code

        pygame.quit()

def BFS():
    print ("entered BFS function") #debug code
    initial_state = State(3, 3, 'left', 0, 0)
    if initial_state.is_goal():
        return initial_state
    var1 = list()
    var2 = set()
    var1.append(initial_state)
    while var1:
        state = var1.pop(0)
        if state.is_goal():
            return state
        var2.add(state)
        child = sucessors(state)
        for child in child:
            if (child not in var2) or (child not in var1):
                var1.append(child)

    return None

class State():
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None
        self.child = []

    def is_goal(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False

    def is_valid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False

## Here, all the states that are available are stated:
def sucessors(current_state):
    child = [];
    if current_state.boat == 'left':
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft - 2, 'right',
                          current_state.cannibalRight, current_state.missionaryRight + 2)

        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

#Moving from left to right.
        # (2C L->R)
        new_state = State(current_state.cannibalLeft - 2, current_state.missionaryLeft, 'right',
                          current_state.cannibalRight + 2, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        # (1c 1M L->R)
        new_state = State(current_state.cannibalLeft - 1, current_state.missionaryLeft - 1, 'right',
                          current_state.cannibalRight + 1, current_state.missionaryRight + 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        #(1M L->R)
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft - 1, 'right',
                          current_state.cannibalRight, current_state.missionaryRight + 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        #(1C L->R)
        new_state = State(current_state.cannibalLeft - 1, current_state.missionaryLeft, 'right',
                          current_state.cannibalRight + 1, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)
    else:
# Moving from right to left.
        # (2M R->L)
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft + 2, 'left',
                          current_state.cannibalRight, current_state.missionaryRight - 2)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        # (2C R->L)
        new_state = State(current_state.cannibalLeft + 2, current_state.missionaryLeft, 'left',
                          current_state.cannibalRight - 2, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        # (1M 1C R->L)
        new_state = State(current_state.cannibalLeft + 1, current_state.missionaryLeft + 1, 'left',
                          current_state.cannibalRight - 1, current_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        # (1M R->L)
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft + 1, 'left',
                          current_state.cannibalRight, current_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        # (1C R->L)
        new_state = State(current_state.cannibalLeft + 1, current_state.missionaryLeft, 'left',
                          current_state.cannibalRight - 1, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)
    return child

if __name__ == "__main__":
        print ("call from main function") #debug code
        main()

#var3 = True

#time.quit(10)        
#sys.exit()
#quit()


