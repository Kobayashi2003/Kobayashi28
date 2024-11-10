#! /usr/bin/env python3
''' An easy way to text test some mazes '''
import mazes

def experiment1():
    g = mazes.Grid(10,12)
    mazes.binary_tree(g)

    m = mazes.Markup(g)
    g.set_markup(m)
    print(g)
    
def experiment2():
    g = mazes.Grid(10,12)
    mazes.binary_tree(g)

    start = g.cell_at(0,0)    
    m = mazes.DijkstraMarkup(g, start)
    
    g.set_markup(m)
    print(g)
    
def experiment3():
    g = mazes.Grid(10,15)
    mazes.sidewinder(g)
    
    start = g.cell_at(9,0)
    goal  = g.cell_at(9,14)      
    dm = mazes.DijkstraMarkup(g, start)
    spm = mazes.ShortestPathMarkup(g,start,goal)
    farthest, distance = dm.farthest_cell()
    g.set_markup(dm)
    print(g)
    g.set_markup(spm)
    print(g)
    print(f'The farthest cell from {start} is {farthest} which has a distance of {distance}')

def experiment4():
    g = mazes.Grid(10,15)
    mazes.sidewinder(g)
    
    lp = mazes.LongestPathMarkup(g, path_marker='X', non_path_marker='.')
    g.set_markup(lp)
    print(g)
        
def main():
    experiment4()

if __name__ == "__main__":
    main()