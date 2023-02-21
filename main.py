import time
import pygame
import numpy as np

#CONSTANTS

BGCOLOUR = (230, 230, 230)
GRIDCOLOUR = (255, 255, 255)
DEADCELL = (230, 230, 230)
ALIVECELL = (28, 28, 28)

FRAME_WIDTH = 1000
FRAME_LENGTH = 600
ROWS = 60
COLUMNS = 100
SIZE = 10

#function applies game rules and updates all individual cells
def update(screen, cells, size, with_progress=False):
    #with_progress contains update within one generation, allowing for synchronised update
    #create temp lattice structure
    #numpy function creates 2D array of inherited dimension, where each cell can inherit state of 1 or 0
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        colour = BGCOLOUR if cells[row, col] == 0 else ALIVECELL

        if row == ROWS:
            row = row%ROWS
        if col == COLUMNS-1:
            col = col%COLUMNS-1

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    colour = DEADCELL
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = ALIVECELL

        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = ALIVECELL

        pygame.draw.rect(screen, colour, (col*size, row*size, size-1, size-1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_LENGTH))

    #np.zero function enables cells to inherit '0' and be considered empty cells
    #forms lattice of rowsxcolumns
    cells = np.zeros((ROWS, COLUMNS))

    screen.fill(GRIDCOLOUR)

    update(screen, cells, SIZE) #returns updated lattice

    pygame.display.flip()
    pygame.display.update()

    running = False

    #game loop - when given a signal, will trigger update process
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                #when space bar pressed, changes activity status relatively
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, SIZE)
                    pygame.display.update()
            #when mouse is pressed on a cell, cell changes state from dead to alive
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1]//SIZE, pos[0]//SIZE] = 1
                #since position of mouse is given by a list of [x, y],
                #y will represenht rows position of the array, x will represent columnn position
                update(screen, cells, SIZE)
                pygame.display.update()

        screen.fill(GRIDCOLOUR)

        #runs actual simulation as updates cells
        if running:
            cells = update(screen, cells, SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()