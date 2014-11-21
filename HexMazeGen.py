from random import randint, shuffle
import sys
sys.setrecursionlimit(100000)

class Blocks:
    Void, Passage, Wall, Player = range(4)

def MazeGen(l_side, n_players, players_l_path_deviation):
    #[y][x] list, [x][y] otherwise
    def DFSMazeGen(x, y, i, random):
        cells[y][x]=Blocks.Passage     

        if randint(0,1)==0 and random and x!=1 and y!=l_side-1:
            rec.append([x, y, i])
            return

        #ur, r, dr, dl, l, ul
        d = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        shuffle(d)
        
        players[i].append([x, y])
        branching = False
        next_i = i
        for direct in d:
            conX = True if direct[0]==1 and x<h-2 else True if direct[0]==-1 and x>=2 else True if direct[0]==0 else False
            conY = True if direct[1]==1 and y<h-2 else True if direct[1]==-1 and y>=2 else True if direct[1]==0 else False
            if conX and conY:
                if cells[y+direct[1]*2][x+direct[0]*2]==Blocks.Wall:
                    if not branching:
                        branching = True
                    else:
                        players.append(list(players[i]))
                        next_i = len(players)-1
                    cells[y+direct[1]][x+direct[0]]=Blocks.Passage
                    DFSMazeGen(x+direct[0]*2, y+direct[1]*2, next_i, random);     

    h = 2*l_side-1
    cells = [[Blocks.Void for i in range(h)] for j in range(h)]
    #list of not-branched cells(<=randint)
    rec = []
    players = [[]]
    players_final = []
    #init cells
    for y in range(h):
        x1 = l_side-y-1 if y<l_side else (y%l_side)+1
        gap = range(x1, h) if y<l_side else range(h-x1)
        for x in gap:
            cells[y][x]=Blocks.Wall
    #gen maze        
    cells[l_side-1][0] = Blocks.Passage
    DFSMazeGen(1,l_side-1,0,True)
    for cell in rec:
        DFSMazeGen(cell[0],cell[1],cell[2],False)
    #do magic with players' positions   
    players.sort(key=len, reverse=True)
    max_dist_index = (1-players_l_path_deviation)*len(players[n_players-1])
    for i in range(len(players)):
        if len(players[i])>=max_dist_index:
            players_final.append(players[i])
    shuffle(players_final)
    for i in range(n_players):
        x = players_final[i][len(players_final[i])-1][0]
        y = players_final[i][len(players_final[i])-1][1]
        cells[y][x] = Blocks.Player
    return cells            
                        
f = open('maze.txt', 'w')
n_players = 4
l_side = 20
#(0<->1); not quite, the name is a bit misleading but whatever
players_l_path_deviation = 0.5
cells = MazeGen(l_side, n_players, players_l_path_deviation)
s = "\n"
counter = 0
for y in range(2*l_side-1):
    for x in range(2*l_side-1):
        counter += 1 if cells[y][x]==Blocks.Passage or cells[y][x]==Blocks.Player else 0;
        s += str(cells[y][x])
f.write(str(l_side*2-1))
f.write(s)
f.close()
