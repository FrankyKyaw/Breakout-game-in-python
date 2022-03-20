"""

Breakout game

Object classes:
    Ball object- bounces in all directions except down 
    Wall object- gets destroyed when hit, similar to the player object 
    Player object- bounces the ball in different directions when hit

Franky Kyaw | Intro to CS | May 2021
"""

from graphics import *

columns = 5
rows = 5
width = 1 / rows
height = 0.05
lose = 0

def make_window(color):
    """ Return a Zelle window with coordinates (0,0) to (1,1) """
    window = GraphWin("Ball Game", 600, 600, autoflush=False)
    window.setBackground(color)
    window.setCoords(0, 0, 1, 1)
    return window

class Ball:
    def __init__(self, player, radius, x, y, dx,dy, color, window):
        self.window = window
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.player = player
        self.circle = Circle(Point(x, y), radius)
        self.circle.setFill(color)
        self.circle.draw(self.window)

        
    def reverse_dx(self):
        """ reverse x direction of motion """
        self.dx = - self.dx
        self.circle.move(self.dx, self.dy)

    def reverse_dy(self):
        """ reverse y direction of motion """
        self.dy = - self.dy
        self.circle.move(self.dx, self.dy)
        
    def position(self):
        """ returns the four coordinates of the ball.
              ****0****
           **          **
         **              **
        *                  *
        *                  *
        0                  0
        *                  *
        *                  *
         **              **
           **          **
             *****0****
        """
        
        center = self.circle.getCenter()
        y = center.getY()
        x = center.getX()
        ball_top = Point(x, y + self.radius)
        ball_bottom = Point(x, y - self.radius)
        ball_left = Point(x - self.radius, y)
        ball_right = Point(x + self.radius, y)
        return ball_top, ball_bottom, ball_left, ball_right

    def bounce_angle(self, dx_angle):
        """ bounces the ball back depending on the x position that the ball
        hits the paddle. """
        self.dx = -0.02 + (0.005) * dx_angle
        self.dy = -self.dy
        self.circle.move(self.dx, self.dy)
        
    def move(self, player):
        """ moves the object and detects collisions with other objects
            and the walls of window"""
        # gets the positions of the player and the ball
        left, right, top, bottom = self.player.position()
        ball_top, ball_bottom, ball_left, ball_right = self.position()
        
        # checks for collision with the player
        if ball_bottom.getY() <=  top and \
           left <= ball_bottom.getX() <= right:
            # the point that the ball hits is divided by a constant
            # which will determine the angle of the ball bounce
            dx_angle = (ball_bottom.getX() - left) // 0.025
            self.bounce_angle(dx_angle)
        # checks for collision with the walls
        elif ball_right.getX() >= 1 or \
             ball_left.getX() <= 0:
            self.reverse_dx()
        # checks for collision with the ceiling
        elif ball_top.getY() >= 1:
            self.reverse_dy()
        # checks if the ball goes under the window 
        elif ball_top.getY() < 0:
            lose = 1
            return lose
        else:
            self.circle.move(self.dx, self.dy)        

class Player:
    def __init__(self, x, y, color, window):
        self.window = window
        self.x = x
        self.y = y
        self.rect = Rectangle(Point(x,y), Point(x + width, y + height))
        self.rect.setFill(color)
        self.rect.draw(window)

    def position(self):
        """ returns the four corners coordinates of the paddle. """
        p1 = self.rect.getP1()
        p2 = self.rect.getP2()
        left = p1.getX()
        right = p2.getX()
        top = p2.getY()
        bottom = p1.getY()
        return left, right, top, bottom

    def block_position(self):
        """ returns the four corner coordinates of the blocks"""
        bottom_left = Point(self.x, self.y)
        top_left = Point(self.x, self.y + height)
        bottom_right = Point(self.x + width, self.y)
        top_right = Point(self.x + width, self.y + height)
        return bottom_left, top_left, bottom_right, top_right


    def play(self):
        """ checks for a key and moves the paddle left or right"""
        keyString = self.window.checkKey()
        if keyString == "a":
            self.rect.move(-0.03, 0)
        elif keyString == "d":
            self.rect.move(0.03, 0)

class Wall:
    def __init__(self, ball, window):
        self.window = window
        self.wall = []
        self.ball = ball
        
    def create_wall(self):
        """ Creates a wall according to the number of columns and rows. """
        x = 0    # These are the starting values for the first block
        y = 0.95
        for row in range(rows):
            for col in range(columns + 1):
                self.wall.append(Player(x,y, "blue", self.window))
                x = col * width
            x = 0  # After a row is done, the x starts from 0 again.
            y = y - height
           
    def detect_collision(self):
        """ Gets the position of the ball and checks it with the position of
        every block in the wall. If there is a collision, the block will be
        undrawn, the ball will bounce off and the i value will be return. """
        
        ball_up, ball_bottom, ball_left, ball_right = self.ball.position()
        for i in range(len(self.wall)):
            bottom_left, top_left, bottom_right, top_right = self.wall[i].block_position()
            # detect bottom side collision with top of ball
            if bottom_left.getX() <= ball_up.getX() <= bottom_right.getX() and \
               bottom_left.getY() <= ball_up.getY():
                self.wall[i].rect.undraw()
                self.ball.reverse_dy()
                return i
            # detect top side collision with bottom of ball
            elif top_left.getX() <= ball_bottom.getX() <= top_right.getX() and \
                 top_left.getY() <= ball_bottom.getY():
                self.wall[i].rect.undraw()
                self.ball.reverse_dy()
                return i
            # detect left side collision with right side of ball
            elif bottom_left.getY() <= ball_right.getY() <= top_left.getY() and \
                 bottom_left.getX() == ball_right.getX():
                self.wall[i].rect.undraw()
                self.ball.reverse_dx()
                return i
            # detect right side collision with left side of ball
            elif bottom_right.getY() <= ball_left.getY() <= top_right.getY() and \
                 bottom_right.getX() == ball_left.getX():
                self.wall[i].rect.undraw()
                self.ball.reverse_dx()
                return i
            
    def delete_blocks(self):
        """ If there is a collision detected, the collided block will be
            destroyed and it will be deleted from the list. """
        i = self.detect_collision()
        if i:
            self.wall.pop(i)
        elif i == 0:
            # The previous condition does not check for 0 value so this is added
            self.wall.pop(i)
class Game:
    def __init__(self):
        """ Creates a game with window, player, ball, wall and win and lose messages."""
        self.window = make_window("black") 
        self.player = Player(0.4, 0.05, "green", self.window)
        self.ball = Ball(self.player, 0.03, 0.5,0.13, 0.01, -0.01,
                                      "white", self.window)
        self.start_message = Text(Point(0.5,0.5), "Press t to start the game.")
        self.start_message.setTextColor("white")
        self.lose_message = Text(Point(0.5,0.5), "Game Over!")
        self.lose_message.setTextColor("white")
        self.win_message = Text(Point(0.5,0.5), "You won!")
        self.win_message.setTextColor("white")
        
        self.wall = Wall(self.ball, self.window)
        self.wall.create_wall()
        

    def lose(self):
        """ Prints a message "Game Over!" on the window. """
        self.lose_message.draw(self.window)
        
    def win(self):
        """ Prints a message "You Won!" on the window. """
        self.win_message.draw(self.window)
            
    def run(self):
        # The program gets a key when it runs. So the first key pressed should
        # be a "t" or the program won't start.
        self.start_message.draw(self.window)
        start = self.window.getKey()
        if start == "t":
            self.start_message.undraw()
            while True:
                # moves the ball and also checks if player loses
                if(self.ball.move(self.player)):
                    self.lose()
                    break
                self.player.play() # checks for player input that controls the paddle
                self.wall.delete_blocks() # deletes block if there are collisions 
                if len(self.wall.wall) == 0: # checks for win when there are no more blocks
                    self.win()
                    break
                update(30)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
