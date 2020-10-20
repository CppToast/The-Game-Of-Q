import tkinter
import game
import os

field_size_x = 50
field_size_y = 30
spike_percentage = 0.02
coins_per_shield = 5
tile_size = 16

def restartGame():
    global game
    if not game.active:
        game.start()
        drawField()

def move(x,y):
    global game
    if game.active:
        game.move(x,y)
        drawField()

def drawField():
    global game, root_window, viewport_canvas
    global player_sprite, death_sprite, coin_sprite, shield_sprite, spike_sprite
    global coin_text, shield_text, status_text
    global field_size_x, field_size_y, tile_size

    coin_text.config(text = str(game.score))
    shield_text.config(text = str(game.shields))

    viewport_canvas.delete("all")
    for y in range(field_size_y):
        for x in range(field_size_x):
            if game.game_map[x][y] == 1:
                viewport_canvas.create_image(x * tile_size, y * tile_size, image = spike_sprite, anchor = "nw")
            if game.game_map[x][y] == 2:
                viewport_canvas.create_image(x * tile_size, y * tile_size, image = coin_sprite, anchor = "nw")
            if game.game_map[x][y] == 3:
                viewport_canvas.create_image(x * tile_size, y * tile_size, image = shield_sprite, anchor = "nw")
    if game.active:
        viewport_canvas.create_image(game.player_x * tile_size, game.player_y * tile_size, image = player_sprite, anchor = "nw")
        status_text.config(text = "")
    else:
        viewport_canvas.create_image(game.player_x * tile_size, game.player_y * tile_size, image = death_sprite, anchor = "nw")
        status_text.config(text = "You have died. Press space to restart the game.")

root_window = tkinter.Tk()
root_window.title("The Game of Q Remake by CppToast")
root_window.bind("w", lambda x: move(0,-1))
root_window.bind("a", lambda x: move(-1,0))
root_window.bind("s", lambda x: move(0,1))
root_window.bind("d", lambda x: move(1,0))
root_window.bind("<Up>", lambda x: move(0,-1))
root_window.bind("<Left>", lambda x: move(-1,0))
root_window.bind("<Down>", lambda x: move(0,1))
root_window.bind("<Right>", lambda x: move(1,0))
root_window.bind("<space>", lambda x: restartGame())

player_sprite = tkinter.PhotoImage(file = os.path.dirname(__file__)+"/gfx/player.png")
death_sprite = tkinter.PhotoImage(file = os.path.dirname(__file__)+"/gfx/death.png")
coin_sprite = tkinter.PhotoImage(file = os.path.dirname(__file__)+"/gfx/coin.png")
shield_sprite = tkinter.PhotoImage(file = os.path.dirname(__file__)+"/gfx/shield.png")
spike_sprite = tkinter.PhotoImage(file = os.path.dirname(__file__)+"/gfx/spike.png")

root_window.iconphoto(True, coin_sprite)

viewport_canvas = tkinter.Canvas(width = tile_size * field_size_x, height = tile_size * field_size_y, bd = 0, highlightthickness = 0)
viewport_canvas.grid(column = 0, row = 0, columnspan = field_size_x)
viewport_canvas.config(bg = "#402800")

coin_icon = tkinter.Label(image = coin_sprite)
coin_icon.grid(column = 0, row = 1, sticky = "w")
coin_text = tkinter.Label(text = "0")
coin_text.grid(column = 1, row = 1, sticky = "w")

shield_icon = tkinter.Label(image = shield_sprite)
shield_icon.grid(column = 0, row = 2, sticky = "w")
shield_text = tkinter.Label(text = "0")
shield_text.grid(column = 1, row = 2, sticky = "w")

status_text = tkinter.Label(text = "OK")
status_text.grid(column = 2, row = 1, sticky = "e", columnspan = field_size_x - 2)

game = game.Game(field_size_x, field_size_y, spike_percentage, coins_per_shield)
game.start()

drawField()

tkinter.mainloop()