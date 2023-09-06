import turtle
import random
from levels import level_1, level_2, level_3, level_4, level_5, level_6
from sprites import sprite_images

wn = turtle.Screen()
wn.bgcolor('#1c2f2f')
wn.title('Maze Game')
wn.setup(width=700, height=700)
wn.tracer(0)
grid_block_size = 24

# set up sprites
for sprite in sprite_images:
    wn.register_shape(sprite)


# classes
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color('#362020')
        self.shape("jungle.gif")
        self.penup()
        self.speed(0)
        self.name = 'Wall'


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Player'
        self.shape("player-right.gif")
        self.gold = 0

    def move_up(self):
        new_x_cor = self.xcor()
        new_y_cor = self.ycor() + 24
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)

    def move_down(self):
        new_x_cor = self.xcor()
        new_y_cor = self.ycor() - 24
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(self.xcor(), self.ycor() - 24)

    def move_left(self):
        new_x_cor = self.xcor() - 24
        new_y_cor = self.ycor()
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)
            self.shape("player-left.gif")

    def move_right(self):
        new_x_cor = self.xcor() + 24
        new_y_cor = self.ycor()
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)
            self.shape("player-right.gif")

    def hide(self):
        hide_sprite(self)


class LeftParen(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shape('lParen.gif')
        self.goto(x, y)
        self.name = "LeftParen"

    def hide(self):
        hide_sprite(self)

class RightParen(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shape('rParen.gif')
        self.goto(x, y)
        self.name = "RightParen"

    def hide(self):
        hide_sprite(self)


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.gold = 50
        self.name = 'Enemy'
        self.shape('enemy-right.gif')
        self.setposition(x, y)
        self.direction = set_direction()

    def change_direction(self):
        if self.direction == 'up':
            dx = 0
            dy = 24
        elif self.direction == 'down':
            dx = 0
            dy = -24
        elif self.direction == 'left':
            dx = -24
            dy = 0
            self.shape('enemy-left.gif')
        elif self.direction == 'right':
            dx = 24
            dy = 0
            self.shape('enemy-right.gif')

        # check if player is near
        if self.distance(player) < (difficulty * 100):
            if player.xcor() < self.xcor():
                self.direction = 'left'

            elif player.xcor() > self.xcor():
                self.direction = 'right'

            elif player.ycor() < self.ycor():
                self.direction = 'down'

            elif player.ycor() > self.ycor():
                self.direction = 'up'

        # move enemy
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # check for collisions
        check = check_wall_collision(move_to_x, move_to_y, walls)
        if check:
            self.setposition(move_to_x, move_to_y)
        else:
            # choose a different direction
            self.direction = set_direction()

        # reposition enemies after a certain time has passed
        wn.ontimer(self.change_direction, t=random.randint(100, 300))

    def hide(self):
        hide_sprite(self)


# functions
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)
            if character == 'X':
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            if character == 'P':
                player.setposition(screen_x, screen_y)
            if character == 'L':
                left_parenthesis.append(LeftParen(screen_x, screen_y))
            if character == 'R':
                right_parenthesis.append(RightParen(screen_x, screen_y))
            if character == 'E':
                enemies.append(Enemy(screen_x, screen_y))

def is_valid_parentheses(s):
    if len(s) % 2 != 0:
        return False
    stack = []
    open_paren = set('L')
    matches = set([ ('L', 'R') ])
    for paren in s:
        if paren in open_paren:
            stack.append(paren)
        else:
            if len(stack) == 0:
                return False
            last_open = stack.pop()
            if (last_open, paren) not in matches:
                return False
    return len(stack) == 0

def game_over():
    print("Secuencia de parentesis invalida! Juego Terminado!")

display_turtle = turtle.Turtle()
display_turtle.hideturtle()  # Hide the turtle icon
display_turtle.penup()  # Prevent drawing lines
display_turtle.goto(-200, 300)

def collision_check(sprite1, sprite2, block_size):
    global players_parenthesis

    if sprite2.distance(sprite1) < block_size:
        if sprite2.name == 'LeftParen':
            players_parenthesis += '('
            sprite2.hide()
            left_parenthesis.remove(sprite2)
        if sprite2.name == 'RightParen':
            players_parenthesis += ')'
            sprite2.hide()
            right_parenthesis.remove(sprite2)
        if not is_valid_parentheses(players_parenthesis):
            game_over()
        
        # Clear the previous text
        display_turtle.clear()
        display_turtle.color('#fedb6f')
        # Write the new collected parentheses string
        display_turtle.write(players_parenthesis, align="left", font=("Consolas", 30, "bold"))
        game_over()
        if sprite2.name == 'Enemy':
            sprite1.hide()
            print("Player with {} gold was killed by a hunting skeleton! GAME OVER!".format(player.gold))


def start_enemies_moving(t):
    for enemy in enemies:
        wn.ontimer(enemy.change_direction, t=t)


def set_direction():
    return random.choice(['up', 'down', 'left', 'right'])


def hide_sprite(sprite):
    sprite.setposition(2000, 2000)
    sprite.hideturtle()


def check_wall_collision(next_x, next_y, object_list):
    if (next_x, next_y) not in object_list:
        return True
    else:
        return False


# class instances
pen = Pen()
player = Player()

# keyboard bindings
key_mapping = {
    "Up": player.move_up,
    "Down": player.move_down,
    "Left": player.move_left,
    "Right": player.move_right
}

for key, action in key_mapping.items():
    wn.onkeypress(action, key)

wn.listen()

# game status
mapList = [level_1, level_2, level_3, level_4, level_5, level_6]
levelsList = [l for l in mapList]
walls, enemies, left_parenthesis, right_parenthesis = [], [], [], []
players_parenthesis = ''
difficulty = 1

# append levels to levels list
rdLevel = random.randint(0, len(levelsList) - 1)
print(f"Jugando en el nivel {rdLevel + 1}...")
setup_maze(levelsList[rdLevel])
# set enemies moving after given timer
start_enemies_moving(250)
# main loop
while True:
    # check player and treasure collision
    [collision_check(player, l, grid_block_size) for l in left_parenthesis]
    [collision_check(player, r, grid_block_size) for r in right_parenthesis]
    
    # check player and enemy collision
    [collision_check(player, e, grid_block_size) for e in enemies]
    
    # update screen
    wn.update()
