import random

def reset_grid():
    #resets grid to be completely empty
    empty_grid = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
    return empty_grid


def print_grid(grid):
    #prints out grid in an organized format
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


def find_empty(grid):
    
    for x in range(len(grid)): #row
        for y in range(len(grid[0])): #column
            if grid[x][y] == 0: #if row(x),column(y) is 0(empty)
                return (x,y)    #this will be position

    return None #if there is no empty square

def valid_num(grid, num, position):   #num represents empty square input
    #checks row
    for i in range(len(grid[0])):
        if grid[position[0]][i] == num and position[1] != i: 
            return False
    #checks column
    for j in range(len(grid)):
        if grid[j][position[1]] == num and position[0] != j:
            return False

    #checks box
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != position:
                return False

    return True
    

def solver(grid):

    empty = find_empty(grid)
    if not empty:
        return True     #base case
    else:
        row, column = empty

    for i in range(1, 10):
        if valid_num(grid, i, (row,column)):
            grid[row][column] = i

            if solver(grid):        #if solution found solver finishes
                return True

            grid[row][column] = 0
            
    return False
    


def start_grid():

    #generates 3 valid and filled boxes diagonal to each other
    grid = reset_grid()
    num_list = list(range(1,10))
    for row in range(3):
        for column in range(3):
            random_num = random.choice(num_list)
            grid[row][column] = random_num
            num_list.remove(random_num)

    num_list = list(range(1,10))
    for row in range(3, 6):
        for column in range(3, 6):
            random_num = random.choice(num_list)
            grid[row][column] = random_num
            num_list.remove(random_num)

    num_list = list(range(1,10))
    for row in range(6, 9):
        for column in range(6, 9):
            random_num = random.choice(num_list)
            grid[row][column] = random_num
            num_list.remove(random_num)
    
    return grid

def finish_grid(grid):
    #fills rest of the grid with valid boxes
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == 0:
                random_num = random.randint(1, 9)

                if valid_num(grid, random_num, (row,column)):
                    grid[row][column] = random_num

                    if solver(grid):
                        finish_grid(grid)
                        return grid

                    grid[row][column] = 0
                    
    return False

def check_repeat(row, column, position_list):
    #checks for a repeat position
    for i in range(len(position_list)):
            if (row, column) == position_list[i]:
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                check_repeat(row, column, position_list)
                return True
                
    return False
                

def create_puzzle(grid):
    #removes random positions of a solvable sudoku puzzle
    position_list = []
    
    while len(position_list) < 40:

        row = random.randint(0, 8)
        column = random.randint(0, 8)
        if not check_repeat(row, column, position_list):
            position_list.append((row, column))
            grid[row][column] = 0

    return grid

print_grid(start_grid())
print("")
print("- - - - - - - - - - - -")
print("")
print_grid(finish_grid(start_grid()))
print("")
print("- - - - - - - - - - - -")
print("")
print_grid(create_puzzle(finish_grid(start_grid())))

