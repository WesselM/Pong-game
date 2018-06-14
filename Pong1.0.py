# Made by Wessel Mostert
# Finished on 7-6-2018

# imports
import arcade
import time

# define arcade window characteristics 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = " Pong1.0"
WINDOW_BACKGROUND_COLOR = arcade.color.LIGHT_GRAY

# the different pages that can be used
INSTRUCTIONS_PAGE = 0
GAME_RUNNING = 1
GAME_OVER_RED_WINS = 2
GAME_OVER_BLUE_WINS = 3

music_background = arcade.sound.load_sound(".\music_background.mp3")
arcade.sound.play_sound(music_background)


class Ball:
    def __init__(self, position_x, position_y, delta_x, delta_y, radius, color):
        # define Ball functions
        self.position_x = position_x
        self.position_y = position_y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.radius = radius
        self.color = color 
 
    def draw(self):
        # define what variables to draw when function is invoked
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self, delta_time, rectangle_list, current_state):
        # calls the functions that must be performed
        self.move(delta_time, current_state)
        self.check_bounds()
        self.check_col(rectangle_list)

    def move(self, delta_time, current_state):    
        # Movement speed & direction of the ball
        self.position_y += self.delta_y * delta_time * 4.1 
        self.position_x += self.delta_x * delta_time * 5.09
    
    def check_bounds(self):
        # bounce the ball of the screen edges
        if self.position_y <= self.radius:
            self.delta_y *= -1
            self.position_y = self.radius
        if self.position_y >= WINDOW_HEIGHT - self.radius:
            self.delta_y *= -1
            self.position_y = WINDOW_HEIGHT - self.radius

    def check_col(self, rectangle_list):
        for rectangle in rectangle_list:
            # check for collision between paddle & ball
            if self.position_x + self.radius >= rectangle.position_x - (rectangle.rect_width / 2) and \
            self.position_x - self.radius <= rectangle.position_x + (rectangle.rect_width / 2) and \
            self.position_y + self.radius >= rectangle.position_y - (rectangle.rect_height / 2) and \
            self.position_y - self.radius <= rectangle.position_y + (rectangle.rect_height / 2):
                self.delta_x *= -1


class Paddle:
    def __init__(self, position_x, position_y, rect_width, rect_height, color):
        # define Paddle functions
        self.position_x = position_x
        self.position_y = position_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.color = color
        self.delta_position_y = 0
        self.movement_speed = 10
    
    def draw(self):
        # define what variables to draw when function is invoked
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.rect_width, self.rect_height, self.color)

    def update(self, delta_time):
        # add the movement to the position
        self.position_y += self.delta_position_y

        # stops pabble when trying to move out of screen
        if self.position_y >= WINDOW_HEIGHT -(self.rect_height/2):
            self.delta_position_y = 0
            self.position_y = WINDOW_HEIGHT - (self.rect_height/2)
        if self.position_y <= 0 + (self.rect_height/2):
            self.delta_position_y = 0
            self.position_y = 0 + (self.rect_height/2)


class MyGame(arcade.Window):
    """ An Arcade game. """

    def __init__(self, width, height, title):
        """ Constructor. """
        super().__init__(width, height, title)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)

        # what state the progrem is in -> what page to use
        self.current_state = INSTRUCTIONS_PAGE

        # adds one ball with functions
        self.ball_list = []
        ball = Ball(WINDOW_HEIGHT/2, WINDOW_WIDTH/2, 50, 50, 20, arcade.color.MOSS_GREEN)
        self.ball_list.append(ball)

        # adds two rectangles with separate functions
        self.rectangle_list = []
        self.rectangle_list.append(Paddle(30, (WINDOW_HEIGHT/2), 20, 100, arcade.color.CADET_BLUE))
        self.rectangle_list.append(Paddle(WINDOW_WIDTH-30, (WINDOW_HEIGHT/2), 20, 100, arcade.color.REDWOOD))

        # define the scores
        self.left_score = 0
        self.right_score = 0

        # hide the mouse cursor
        self.set_mouse_visible(False)

    def draw_instructions_page(self): # what to draw on the instructions page
        # text to be drawn
        output = "Use the paddles to hit the ball and change it's trajectory.\n\
        If the ball goes behind your paddle, your opponent scores a point.\n\
The first person to earn 7 points is the winner.\n\n\
Blue; use the 'W' key to move up, and the 'S' key to move down.\n\
Red; use the 'up arrow' key to move up, and the 'down arrow' key to\n\
    move down.\n\n\
Press the space-bar to start"
        #where and how to draw the text
        arcade.draw_text(output, WINDOW_WIDTH/2, WINDOW_HEIGHT - ((WINDOW_HEIGHT - (WINDOW_HEIGHT/4 + 1))/2),arcade.color.DAVY_GREY, 16, width=WINDOW_WIDTH, align="center", anchor_x="center",anchor_y="center")

    def draw_game_over_red_wins(self): # what to draw on the game over screen when red wins
        arcade.draw_text("GAME OVER! \nRed has won the game.", WINDOW_WIDTH/2, WINDOW_HEIGHT - ((WINDOW_HEIGHT - (WINDOW_HEIGHT/6 + 1))/2),arcade.color.REDWOOD, 30, width=WINDOW_WIDTH, align="center", anchor_x="center",anchor_y="center")     
        arcade.draw_text("Press the space-bar to play again", WINDOW_WIDTH/2, WINDOW_HEIGHT/2.5,arcade.color.REDWOOD, 15, width=WINDOW_WIDTH, align="center", anchor_x="center",anchor_y="center")     
    
    def draw_game_over_red_wins(self): # what to draw on the game over screen when blue wins
        arcade.draw_text("GAME OVER! \nBlue has won the game.", WINDOW_WIDTH/2, WINDOW_HEIGHT - ((WINDOW_HEIGHT - (WINDOW_HEIGHT/6 + 1))/2),arcade.color.CADET_BLUE, 30, width=WINDOW_WIDTH, align="center", anchor_x="center",anchor_y="center")     
        arcade.draw_text("Press the space-bar to play again", WINDOW_WIDTH/2, WINDOW_HEIGHT/2.5,arcade.color.CADET_BLUE, 15, width=WINDOW_WIDTH, align="center", anchor_x="center",anchor_y="center")     


    def draw_game(self): # what to draw when the game is going on
        # if ball is in list, draw the left score, a devider, and then the right score
        for ball in self.ball_list:
            ball.draw()
            arcade.draw_text("%(left_score)s" %{"left_score":self.left_score}, WINDOW_WIDTH / 2 - 20, WINDOW_HEIGHT - 40, arcade.color.CADET_BLUE,30)
            arcade.draw_text("%(right_score)s" %{"right_score":self.right_score}, WINDOW_WIDTH / 2 + 20, WINDOW_HEIGHT - 40, arcade.color.REDWOOD,30)
            arcade.draw_text(" I", WINDOW_WIDTH/2 - 8, WINDOW_HEIGHT - 45, arcade.color.MOSS_GREEN, 40,)

        # if rectangles are called and available, draw them
        for rectangle in self.rectangle_list:
            rectangle.draw()

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()

        # draw the page that is adressed at the moment
        if self.current_state == INSTRUCTIONS_PAGE:
            self.draw_instructions_page()
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == GAME_OVER_RED_WINS:
            self.draw_game_over_red_wins()
        else:
            self.draw_game_over_red_wins() 

    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        if self.current_state == GAME_RUNNING:
            # update the score
            self.score()

            # if ball is in list, update/redraw it
            for ball in self.ball_list:
                ball.update(delta_time, self.rectangle_list, self.current_state)
            
            # if rectangles are in list, update/redraw them
            for rectangle in self.rectangle_list:
                rectangle.update(delta_time)  

    def reset(self): 
        #reset the scores for the left and the right side
        self.left_score = 0 
        self.right_score = 0 

        #reset the ball direction and movement speed
        for ball in self.ball_list:
            ball.delta_x = 50
            ball.delta_y = 50
        
        #reset the paddle position
        for rectangle in self.rectangle_list:
            rectangle.position_y = WINDOW_HEIGHT / 2

    def score(self):
        # if balls are in list, update/redraw them
        for ball in self.ball_list:
            # if the left side misses the ball, add one point to the right and respawn the ball in the left direction
            if ball.position_x <= ball.radius:
                ball.delta_x = -50
                ball.position_x = WINDOW_WIDTH/2
                ball.position_y = WINDOW_HEIGHT/2
                self.right_score += 1
            if self.right_score == 7:
                self.current_state = GAME_OVER_RED_WINS

            # if the right side misses the ball, add one point to the left and respawn the ball in the right direction
            if ball.position_x >= WINDOW_WIDTH - ball.radius:
                ball.delta_x = 50
                ball.position_x = WINDOW_WIDTH/2
                ball.position_y = WINDOW_HEIGHT/2
                self.left_score += 1 
            if self.left_score == 7:
                self.current_state = GAME_OVER_BLUE_WINS

    def on_key_press(self, key, modifiers):
        # change the  pages when the space-bar is pressed 
        if key == arcade.key.SPACE and self.current_state != GAME_RUNNING: # when the space-bar is pressed and the game is not in progress, change the screen.
            if self.current_state == INSTRUCTIONS_PAGE: # when in the instructions page, go to the game itself
                self.current_state = GAME_RUNNING
                self.reset()
            elif self.current_state == GAME_OVER_BLUE_WINS or GAME_OVER_RED_WINS: # when in the game over screen, start the game again
                self.current_state = GAME_RUNNING
                self.reset()

        # when key is pressed, activate movment for Y pos of left paddle
        if key == arcade.key.W:
            self.rectangle_list[0].delta_position_y = self.rectangle_list[0].movement_speed
        elif key == arcade.key.S:
            self.rectangle_list[0].delta_position_y = -self.rectangle_list[0].movement_speed

        # when key is pressed, activate movment for Y pos of right paddle
        if key == arcade.key.UP:
            self.rectangle_list[1].delta_position_y = self.rectangle_list[1].movement_speed
        elif key == arcade.key.DOWN:
            self.rectangle_list[1].delta_position_y = -self.rectangle_list[1].movement_speed

    def on_key_release(self, key, modifiers): 
        # if key released, stop movement of left paddle
        if key == arcade.key.W or key == arcade.key.S:
            self.rectangle_list[0].delta_position_y = 0

        # if key released, stop movement of right paddle
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rectangle_list[1].delta_position_y = 0
    

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()