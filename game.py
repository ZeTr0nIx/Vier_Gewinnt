from calendar import c
from turtle import position
import pygame,sys

class Button: 

    def __init__(self, text,  pos, font, background=[255,255,255], feedback="",centered=True, action="exit"):
        self.x, self.y = pos
        self.background = background
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Arial", 30)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, background,centered)
        
    def change_text(self, text, background, centered):
        self.text = self.font.render(text, 1, BLACK)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(background)
        self.surface.blit(self.text, (0, 0))
        self.surface.set_alpha(200)
        if centered: 
            self.x = self.x-self.size[0]/2
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
 
    def click(self, event, victory):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if self.action == "exit" and victory:
                        sys.exit()

def draw_grid(grid):
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            color = LIGHT_GREY
            if grid[column][row] == 1:
                color = RED
            elif grid[column][row] == 2:
                color = YELLOW
            pygame.draw.circle(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row   + MARGIN],
                              RADIUS)


def drop_plate(grid, column, row, player):
    grid[column][row]=player
    if player == 1:
        return 2
    return 1


def check_for_victory(grid):

    def check_row(row):
        player_one = [0 , 1]
        player_two = [0 , 2]
        for column in range(COLUMN_COUNT):
            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
        return 0
    
    def check_column(column):
        player_one = [0 , 1]
        player_two = [0 , 2]
        for row in range(ROW_COUNT):

            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
        return 0

    def check_diagonal_right(start_row, start_column):
        player_one = [0 , 1]
        player_two = [0 , 2]
        row, column = start_row, start_column
        while column<COLUMN_COUNT and row < ROW_COUNT:
            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
            column +=1
            row+=1
        player_one = [0 , 1]
        player_two = [0 , 2]
        row, column = start_row, start_column
        while column>-1 and row >-1:
            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
            column -=1
            row-=1
        return 0

    def check_diagonal_left(start_row, start_column):
        player_one = [0 , 1]
        player_two = [0 , 2]
        row, column = start_row, start_column
        while column>-1 and row < ROW_COUNT:
            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
            column -=1
            row+=1
        player_one = [0 , 1]
        player_two = [0 , 2]
        row, column = start_row, start_column
        while column<COLUMN_COUNT and row >-1:
            if grid[column][row]==1:
                player_one[0]+=1
                player_two[0]=0
            elif grid[column][row]==2:
                player_two[0]+=1
                player_one[0]=0
            else:
                player_one[0]=0
                player_two[0]=0
            if player_one[0]==4:
                return player_one[1]
            elif player_two[0]==4:
                return player_two[1]
            column +=1
            row-=1
        return 0
    
    winner = 0
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            winner =check_column(column)
            if winner != 0:
                return winner
            winner =check_diagonal_right(row,column)
            if winner != 0:
                return winner
            winner =check_row(row)
            if winner != 0:
                return winner
            winner =check_diagonal_left(row,column)
            if winner != 0:
                return winner
            

def get_final_stacking_position(grid, column):
    for row in range(ROW_COUNT):
        if grid[column][row] == 1 or grid[column][row] == 2:
            return row-1
    return row

def create_new_grid():
    grid = []
    for column in range(COLUMN_COUNT):
        grid.append([])
        for row in range(ROW_COUNT):
            grid[column].append(0)
    return grid
            
SCREEN_SIZE = [440, 375]
SCREEN_CENTER = [SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2]
BLACK = 0,0,0
BLUE = 0,0,255
LIGHT_GREY= 200,200,200
GREY = 130,130,130
RED = 255,0,0
YELLOW = 255,255,0
GRID_CELL_SIZE = HEIGHT, WIDTH, MARGIN, RADIUS= 40,40,25,20
COLUMN_COUNT = 7
ROW_COUNT = 6
DROP_SPEED = 10

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.init()
pygame.display.set_caption("Vier Gewinnt")

grid = create_new_grid()

player = 1
victory = False
current_position = 0,0
final_position = 0,0
exit_button = Button("CLOSE",[SCREEN_CENTER[0],SCREEN_CENTER[1]+70],"Arial",GREY,centered=True)

while True:
    for event in pygame.event.get():
        
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not victory:
                pos = pygame.mouse.get_pos()
                
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                row = get_final_stacking_position(grid, column)
                
                if row>-1:
                    player = drop_plate(grid,column,row,player)
                
                victor = check_for_victory(grid)
                if victor == 1 or victor ==2:
                    victory = True
                current_position = row, column
                
            exit_button.click(event,victory)
            
                                    
    screen.fill(BLUE)
    draw_grid(grid)
    
    if victory:
        font = pygame.font.SysFont("Arial", 45)
        victory_phrase = "PLAYER {0} has won!".format(victor)
        img = font.render(victory_phrase, True, BLACK)
        rect = img.get_rect()
        pygame.draw.rect(img,BLACK,rect,1)
        screen.blit(img, ((SCREEN_SIZE[0]/2)-(img.get_width()/2), (SCREEN_SIZE[1]/3)))
        exit_button.show()
        
    pygame.display.update()