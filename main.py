from tkinter import Tk, BOTH, Canvas

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
            self, window, xy_tl, xy_br, 
            lw = True, rw = True, tw = True, bw = True
            ) -> None:
        self.has_left_wall = lw
        self.has_right_wall = rw
        self.has_top_wall = tw
        self.has_bottom_wall = bw
        self._x1= xy_tl[0]
        self._x2 = xy_br[0]
        self._y1 = xy_tl[1]
        self._y2 = xy_br[1]
        self._win = window

    def draw(self):
        walls = []

        if self.has_left_wall:
            walls.append(
                    Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        if self.has_right_wall:
            walls.append(
                    Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        if self.has_top_wall:
            walls.append(
                    Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        if self.has_bottom_wall:
            walls.append(
                    Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))

        for w in walls:
            self._win.draw_line(w, "black")
    
    def draw_move(self, to_cell, undo=False):
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
        
class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            ) -> None:
        pass


def main():
    win = Window(800,600)
    l1 = Line(Point(20, 200), Point(30, 300))
    l2 = Line(Point(600, 100), Point(100, 400))
    win.draw_line(l1, "blue")
    win.draw_line(l2, "red")
    
    c1 = Cell(win, (40, 40), (60,60), False, True, True, True)
    c2 = Cell(win, (80, 40), (120, 80), True, False, True, False)
    c1.draw()
    c2.draw()

    c1.draw_move(c2)

    # dont touch this
    win.wait_for_close()


if __name__ == "__main__":
    main()
