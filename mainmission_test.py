
import pygame, sys
from pygame.locals import *

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


def sucessors(current_state):
    child = [];
    if current_state.boat == 'left':
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft - 2, 'right',
                          current_state.cannibalRight, current_state.missionaryRight + 2)

        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## Two cannibals crossing from left to right.
        new_state = State(current_state.cannibalLeft - 2, current_state.missionaryLeft, 'right',
                          current_state.cannibalRight + 2, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One missionary and one cannibal crossing from left to right.
        new_state = State(current_state.cannibalLeft - 1, current_state.missionaryLeft - 1, 'right',
                          current_state.cannibalRight + 1, current_state.missionaryRight + 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One missionary crossing from left to right.
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft - 1, 'right',
                          current_state.cannibalRight, current_state.missionaryRight + 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One cannibal crossing from left to right.
        new_state = State(current_state.cannibalLeft - 1, current_state.missionaryLeft, 'right',
                          current_state.cannibalRight + 1, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)
    else:
        ## Two missionaries crossing from right to left.
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft + 2, 'left',
                          current_state.cannibalRight, current_state.missionaryRight - 2)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## Two cannibals crossing from right to left.
        new_state = State(current_state.cannibalLeft + 2, current_state.missionaryLeft, 'left',
                          current_state.cannibalRight - 2, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One missionary and one cannibal crossing from right to left.
        new_state = State(current_state.cannibalLeft + 1, current_state.missionaryLeft + 1, 'left',
                          current_state.cannibalRight - 1, current_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One missionary crossing from right to left.
        new_state = State(current_state.cannibalLeft, current_state.missionaryLeft + 1, 'left',
                          current_state.cannibalRight, current_state.missionaryRight - 1)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)

        ## One cannibal crossing from right to left.
        new_state = State(current_state.cannibalLeft + 1, current_state.missionaryLeft, 'left',
                          current_state.cannibalRight - 1, current_state.missionaryRight)
        if new_state.is_valid():
            new_state.parent = current_state
            current_state.child.append(new_state)
            child.append(new_state)
    return child


def breadth_first_search():
    initial_state = State(3, 3, 'left', 0, 0)
    if initial_state.is_goal():
        return initial_state
    frontier = list()
    explored = set()
    frontier.append(initial_state)
    while frontier:
        state = frontier.pop(0)
        if state.is_goal():
            return state
        explored.add(state)
        child = sucessors(state)
        for child in child:
            if (child not in explored) or (child not in frontier):
                frontier.append(child)

    return None


def main():
    # ai_solving = False
    pygame.init()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    window  = 1000, 680
    background = pygame.image.load('River.jpg')
    background = pygame.transform.scale(background, window)
    # screen = pygame.display.set_mode((1024, 768), FULLSCREEN)
    screen = pygame.display.set_mode(window, HWSURFACE | DOUBLEBUF | RESIZABLE)
    pygame.display.set_caption("AI ASSIGNMENT:SIMULATION OF MISSIONARIES_CANNIBAL PROBLEM")
    #size = (640, 486)  # as that of bg image
    #screen = pygame.display.set_mode(size)
    #pygame.display.set_caption("Missionary and Cannibal AI Game")

    # graphics.
    #background = pygame.image.load("river.jpg").convert()
    boat = pygame.image.load("boat.png").convert_alpha()
    boat.set_colorkey(WHITE)
    cannibal = pygame.image.load("cannibal.png").convert_alpha()
    cannibal.set_colorkey(WHITE)
    missionary = pygame.image.load("human.png").convert_alpha()

    # Set positions
    background_position = [0, 0]
    boatleft_position = [250, 250]
    boatright_position = [500, 250]

    done = False

    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                pygame.quit()
                sys.exit()

        # Copy image to screen:
        screen.blit(background, background_position)

        solution = breadth_first_search()
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
                    screen.blit(cannibal, [730 + (j * 20), 350])

            if state.missionaryLeft > 0:
                for i in range(1, state.missionaryLeft + 1):
                    screen.blit(missionary, [i * 20 + 30, 150])

            if state.missionaryRight > 0:
                for j in range(1, state.missionaryRight + 1):
                    screen.blit(missionary, [700 + (j * 20), 200])

            pygame.display.update()
            pygame.time.delay(3000)
            screen.fill(WHITE)

            # Copy image to screen:
            screen.blit(background, background_position)
            '''

           for p in range(len(state.child)):
                state = state.child[len(state.child) - p - 1]

            if state.boat == 'left':
                screen.blit(boat, boatleft_position)

            if state.boat == 'right':
                screen.blit(boat, boatright_position)

            if state.cannibalLeft > 0:
                for i in range(1, state.cannibalLeft + 1):
                    screen.blit(cannibal, (i * 20+50, 300))

            if state.cannibalRight > 0:
                for j in range(1, state.cannibalRight + 1):
                    screen.blit(cannibal, [680 + (j * 20), 200])

            if state.missionaryLeft > 0:
                for i in range(1, state.missionaryLeft + 1):
                    screen.blit(missionary, [i * 20 + 10, 200])

            if state.missionaryRight > 0:
                for j in range(1, state.missionaryRight + 1):
                    screen.blit(missionary, [700 + (j * 20), 200])

            # update the screen
            p = p + 1
            pygame.display.update()
            pygame.time.delay(3000)'''

            screen.blit(background, background_position)

    pygame.display.flip()

    pygame.time.Clock().tick(60)



pygame.quit()



# if called from the command line, call main()
if __name__ == "__main__":
    main()
