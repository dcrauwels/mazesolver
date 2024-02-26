from tkinter import Tk, BOTH, Canvas

def function_announce(f):
    def wrapper(*args, **kwargs):
        print(f"Calling: {f.__name__}")
        f(*args, **kwargs)
    return wrapper

class Window:
    def __init__(self, width, height) -> None:
        
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
        self.__canvas = Canvas()
        self.__canvas.pack(fill=BOTH, expand=1)

        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("--window closed--")
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2) -> None:
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand = 1)

class Cell:
    def __init__(
            self,
            xy_tl, 
            xy_br, 
            lw = True, rw = True, tw = True, bw = True,
            win = None, 
            ) -> None:
        self.has_left_wall = lw
        self.has_right_wall = rw
        self.has_top_wall = tw
        self.has_bottom_wall = bw
        self._visited = False
        self._x1= xy_tl[0]
        self._x2 = xy_br[0]
        self._y1 = xy_tl[1]
        self._y2 = xy_br[1]
        self._win = win

    def draw(self):
        #Draw cell by making four walls in walls list.
        #Draws either background color or black based on has_x_wall

        walls = []
        wall_existence = [self.has_left_wall, self.has_right_wall, 
                self.has_top_wall, self.has_bottom_wall]

        walls.append(
                Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        walls.append(
                Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        walls.append(
                Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        walls.append(
                Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))

        if self._win is not None:
            for i in range(4):
                self._win.draw_line(walls[i], "black" if wall_existence[i] else "#d9d9d9")
    
    def draw_move(self, to_cell, undo=False):
        #Draws a line from one cell to target to_cell.
        #Uses middle of cell based on cell data members x1 x2 y1 y2
        own_middle_x = (self._x1 + self._x2) / 2
        own_middle_y = (self._y1 + self._y2) / 2
        target_middle_x = (to_cell._x1 + to_cell._x2) / 2
        target_middle_y = (to_cell._y1 + to_cell._y2) / 2

        print(f"Own coordinates: {self._x1}, {self._y1}; {self._x2}, {self._y2}.")
        print(f"Line starting point: {own_middle_x}, {own_middle_y}")
        print(f"Line ending point: {target_middle_x}, {target_middle_y}")

        cell_line = Line(
                Point(own_middle_x, own_middle_y),
                Point(target_middle_x, target_middle_y))
        cell_line_color = "red" if undo else "gray"

        self._win.draw_line(cell_line, cell_line_color)
    
    def _break_walls_r(self, i, j, seed = None):
        #Recursively break walls to make a maze.
        import random
        if seed is not None:
            random.seed(seed)

        self._visited = True
        while True:
            ij_list = []

        
class Maze:
    #Init has a bunch of parameters plus call to local function _create_cells()
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            ) -> None:
        self._x1 = x1
        self._y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()

    def _create_cells(self):
        #Create empty cells array and then populate with cells.
        #x and y coords are based on Wall parameters (starting x1, y1 and cell size)
        self._cells = []
        for c in range(self.num_cols):

            column = [Cell(
                    (self._x1 + self._cell_size_x * r, self._y1 + self._cell_size_y * c),
                    (self._x1 + self._cell_size_x * (r+1), self._y1 + self._cell_size_y * (c+1)),
                    win = self._win,
                    ) for r in range(self.num_rows)]

            self._cells.append(column)
        self._animate()
        self._break_entrance_and_exit()

    def _animate(self):
        #Draw cells one by one (nested loop)
        for col in self._cells:
            for cel in col:
                cel.draw()
                if self._win is not None:
                    self._win.redraw()
                from time import sleep
                #Sleep, may want to comment this out later.
                sleep(0.05)

    def _break_entrance_and_exit(self):
        #Break top wall in top left and bottom wall in bottom right cell
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False

        #Redraw
        self._cells[0][0].draw()
        self._cells[-1][-1].draw()

        

def main():
    win = Window(800,600)
    
    #l1 = Line(Point(20, 200), Point(30, 300))
    #l2 = Line(Point(600, 100), Point(100, 400))
    #win.draw_line(l1, "blue")
    #win.draw_line(l2, "red")
  
    #c1 = Cell((40, 40), (60,60), False, True, True, True, win) 
    #c2 = Cell((80, 40), (120, 80), True, False, True, False, win)
    #c1.draw()
    #c2.draw()

    #c1.draw_move(c2)
    
    maze1 = Maze(100, 100, 4, 4, 100, 100, win)

    # dont touch this
    win.wait_for_close()


if __name__ == "__main__":
    main()
