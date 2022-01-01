import random as rd

def add(m1,m2):
    for i in range(2):
        m1[i] += m2[i]
    
    return m1
    
def copy(board):
    return [[j for j in i] for i in board]

def mprint(m,ref=[],sep=" ",blank=" "):
    n = len(m)-2
    if ref == []:
        ref = m
    for i in range(1,n+1):
        for j in range(1,n+1):
            if ref[i][j] != None:
                print(m[i][j], end=sep)
            else:
                print(blank, end=sep)
        print()

def make_board(string):
    lines = string.split(";")
    n = len(lines)
    board = [[None for j in range(n)] for i in range(n)]

    for i in range(n):
        items = lines[i].split(",")
        for j in range(n):
            if items[j].isnumeric():
                board[i][j] = int(items[j])
            elif items[j] == "X":
                board[i][j] = items[j]

    return board

def cast(board):
    n = len(board)
    casted = [["X" for i in range(n+2)]] + [["X"]+i+["X"] for i in board] + [["X" for i in range(n+2)]]
    return casted

class Game:
    def __init__(self,n,board=[]):
        if board != []:
            self.Board = cast(board)
            self.n = len(board)
        else:
            self.Board = self.gen_board(n)
            self.n = n
        
        self.Shadow = [[int(self.Board[i][j] != "X") for j in range(self.n+2)] for i in range(self.n+2)]
        self.LiveShadow = copy(self.Shadow)
        self.gen_puzzle()
        self.Puzzle = [[(self.Board[i][j] if self.LiveShadow[i][j] != None else None) for j in range(self.n+2)] for i in range(self.n+2)]

    #--- PUZZLE GENERATION

    def gen_puzzle(self):
        queue = [(i,j) for j in range(1,self.n+1) for i in range(1,self.n+1)]

        for y in range(1,self.n+1):
            for x in range(1,self.n+1):
                neighbours = self.visit(self.Shadow,y,x,strict=True,count=False)
                if (y,x) in queue and self.Board[y][x] != "X" and len(neighbours)==1 and neighbours[0] in queue:
                    self.LiveShadow[y][x] = None
                    queue.remove((y,x))
                    queue.remove(neighbours[0])
                if self.Board[y][x] == "X" and self.visit(self.LiveShadow,y,x,strict="True"):
                    self.LiveShadow[y][x] = None
                    queue.remove((y,x))
                if len(neighbours) == 0 and self.Shadow[y][x] == 0:
                    self.LiveShadow[y][x] = None
                    queue.remove((y,x))

        while queue != []:
            y, x = rd.choice(queue)
            print("("+str(y)+", "+str(x)+")", self.LiveShadow[y][x])
            queue.remove((y,x))

            play = copy(self.LiveShadow)
            play[y][x] = None
            temp_puzz = [[(None if play[i][j] == None else self.Board[i][j]) for j in range(0,self.n+2)] for i in range(0,self.n+2)]

            sol = Game.solve(temp_puzz)
            if sol == self.Shadow:
                self.LiveShadow[y][x] = None
                mprint(self.LiveShadow)

    
    #--- PUZZLE GENERATION

    def new(self,n=0):
        if n == 0:
            n = self.n
        else:
            self.n = n
        
        self.Board = self.generate(self.n)

        self.Shadow = [[int(self.Board[i][j] != "X") for j in range(self.n+2)] for i in range(self.n+2)]
        self.LiveShadow = copy(self.Shadow)
        self.gen_puzzle()
        self.Puzzle = [[(self.Board[i][j] if self.LiveShadow[i][j] != None else None) for j in range(self.n+2)] for i in range(self.n+2)]

    #--- PUZZLE SOLVING

    @staticmethod
    def solve(Puzzle, LiveShadow=[]):
        n = len(Puzzle)-2

        if LiveShadow == []:
            LiveShadow = copy(Puzzle)
            for i in range(n+2):
                for j in range(n+2):
                    if Puzzle[i][j] == "X":
                        LiveShadow[i][j] = 0
                    elif Puzzle[i][j] == None:
                        LiveShadow[i][j] = None
                    else:
                        LiveShadow[i][j] = 1
        
        PuzzShadow = copy(LiveShadow)

        queue = [(i,j) for j in range(1,n+1) for i in range(1,n+1) if LiveShadow[i][j] == None]
        solvable = True

        while queue != [] and solvable:
            i = 0

            while i < len(queue) and solvable:
                y,x = queue[i]
                checklist = Game.visit(PuzzShadow,y,x,count=False)
                play = copy(LiveShadow)
                is0 = True
                is1 = True
                checklist = [point for point in checklist if PuzzShadow[point[0]][point[1]] != None]
                if len(checklist) > 0:
                    for y_,x_ in checklist:
                        play[y][x] = 0
                        if is0:
                            h = Game.visit(play,y_,x_)
                            is0 = (h >= Puzzle[y_][x_])
                        
                        play[y][x] = 1
                        if is1:
                            g = Game.visit(play,y_,x_,strict=True)
                            is1 = (g <= Puzzle[y_][x_])

                if Game.visit(LiveShadow,y,x,strict=True) == 0 and Game.visit(LiveShadow,y,x) == 0:
                    is0 = True
                    is1 = False

                if is1 != is0:
                    LiveShadow[y][x] = int(is1)
                    queue.pop(i)
                    break
                else:
                    solvable = (is0 or is1)
                    breakp = (y,x)
                    i += 1
            if i == len(queue) and solvable and not(Game.solved(LiveShadow)):
                solvable = False
                breakp = (y,x)

        if not(solvable):
            return (None, breakp)
        else:
            return LiveShadow
    
    #--- END OF PUZZLE SOLVING

    @staticmethod
    def visit(board,row,col,strict=False,count=True):
        x = col
        y = row
        n = len(board)-2
        sum = 0
        neighbours = []
        for m in [(0,1),(1,0),(0,-1),(-1,0)]:
            y, x = add([row,col],m)
            
            while (x >= 0 and y >= 0 and x <= n+1 and y <= n+1) and ((strict == False and board[y][x] != 0) or (strict == True and board[y][x] == 1)):
                if count:
                    sum += 1
                else:
                    neighbours.append((y,x))
                y, x = add([y,x],m)
        
        if count:
            return sum
        else:
            return neighbours
    
    @staticmethod
    def solved(board):
        for i in board:
            for j in i:
                if j == None:
                    return False
        return True

    @staticmethod
    def gen_board(n):
        board = [[0 for i in range(n)] for j in range(n)]

        for j in range(n):
            s = -1
            k = rd.randint(n//2,n)
            for i in range(k):
                s += rd.randint(1,n//2)
                if s >= n:
                    break
                else:
                    board[j][s] = "X"

        board = cast(board)

        mprint(board)

        j = 1
        xcount = 0

        while j <= n:
            i = 1
            while i <= n:
                if board[j][i] != "X":
                    sum = 0
                    restart = False
                    for m in [(0,1),(1,0),(0,-1),(-1,0)]:
                        x = i
                        y = j
                
                        y, x = add([y,x],m)
                
                        while board[y][x] != "X" and restart == False:
                            sum += 1
                
                            if sum > n:
                                board[j][i] = "X"
                                j = 1
                                i = 0
                                xcount = 0
                                restart = True
                    
                            y, x = add([y,x],m)
                
                        if restart == True:
                            break
                
                    if sum == 0:
                        board[j][i] = "X"
                        xcount += 1
                    elif restart == False:
                        board[j][i] = sum
                else:
                    xcount += 1
                i += 1
            j += 1
        
        return board