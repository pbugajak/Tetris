import random


class Figure:
    """
    Matrix data for figures
    """
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 5, 9, 10], [4, 5, 6, 8], [1, 2, 6, 10], [2, 4, 5, 6]],
        [[2, 6, 9, 10], [2, 6, 10, 11], [6, 7, 10, 14], [5, 6, 7, 11]],
        [[1, 2, 6, 7], [2, 5, 6, 9]],
        [[1, 2, 5, 6]]
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]       # coordinate vector of current figure

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])  # rotation method

    def un_rotate(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])


class Tetris:
    field = []
    height = 0
    width = 0
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        for y in range(height):
            new_line = []
            for x in range(width):
                if x == 0 or x == width - 1 or y == height - 1:
                    new_line.append('*')
                else:
                    new_line.append(' ')
            self.field.append(new_line)

    """
    Method add '*' to field which contains the figure.
    """
    def add_figure(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.figure.x <= x < self.figure.x + 4 and self.figure.y <= y <= self.figure.y + 4:
                    p = (y - self.figure.y) * 4 + (x - self.figure.x)
                    if p in self.figure.image():
                        self.field[y][x] = '*'
                    elif self.field[y][x] != '*':
                        self.field[y][x] = ' '

    """
    Method that removes figures data from current move if we can make next move.
    """
    def remove_figure(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.figure.x <= x < self.figure.x+4 and self.figure.y <= y <= self.figure.y+4:
                    p=(y-self.figure.y)*4+(x-self.figure.x)
                    if p in self.figure.image():
                        self.field[y][x] = ' '

    def new_figure(self):               # creating new figure on our board
        self.figure = Figure(random.randint(1, self.width -4), 0)

    """
    This is very important, there is a loot of conditions base on which our game 
    will let us move forward our pieces, or not...
    """
    def intersects(self):       #
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] == '*':
                        intersection = True
                    if self.field[i + self.figure.y][j + self.figure.x] == '*':
                        intersection = True
        return intersection

    """
    Method for adding '*' on Tetries instance field.
    Added '*' symbols stays for the rest of the play.
    """
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = '*'
        self.new_figure()
        if self.intersects():   # condition to end the game
             exit()

    """
    Printing our self.figure on self.field
    """
    def let_see(self):
        if self.figure != None:
            self.add_figure()
        for x in range(self.width):
            for y in range(self.height):
                print(self.field[x][y], end='')
            print()
        if self.figure != None:
            self.remove_figure()

    def go_down(self):      # method to move block one by one y value to the base of the self.field
        self.figure.y += 1
        if self.intersects():   # also checking if it is possible
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):  # method to move block one by one x value to the base of the self.field
        old_x = self.figure.x   # executed also for 'a' and 'd'
        self.figure.x += dx
        if self.intersects():       # also checking if it is possible
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def un_rotate(self):
        old_rotation = self.figure.rotation
        self.figure.un_rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


if __name__ == "__main__":
    playground = Tetris(20, 20)         # new instance of Tetris class
    playground.let_see()
    playground.new_figure()             # added first figure to the field
    playground.let_see()                # printing our field with figure
    n = input()
    while n != 'END':                   # Command dependences from input to be executed
        if n == 'a':
            playground.go_side(-1)
            playground.go_down()
        elif n == 'd':
            playground.go_side(1)
            playground.go_down()
        elif n == 's':
            playground.un_rotate()
            playground.go_down()
        elif n == 'w':
            playground.rotate()
            playground.go_down()
        playground.let_see()
        n = input()
