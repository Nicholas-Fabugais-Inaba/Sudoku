import pygame
from sudokusolver import solver, valid_num, create_puzzle, finish_grid, start_grid, find_empty

pygame.font.init()

def generate_Board():
    #generate random puzzle
    return create_puzzle(finish_grid(start_grid()))

class Grid:

    def __init__(self, rows, columns, width, height):
        #initialize board values
        self.board = generate_Board()
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.squares = [[Square(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]
        self.model = None
        self.selected = None

    def update_model(self):
        #updates the board model
        self.model = [[self.squares[i][j].num for j in range(self.columns)] for i in range(self.rows)]

    def place(self, num):
        #places inputted number into the board
        row, column = self.selected
        if self.squares[row][column].num == 0:
            self.squares[row][column].set(num)
            self.update_model()

            if valid_num(self.model, num, (row, column)) and solver(self.model):
                return True
            else:
                self.squares[row][column].set(0)
                self.squares[row][column].set_temp(0)
                self.update_model()
                return False

    def sketch(self, num):
        #places a 'sketched/temporary' value to aid the user
        row, column = self.selected
        self.squares[row][column].set_temp(num)

    def draw(self, window):
        #draws the board
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(window, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.columns):
                self.squares[i][j].draw(window)

    def select(self, row, column):
        #sets every square to be unselected 'False' and the actual row, column
        #of the selected square to be selected 'True'
        for i in range(self.rows):
            for j in range(self.columns):
                self.squares[i][j].selected = False

        self.squares[row][column].selected = True
        self.selected = (row, column)

    def clear(self):
        #clears the selected square to become empty '0'
        row, column = self.selected
        if self.squares[row][column].num == 0:
            self.squares[row][column].set_temp(0)

    def click(self, position):
        #returns the position on the board that is selected
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        #checks each value and if all values are not empty '0' board is finished
        
        for i in range(self.rows):
            for j in range(self.columns):
                if self.squares[i][j].num == 0:
                    return False
        return True


    def solve_board(self):
        
        empty = find_empty(self.board)
        if not empty:
            return True     #base case
        else:
            row, column = empty

        for num in range(1, 10):
            if valid_num(self.board, num, (row,column)):
                self.board[row][column] = num
                self.squares[row][column].set(num)
                pygame.time.delay(63)
                self.update_model()

                if self.solve_board():        #if solution found solver finishes
                    return True

                self.board[row][column] = 0
                self.squares[row][column].set(0)
                pygame.time.delay(63)
                self.update_model()
                    
        return False
        

class Square:

    rows = 9
    columns = 9

    def __init__(self, num, row, column, width, height):
        #initialize individual num values
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.num = num
        self.temp = 0
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.column * gap
        y = self.row * gap

        #draw sketch
        if self.temp != 0 and self.num == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            window.blit(text, (x+5, y+5))

        #draw board num value
        elif not(self.num == 0):
            
            text = font.render(str(self.num), 1, (0, 0, 0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        #draw red border around selected square
        if self.selected:
            pygame.draw.rect(window, (0, 0, 255), (x, y, gap, gap), 3)

    def set(self, num):
        #set num value to num
        self.num = num

    def set_temp(self, num):
        #set temp num value to num
        self.temp = num

class Button:

    def __init__(self, colour, x, y, width, height, text=''):
        #initialize values to button object properties
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):
        #draw button outline and text
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        

    def hover(self, position):
        #return if the button is hovered over with mouse or not
        if position[0] > self.x and position[0] < self.x + self.width:
            if position[1] > self.y and position[1] < self.y + self.height:
                return True
        return False


def redraw_window(window, board, button):
    #draw background window white
    window.fill((255, 255, 255))

    button.draw(window)
    board.draw(window)

def main():
    #initialize what will be displayed in the window
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    solveButton = Button((255, 255, 255), 215, 545, 110, 50, 'SOLVE')
    board = Grid(9, 9, 540, 540)
    key = None
    running = True


    #allows window to keep running until board is finished
    while running:
        
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if solveButton.hover(position):
                    print("SOLVING...")
                    board.solve_board()
                    print("SOLVED!")


            if event.type == pygame.MOUSEMOTION:
                if solveButton.hover(position):
                    solveButton.colour = (180, 180, 180)
                else:
                    solveButton.colour = (255, 255, 255)
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            print("SUCCESS!")
                        else:
                            print("WRONG")
                        key = None

                        if board.is_finished():
                            print("GAME OVER!")
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                    
        
        if board.selected and key != None:
            board.sketch(key)

        redraw_window(window, board, solveButton)
        pygame.display.update()


main()
pygame.quit()

            
