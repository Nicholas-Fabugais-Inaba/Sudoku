import pygame
from sudokusolver import solver, valid_num, create_puzzle, finish_grid, start_grid, find_empty
import time
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

    def new_board(self, window, board, time, button1, button2):
        #generates a new board
        self.board = generate_Board()
        self.rows = board.rows
        self.columns = board.columns
        self.width = board.width
        self.height = board.height
        self.squares = [[Square(self.board[i][j], i, j, self.width, self.height) for j in range(self.columns)] for i in range(self.rows)]
        self.model = None
        self.selected = None
        redraw_window(window, board, time, button1, button2)
        pygame.display.update()

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
        try:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.squares[i][j].selected = False

            self.squares[row][column].selected = True
            self.selected = (row, column)
        except IndexError:
            self.selected = None

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


    def solve_board(self, window, board, time, button1, button2):

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                exit()
        
        empty = find_empty(self.board)
        if not empty:
            return True     #base case
        else:
            row, column = empty

        for num in range(1, 10):
            if valid_num(self.board, num, (row,column)):
                self.select(row, column)
                self.board[row][column] = num
                self.squares[row][column].set(num)
                pygame.time.delay(63)
                redraw_window(window, board, time, button1, button2)
                pygame.display.update()

                if self.solve_board(window, board, time, button1, button2):        #if solution found solver finishes
                    return True

                self.select(row, column)
                self.board[row][column] = 0
                self.squares[row][column].set(0)
                pygame.time.delay(63)
                redraw_window(window, board, time, button1, button2)
                pygame.display.update()
                    
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

    def __init__(self, color, x, y, width, height, text=''):
        #initialize values to button object properties
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):
        #draw button outline and text
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

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


def redraw_window(window, board, time, button1, button2):
    #draw background window white
    window.fill((255, 255, 255))

    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render(str(time), 1, (0,0,0))
    window.blit(text, (374, 542))
    
    button1.draw(window)
    button2.draw(window)
    board.draw(window)


def main():
    #initialize what will be displayed in the window
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    solveButton = Button((255, 255, 255), 195, 545, 150, 50, 'SOLVE')
    new_gameButton = Button((255, 255, 255), 0, 545, 180, 50, 'NEW GAME')
    board = Grid(9, 9, 540, 540)
    x_arrow_movement = 0
    y_arrow_movement = 0
    key = None
    running = True
    start = time.time()


    #allows window to keep running until board is finished
    while running:
            
        time_passed = round(time.time() - start)
        play_time = time.strftime('%H:%M:%S', time.gmtime(time_passed))
        
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                #quits out of pygame window
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #if solve button is pressed, visually solves the board using a recursive backtracking algorithm
                if solveButton.hover(position):
                    if board.is_finished():
                        print("GAME OVER!")
                    else:
                        print("SOLVING...")
                        board.solve_board(window, board, play_time, solveButton, new_gameButton)
                        print("SOLVED!")
                #if new game button is pressed, creates a new board
                if new_gameButton.hover(position):
                    board.new_board(window, board, play_time, solveButton, new_gameButton)
                    print("NEW GAME!")
                    start = time.time()

                x_arrow_movement = 0
                y_arrow_movement = 0


            if event.type == pygame.MOUSEMOTION:
                #buttons change color when mouse is hovering over their position
                if solveButton.hover(position):
                    solveButton.color = (180, 180, 180)
                else:
                    solveButton.color = (255, 255, 255)
                    
                if new_gameButton.hover(position):
                    new_gameButton.color = (180, 180, 180)
                else:
                    new_gameButton.color = (255, 255, 255)
            
            if event.type == pygame.KEYDOWN:
                #number keys pressed set key to number, arrow keys pressed move in arrow key direction
                #backspace clears number from board, if sketched
                #return key enters in sketched number
                if event.key == pygame.K_UP:
                    try:
                        y_arrow_movement-=1
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                        key = None
                    except (UnboundLocalError, TypeError):
                        clicked = (5, 4)
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                    
                if event.key == pygame.K_DOWN:
                    try:
                        y_arrow_movement+=1
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                        key = None
                    except (UnboundLocalError, TypeError):
                        clicked = (3, 4)
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                    
                if event.key == pygame.K_LEFT:
                    try:
                        x_arrow_movement-=1
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                        key = None
                    except (UnboundLocalError, TypeError):
                        clicked = (4, 5)
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                    
                if event.key == pygame.K_RIGHT:
                    try:
                        x_arrow_movement+=1
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                        key = None
                    except (UnboundLocalError, TypeError):
                        clicked = (4, 3)
                        board.select(clicked[0]+y_arrow_movement, clicked[1]+x_arrow_movement)
                    
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

            #selects square clicked on by mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                    
        #key sketched into square
        if board.selected and key != None:
            board.sketch(key)


        redraw_window(window, board, play_time, solveButton, new_gameButton)
        pygame.display.update()


main()
pygame.quit()

            
