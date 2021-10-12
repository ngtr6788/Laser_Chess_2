import pygame
from pygame.locals import *

import laser_chess
from laser_chess import LaserChess
from laser_chess_consts import *
import laser_chess_ai

from typing import Tuple, List, TypedDict
from pathlib import Path
import time

"""
This module creates an interactive Laser Chess game implemented
by PyGame, as in, you can click on a piece on the screen and either move
or rotate that piece on the screen, interactive, no typing numbers or letters.

To move a piece, simply drag and drop. To rotate a piece, you press the left
button and press A for counterclockwise, D for clockwise.
"""

SQUARE_SIZE = 50

# Colour tuples
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (186, 24, 24)
BLUE   = (0, 14, 143)
SILVER = (192, 192, 192)
YELLOW = (255, 255, 0)

# Bringing the images together
pieces = Path("./laser chess pieces/")  # the folder the pieces are in
KING1_IMG = pygame.image.load(pieces / "king1.png")
KING2_IMG = pygame.image.load(pieces / "king2.png")
FEND1_IMG = pygame.image.load(pieces / "defender1.png")
FEND2_IMG = pygame.image.load(pieces / "defender2.png")
SWITCH1_IMG = pygame.image.load(pieces / "switch1.png")
SWITCH2_IMG = pygame.image.load(pieces / "switch2.png")
FLEC1_IMG = pygame.image.load(pieces / "deflector1.png")
FLEC2_IMG = pygame.image.load(pieces / "deflector2.png")
LASER1_IMG = pygame.image.load(pieces / "laser1.png")
LASER2_IMG = pygame.image.load(pieces / "laser2.png")

PIECE_TO_IMAGE = {KING_1: KING1_IMG,
                  KING_2: KING2_IMG,
                  FEND_E1: FEND1_IMG,
                  FEND_N1: pygame.transform.rotate(FEND1_IMG, 90),
                  FEND_W1: pygame.transform.rotate(FEND1_IMG, 180),
                  FEND_S1: pygame.transform.rotate(FEND1_IMG, 270),
                  FEND_E2: FEND2_IMG,
                  FEND_N2: pygame.transform.rotate(FEND2_IMG, 90),
                  FEND_W2: pygame.transform.rotate(FEND2_IMG, 180),
                  FEND_S2: pygame.transform.rotate(FEND2_IMG, 270),
                  SWITCH_NESW1: pygame.transform.rotate(SWITCH1_IMG, 90),
                  SWITCH_NWSE1: SWITCH1_IMG,
                  SWITCH_NESW2: pygame.transform.rotate(SWITCH2_IMG, 90),
                  SWITCH_NWSE2: SWITCH2_IMG,
                  FLEC_NE1: FLEC1_IMG,
                  FLEC_NW1: pygame.transform.rotate(FLEC1_IMG, 90),
                  FLEC_SW1: pygame.transform.rotate(FLEC1_IMG, 180),
                  FLEC_SE1: pygame.transform.rotate(FLEC1_IMG, 270),
                  FLEC_NE2: FLEC2_IMG,
                  FLEC_NW2: pygame.transform.rotate(FLEC2_IMG, 90),
                  FLEC_SW2: pygame.transform.rotate(FLEC2_IMG, 180),
                  FLEC_SE2: pygame.transform.rotate(FLEC2_IMG, 270),
                  LASER_H1: pygame.transform.rotate(LASER1_IMG, 90),
                  LASER_V1: LASER1_IMG,
                  LASER_H2: pygame.transform.rotate(LASER2_IMG, 90),
                  LASER_V2: LASER2_IMG}

TURN_COLOUR = {FIRST: BLUE, SECOND: RED}

class Piece(TypedDict):
  rect: pygame.Rect
  image: pygame.Surface
  piece: int
  player: int 

def main():
  pygame.init()

  # This is where our list of pieces would go. It is a list of dictionaries,
  # each containing the pieces' surrounding Rect data and Image.
  laser_board = LaserChess(ACE)
  pieces_list = LaserChess_to_dictlist(laser_board)

  # the drag and drop or clicky booleans and constants go here.
  drag_and_drop = False
  allow_rotate = False
  clicked_piece = None
  
  orig_pixel_coord = None
  orig_board_coord = None
  
  cur_player = FIRST
  move_made = False

  ai = False
  evaluate = False

  # I initially draw the screen first, in case bad stuff happens.
  SCREEN = laser_chess_screen()
  
  while True: # This is where the actual game thingy occurs.
    for event in pygame.event.get():
      if event.type == QUIT:
          # you close the window and we're done!
          terminate()
          return
      if ai and laser_board.winner == 0 and cur_player == SECOND:
        thing = laser_chess_ai.minimax(laser_board, depth=3, max_player=cur_player)
        print(thing) 
        points, loc, move = thing
        if not None in {loc, move}:
          move_made = laser_board.make_move(loc, move, cur_player)
        else:
          break
        pieces_list = LaserChess_to_dictlist(laser_board)
      else:
        if event.type == MOUSEBUTTONDOWN:          
          # if you click on a piece, it keeps track of what the piece is,
          # who owns it, and the original square's coordinates.
          if laser_board.winner == 0 and \
            event.button == 1:  # left mouse button
            
            for piece in pieces_list:
              if piece["rect"].collidepoint(event.pos):
                if cur_player == piece["player"]:
                  orig_pixel_coord = piece["rect"].topleft
                  orig_board_coord = pixel_to_board_coord(orig_pixel_coord)
                  drag_and_drop = True
                  allow_rotate = True
                  clicked_piece = piece
                break

        elif event.type == MOUSEBUTTONUP and True == drag_and_drop:
          # if you drop it, and the square is a legal place to be,
          # then the piece will *fit into* the square hovered by the mouse.

          # What's a legal move? The piece moves to an empty adjacent square
          # or, if it is a switch, it switches places with defenders
          # and deflectors, or the square is not illegal to be.

          # However, if the square clicked is not adjacent to its original
          # square, or is occupied, it stays in the original square.

          orig_coord_y, orig_coord_x = orig_board_coord

          new_board_coord = pixel_to_board_coord(event.pos)
          new_coord_y, new_coord_x = new_board_coord
          
          move = (new_coord_y - orig_coord_y, new_coord_x - orig_coord_x)

          new_pixel_coord = board_coord_to_pixel(new_board_coord)

          try:
            move_made = laser_board.make_move(orig_board_coord, \
                                              move, cur_player)
          except:
            move_made = False

          if True == move_made:
            clicked_piece["rect"].topleft = new_pixel_coord
            if clicked_piece["piece"] == SWITCH:
              # you look for the piece for the switch to switch
              for piece in pieces_list:
                if piece["rect"].collidepoint(event.pos) and \
                   piece != clicked_piece:
                  piece["rect"].topleft = orig_pixel_coord
                  break
          else:
            clicked_piece["rect"].topleft = orig_pixel_coord

          drag_and_drop = False
          allow_rotate = False
          
          clicked_piece = None
          
          orig_pixel_coord = None
          orig_board_coord = None         

        elif event.type == MOUSEMOTION:
          # if you move the piece, that piece loses its ability to rotate
          allow_rotate = False
          if drag_and_drop == True:
            # if you drag it around, the square would move around with the mouse
            clicked_piece["rect"].move_ip(event.rel)

        elif event.type == KEYDOWN and allow_rotate == True:
          # if you press a piece, that piece loses its ability to move
          
          # if you press A, it rotates anticlockwise. D = clockwise.
          drag_and_drop = False

          if event.key == K_d:
            # rotate clockwise
            clicked_piece["image"] = \
                          pygame.transform.rotate(clicked_piece["image"], -90)
            move = CW
          elif event.key == K_a:
            # rotate counter(anti)clockwise
            clicked_piece["image"] = \
                          pygame.transform.rotate(clicked_piece["image"], 90)
            move = ACW
          else:
            move = None

          if move in ROTATION_MOVES:
            laser_board.make_move(orig_board_coord, move, cur_player)
            move_made = True

          drag_and_drop = False
          allow_rotate = False
          
          clicked_piece = None
          
          orig_pixel_coord = None
          orig_board_coord = None
        
      # This is the place where the screen is updated.
      SCREEN = laser_chess_screen()

      # I draw all the non-dragging pieces in place.
      for piece in pieces_list:
        if (clicked_piece is None) or (clicked_piece != piece):
          SCREEN.blit(piece["image"].convert_alpha(), piece["rect"])

      if True == move_made:
        # I draw the laser beam.

        if evaluate == True:
          eval_before = laser_chess_ai.evaluate_board(laser_board, cur_player)
          print(f"Before laser evaluation: {eval_before}")
        
        animate_laser(SCREEN, laser_board, cur_player)
        pieces_list = LaserChess_to_dictlist(laser_board)

        if evaluate == True:
          eval_after = laser_chess_ai.evaluate_board(laser_board, cur_player)
          print(f"After laser evaluation: {eval_after}")

        cur_player = -cur_player  # change turns
        if cur_player == FIRST:
          p_str = "First"
        else:
          p_str = "Second"
        print(f"{p_str} player to move")

        laser_board.print_winner()
        
        move_made = False

      # I then draw the dragging piece last so it is above all others.
      if (not clicked_piece is None):  # ... if there is any.
        SCREEN.blit(clicked_piece["image"].convert_alpha(), \
                    clicked_piece["rect"])
        pygame.draw.rect(SCREEN, TURN_COLOUR[cur_player], \
                         clicked_piece["rect"], width = 1)

      pygame.display.update()  # Update the new board.

def terminate():
  # End the main game loop
  pygame.display.quit()
  pygame.quit()

def laser_chess_screen() -> pygame.Surface:
  # Displays a screen showing the Laser Chess game board.

  width = COLUMNS * (SQUARE_SIZE + 1) + 1
  height = ROWS * (SQUARE_SIZE + 1) + 1
  board = pygame.display.set_mode((width, height))
  board.fill(SILVER)

  for i in range(0, width, SQUARE_SIZE + 1):
    pygame.draw.line(board, BLACK, (i, 0), (i, height), 1)
  for j in range(0, height, SQUARE_SIZE + 1):
    pygame.draw.line(board, BLACK, (0, j), (width, j), 1)

  return board

def pixel_to_board_coord(pixel: Tuple[int, int]) -> Tuple[int, int]:
  # Converts the pixel location on the screen to board square coordinates

  pixel_x, pixel_y = pixel
  return (pixel_y // (SQUARE_SIZE + 1), pixel_x // (SQUARE_SIZE + 1))

def board_coord_to_pixel(board_coord: Tuple[int, int]) -> Tuple[int, int]:
  # Converts a square's board coordinates to the top-left pixel of that square

  board_y, board_x = board_coord
  return (board_x * (SQUARE_SIZE + 1) + 1, board_y * (SQUARE_SIZE + 1) + 1)

def LaserChess_to_dictlist(laserboard: LaserChess) -> List[Piece]:
  # This takes a LaserChess board object and creates a list of dictionaries.
  # Each dictionary contains the Rect object to drag to and the Image "blit"ed,
  # as well as the piece type and which player owns it.

  dictlist = []
  for i in range(ROWS):
    for j in range(COLUMNS):
      piece_dict = {"rect": None, "image": None, "piece": 0, "player": 0}
      board_coord = (i, j)
      pixel_coord = board_coord_to_pixel(board_coord)
      board_piece = laserboard.board[board_coord]
      if board_piece == 0:  # place is empty
        continue
      else:
        piece_dict["image"] = PIECE_TO_IMAGE.get(board_piece)
      piece_dict["rect"] = pygame.Rect(pixel_coord, (SQUARE_SIZE, SQUARE_SIZE))
      piece_dict["piece"] = laser_chess.find_piece(board_piece)
      piece_dict["player"] = laser_chess.find_player(board_piece)
      dictlist.append(piece_dict)
  return dictlist

def animate_laser(
  screen: pygame.Surface, laser_board: laser_chess.LaserChess, player: int
  ) -> None:
  # Draws the laser's path onto the screen.
  
  coord_path = laser_board.shoot_laser_path(player, capture=True)
  pixel_laser_path = []
  
  for board_coord in coord_path:
    board_y, board_x = board_coord
    centre_pixel = lambda x: (x * (SQUARE_SIZE + 1) + 1 + SQUARE_SIZE // 2)
    pixel_coord = (centre_pixel(board_x), centre_pixel(board_y))
    pixel_laser_path.append(pixel_coord)

  pygame.draw.lines(screen, RED, False, pixel_laser_path, 1)
  pygame.display.flip()
  time.sleep(0.1)
  

if __name__ == "__main__":
  """Things (steps) I learned along the way:
  STEP 1: See how I can implement a drag and drop on the screen. DONE!
  STEP 1.1: When drag and drop, how do I drop so piece fits square? DONE!
  STEP 1.2: How do I make the dragging piece above all pieces? DONE!

  STEP 2: What do I use for pieces? A: Images to upload with a Rect to be filled.
  STEP 2.1: How do I get a bazillion pieces then? DONE!
  STEP 2.2: How do I get the correct piece and orientation? DONE!

  STEP 3: How best should I rotate a shape? pygame.transform.rotate() DONE!

  STEP 4: Redesign the board grid so squares don't overlap grid. DONE!, sortof.

  STEP 5: How do I allow myself to move all those pieces? DONE!
  STEP 5.1: How do I make the pieces travel one adjacent square at a time? DONE!
  STEP 5.2: How do I allow the pieces to not be on top of each other? DONE!
  STEP 5.3: But how about switches and its special swapping rule? DONE!
  STEP 5.4: How about rotating the pieces? Click on it and press A or D. DONE!

  STEP 6: How do you animate the laser? DONE!
  STEP 6.1: How do eliminate pieces then? DONE!

  STEP 7: How do you do turn based things? DONE?!?

  STEP 8: Better ways to store the piece image and Rects and info? IDK

  STEP 9: I feel that most of this code, as well as the laser_chess module
          breaks the Zen of Python. I might want to rewrite my code, so it
          looks more readable. Too much bureaucracy. Too many tangled stuff.
  """
  main()
