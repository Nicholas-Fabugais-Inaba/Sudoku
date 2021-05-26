grid = [
       [0,0,0,3,0,0,0,0,0],
       [0,0,0,1,4,6,7,5,0],
       [0,6,0,0,2,0,0,9,8],
       [1,0,2,4,0,0,0,8,6],
       [0,0,4,0,5,2,3,0,0],
       [7,0,0,0,0,0,0,0,0],
       [3,0,0,0,8,0,0,7,1],
       [2,9,0,0,0,0,0,0,0],
       [0,0,6,7,0,5,4,0,0]
]

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
        return True
    else:
        row, column = empty

    for i in range(1, 10):
        if valid_num(grid, i, (row,column)):
            grid[row][column] = i

            if solver(grid):
                return True

            grid[row][column] = 0

    return False

def print_grid(grid):
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

print_grid(grid)
solver(grid)
print_grid(grid)




