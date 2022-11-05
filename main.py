# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#f1f1f1",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    right = my_head["x"] + 1
    left = my_head["x"] - 1
    up = my_head["y"] + 1
    down = my_head["y"] - 1

    cell_up = {"x": my_head["x"], "y": up}
    cell_down = {"x": my_head["x"], "y": down}
    cell_left = {"x": left, "y": my_head["y"]}
    cell_right = {"x": right, "y": my_head["y"]}

    if down < 0:
      is_move_safe["down"] = False
      
    if left < 0:
      is_move_safe["left"] = False
      
    if right >= board_width:
      is_move_safe["right"] = False
      
    if up >= board_height:
      is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    
    if cell_up in my_body:
      is_move_safe["up"] = False

    if cell_down in my_body:
      is_move_safe["down"] = False

    if cell_left in my_body:
      is_move_safe["left"] = False

    if cell_right in my_body:
      is_move_safe["right"] = False
    
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    opponent_cells = []
    opponent_body_cells = {}
    opponent_head_cells = {}

    safe_moves_counter = 0
    for directions in is_move_safe:
        if directions:
          safe_moves_counter += 1
  
    for opponent in opponents:
      for opponent_body_cell in opponent["body"]:
        opponent_cells.append({"x": opponent_body_cell["x"], "y": opponent_body_cell["y"]})
        opponent_body_cell.setdefault(opponent["id"], []).append({"x": opponent_body_cell["x"], "y": opponent_body_cell["y"]})
      opponent_cells.append({"x" :opponent["head"]["x"], "y" :opponent["head"]["y"]})
      opponent_head_cells[opponent["id"]] = {"x" :opponent["head"]["x"], "y" :opponent["head"]["y"]}
      
      """if safe_moves_counter > 1:
        opponent_cells.append({"x" :opponent["head"]["x"] + 1, "y" :opponent["head"]["y"]})
        opponent_cells.append({"x" :opponent["head"]["x"] - 1, "y" :opponent["head"]["y"]})
        opponent_cells.append({"x" :opponent["head"]["x"], "y" :opponent["head"]["y"] + 1})
        opponent_cells.append({"x" :opponent["head"]["x"], "y" :opponent["head"]["y"] - 1})"""


    if cell_up in opponent_cells:
      is_move_safe["up"] = False

    if cell_down in opponent_cells:
      is_move_safe["down"] = False

    if cell_left in opponent_cells:
      is_move_safe["left"] = False

    if cell_right in opponent_cells:
      is_move_safe["right"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
      
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    foods = game_state['board']['food']
    for food in foods:
      food["distance"] = math.sqrt((food["x"] - my_head["x"])**2 + (food["y"] - my_head["y"])**2)
    food_sorted_distance = sorted(foods, key=lambda d: d['distance'])
    for food in food_sorted_distance:
      in_between_x = []
      in_between_y = []
      if food["x"] > my_head["x"]:
        x_step = -1
      else:
        x_step = 1
      if food["y"] > my_head["y"]:
        y_step = -1
      else:
        y_step = 1
      for x in range(food["x"], my_head["x"], x_step):
        in_between_x.append(x)
      for y in range(food["y"] - my_head["y"], y_step):
        in_between_y.append(y)
      for x in in_between_x:
        for y in in_between_y:
          if {"x": x, "y": y} in opponent_cells:
            food["danger"] = food.get("danger", 0) + 1
      if food.get("danger", 0) == 0:
        food["score"] = food["distance"]
      else:
        food["score"] = food["distance"] * 1/food["danger"]
    preferred_foods = sorted(foods, key=lambda d: d["score"])
    for food in preferred_foods:
      if food["x"] < my_head["x"] and is_move_safe["left"]:
        print("left")
        return {"move": "left"}
      if food["x"] > my_head["x"] and is_move_safe["right"]:
        print("right")
        return {"move": "right"}
      if food["y"] < my_head["y"] and is_move_safe["down"]:
        print("down")
        return {"move": "down"}
      if food["y"] > my_head["y"] and is_move_safe["up"]:
        print("up")
        return {"move": "up"}


    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
