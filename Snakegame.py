from pdb import Restart
import tkinter
import random

Rows = 25
Cols = 25 
Tile_size = 25 
Window_width = Tile_size * Rows
Window_height = Tile_size * Cols
#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = Window_width, height = Window_height)
canvas.pack()
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#center the window

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2)-(Window_width/2))
window_y = int((screen_height/2)-(Window_height/2))
window.geometry(f"{Window_width}x{Window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(5*Tile_size, 5*Tile_size) # single tile, snake's head
food = Tile(10*Tile_size, 10*Tile_size)
snake_body = []  # multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(e):   #e = event
    global velocityX, velocityY, game_over, score, snake_body, food

    if (game_over): 
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif(e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif(e.keysym == "Left" and velocityX != 1): 
        velocityX = -1
        velocityY = 0
    elif(e.keysym == "Right" and velocityX !=-1):
        velocityX = 1
        velocityY = 0

    #reset the game
    if (e.keysym == "space" and game_over == True):
        game_over = False
        velocityX = 0
        velocityY = 0 
        score = 0
        snake.x, snake.y = 5*Tile_size, 5*Tile_size
        snake_body.clear()
        food.x = random.randint(0, Cols-1)* Tile_size
        food.y = random.randint(0, Rows-1)* Tile_size
        move()
        draw()

#move the snake

def move(): 
    global snake, food, snake_body, game_over, score

    if (game_over):
        return
    if (snake.x < 0 or snake.x >= Window_width or snake.y < 0 or snake.y >= Window_height):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #collison
    if (snake.x == food.x and food.y == snake.y) : 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, Cols-1)* Tile_size
        food.y = random.randint(0, Rows-1)* Tile_size
        score += 1
    
    #update snake body
    for i in range(len(snake_body)-1,  -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y 


    snake.x += velocityX * Tile_size
    snake.y += velocityY * Tile_size
def draw():
    global snake, food, snake_body, game_over, score
    move()
    canvas.delete("all")

     #draw food
    canvas.create_rectangle(food.x, food.y, food.x + Tile_size, food.y + Tile_size, fill= "lime green")

    #draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + Tile_size, snake.y + Tile_size, fill = "red")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + Tile_size, tile.y + Tile_size, fill = "red")
    if (game_over): 
        canvas.create_text(Window_width/2, Window_height/2, font= "Chiller 30", text= f"Game Over: {score}", fill= "white")
    else: 
        canvas.create_text(30, 20, font = "Chiller", text = f"Score:{score}", fill = "white")

                                

   
    window.after(100, draw) #100ms = 1/10 of a second
draw()
def restart(e=None):
    global game_over, score, snake_body, velocityX, velocityY, snake, food

    game_over = False
    velocityX = 0
    velocityY = 0
    score = 0
    snake.x, snake.y = 5*Tile_size, 5*Tile_size
    snake_body.clear()
    food.x = random.randint(0, Cols-1) * Tile_size
    food.y = random.randint(0, Rows-1) * Tile_size


window.bind("<Key>", change_direction)
window.bind("<space>", restart)   # quand on appuie sur espace
window.mainloop()
