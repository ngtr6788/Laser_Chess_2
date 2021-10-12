import numpy as np
from typing import Sequence, Tuple, Union
from laser_chess_consts import *
from copy import deepcopy

"""
LaserChess, invented by Luke Hooper and Michael Larson, is a strategy game
combining chess-like moves with lasers eliminating pieces. The board has
mirrored pieces and your goal is to get your mirror pieces to get your laser
to hit your opponent's king while keeping your king from your opponent's laser.

For more information, go to https://www.thinkfun.com/products/laser-chess/ to
buy the board, and
https://www.thinkfun.com/wp-content/uploads/2017/10/LaserCh-1034-Instructions.pdf
for more info on rules.

Rules: 
Each player has kings, defenders, switches, deflectors and lasers.

If a player's king is hit, the other player wins.

A defender has a "safe" side. If the laser hits that side, it is not
eliminated. It "blocks" the laser. Otherwise, it's eliminated from the game.

A switch is a piece with two mirrors, one on each side. The mirrors change
the direction of the laser by 90 degrees, so the laser can go ziggly zaggly
as you want, because the mirrors make a 45 degree angle from the square sides.

A deflector is a piece with one mirror. If it is hit on a non-mirror side,
it's eliminated from the game. 

The laser, well, shoots the laser. The player can rotate the laser piece
90 degrees. The laser cannot move to another square.

On each turn, a player can either:
1. Move a piece on an adjacent square, or
2. Rotate a piece, including the laser, 90 degrees.

A switch can swap places with another deflector or defender.

After that, the player's laser is fired and hands the turn to the other player.
"""

"""
Quick note on integer piece notation:

- The sign says which player owns that piece.
- The first digit encodes the piece type.
- The second digit encodes the piece orientation.
Check the laser_chess_consts.py for more info on which number is which
"""

def make_piece(player: int, piece: int, orientation: int) -> int:
  """
  This function returns a number that encodes a pieces's info.

  For example:
  -22 is the second player's deflector whose mirror is facing SW
  41 is the first player's defender whose shield is facing E

  requires: player is a valid PLAYER number (1 or -1)
            piece is a valid piece (LASER to KING)
            0 <= orientation <= 3
            orientation is valid for the piece type (not asserted)
  """
  assert player in PLAYER
  assert piece in PIECE_TYPES
  assert 0 <= orientation <= 3
  return player * (piece + orientation)

def make_empty_board() -> np.ndarray:
  """
  Makes a board with just the laser pieces pointing vertically
  into the board.
  """
  board = np.zeros((ROWS, COLUMNS))
  board[0, 0] = LASER_V2
  board[ROWS - 1, COLUMNS - 1] = LASER_V1
  return board

def find_player(piece: int) -> int:
  """
  Returns the sign encoding the player.
  For example:
  -23 belongs to the second player, so -1
  11 belongs to the first player, so 1
  """
  if (piece > 0):
    return FIRST
  elif (piece < 0):
    return SECOND
  else:
    return 0

def find_piece(piece: int) -> int:
  """
  Returns the type of piece, as an integer encoding in the piece
  """
  return (abs(piece) // 10) * 10

def find_orient(piece: int) -> int:
  """
  Returns the orientation of the piece, as an encoded integer.
  """
  return abs(piece) % 10

def tuple_add(
  tuple1: Sequence[float], tuple2: Sequence[float]
  ) -> Sequence[float]:
  """
  Add two equally sized tuple of numbers, index by index.
  requires: tuple1 and tuple2 is equally sized
  """
  assert len(tuple1) == len(tuple2)
  return tuple(np.array(tuple1) + np.array(tuple2))

def num_orientations(piece_type: int) -> int:
  """
  Finds the number of distinct orientations the piece has
  requires: piece_type is a valid piece type
  """
  assert piece_type in PIECE_TYPES
  if piece_type == LASER:
    return 2
  elif piece_type == DEFLECTOR:
    return 4
  elif piece_type == SWITCH:
    return 2
  elif piece_type == DEFENDER:
    return 4
  elif piece_type == KING:
    return 1

def coord_within_bounds(location: Tuple[int, int]) -> bool:
  """
  Determines if the tuple coordinate is within the bounds of the board
  """
  return (0 <= location[0] < ROWS) and (0 <= location[1] < COLUMNS)

class LaserChess():
  """
  The LaserChess object is the representation of the
  Laser Chess game, with the board, pieces and their
  orientation, as well as legal ways to make a move and shooting lasers.

  It provides a way to make a move and shooting the laser, as well as
  automatically changing turns with your opponent and dealing with
  invalid moves.
  """

  def __init__(self, setup_method: Union[np.ndarray, Sequence[Sequence[int]]],
               player_to_move: int = FIRST):
    """
    Constructs a Laser Chess board.
    By default, the first player goes first.

    requires: setup_method is a 8 x 10 2-D Numpy array
              
              Both ways must be set up using the integer representation
              of pieces. [not asserted] The second player's laser is at the top-left corner,
              and the first player's laser is at the bottom-right corner.
              Both players have a king.

              player_to_move is FIRST or SECOND (is the current player's turn)
    """

    assert player_to_move in PLAYER
    assert isinstance(setup_method, np.ndarray)

    assert np.shape(setup_method) == (ROWS, COLUMNS)
    assert setup_method[0, 0] in {-11, -10} # second player laser
    assert setup_method[ROWS - 1, COLUMNS - 1] in {10, 11} # first player laser
    assert KING_1 in setup_method # first player king
    assert KING_2 in setup_method # second player king

    self.board = deepcopy(setup_method)
    self.turn = player_to_move
    self.winner = 0

  def print_winner(self) -> None:
    if self.winner == FIRST:
      print("First player wins")
    elif self.winner == SECOND:
      print("Second player wins")
    else:
      print("No winner yet")

  def make_move(self, location: Tuple[int, int], \
                move_type: Union[Tuple[int, int], int],
                player_turn = None) -> bool:
    """
    On each turn, a player chooses a location on the board
    and the move they want to make (lasers included), and
    if it is a valid move, the move is made and returns True,
    False otherwise.

    A valid move must take a player's own piece at that location on the
    board and the move can be done (for example, a "move" move takes
    a piece to an empty adjacent square)

    If player_turn is not specified, then we use self.turn instead.

    requires: location is within the bounds of the board
              move_type is one of the allowed move type
              player_turn is a valid player or None

    """
    assert coord_within_bounds(location)
    assert move_type in LEGAL_MOVES 
    assert player_turn in PLAYER or player_turn is None

    move_is_made = False

    if not player_turn is None:
      self.turn = player_turn

    if self.board[location] == 0:
      move_is_made = False
    elif find_player(self.board[location]) != self.turn:
      move_is_made = False
    elif move_type in ROTATION_MOVES:
      coord_piece = self.board[location]
      player = find_player(coord_piece)
      piece = find_piece(coord_piece)
      orient = find_orient(coord_piece)
      orient = (orient + move_type) % num_orientations(piece)
      self.board[location] = make_piece(player, piece, orient)
      move_is_made = True
    elif move_type in MOVE_MOVES:
      new_location = tuple_add(location, move_type)
      new_y, new_x = new_location
      
      if find_piece(self.board[location]) == LASER:
        move_is_made = False
      elif not coord_within_bounds(new_location):
        move_is_made = False
      elif player_turn == FIRST and \
           ((new_x == 0) or new_location in {(0, COLUMNS - 2), \
                                             (ROWS - 1, COLUMNS - 2)}):
        move_is_made = False
      elif player_turn == SECOND and \
           (COLUMNS - 1 == new_x or new_location in {(0, 1), (ROWS - 1, 1)}):   
        move_is_made = False
      elif self.board[new_location] == 0:
        move_is_made = True
        self.board[location], self.board[new_location] = \
          self.board[new_location], self.board[location]
      elif find_piece(self.board[location]) == SWITCH \
          and find_piece(self.board[new_location]) in {DEFLECTOR, DEFENDER}:
        move_is_made = True
        self.board[location], self.board[new_location] = \
          self.board[new_location], self.board[location]
      else:
        move_is_made = False
            
    return move_is_made

  def _shoot_laser_path_piece(self, player_turn = None, capture = True):
    """
    The player in player_turn shoots the laser. This returns the path of the
    laser taken, as well as the piece eliminated.

    requires: player_turn is FIRST or SECOND, or None (self.turn is used)
    """
    assert player_turn in PLAYER or player_turn is None

    if not player_turn is None:
      self.turn = player_turn

    destroyed_piece = None
    laser_path = []
    
    # If winner is determined, nothing happens.
    if self.winner != 0: # or self.movemade == False:
      return (destroyed_piece, laser_path)

    piece_captured = False

    if self.turn == SECOND:
      laser_coord = (0, 0)
      if LASER_HORT == find_orient(self.board[laser_coord]):
        laser_dir = E
      else:
        laser_dir = S
    else: # self.turn == FIRST
      laser_coord = (ROWS - 1, COLUMNS - 1)
      if LASER_HORT == find_orient(self.board[laser_coord]):
        laser_dir = W
      else:
        laser_dir = N
    
    while coord_within_bounds(laser_coord):
      laser_path.append(laser_coord)
      coord_piece = self.board[laser_coord]

      if find_piece(coord_piece) == DEFLECTOR:
        if find_orient(coord_piece) == FLEC_NE:
          if laser_dir == W:
            laser_dir = N
          elif laser_dir == S:
            laser_dir = E
          else:
            piece_captured = True
            break
        elif find_orient(coord_piece) == FLEC_NW:
          if laser_dir == E:
            laser_dir = N
          elif laser_dir == S:
            laser_dir = W
          else:
            piece_captured = True
            break
        elif find_orient(coord_piece) == FLEC_SW:
          if laser_dir == E:
            laser_dir = S
          elif laser_dir == N:
            laser_dir = W
          else:
            piece_captured = True
            break
        elif find_orient(coord_piece) == FLEC_SE:
          if laser_dir == N:
            laser_dir = E
          elif laser_dir == W:
            laser_dir = S
          else:
            piece_captured = True
            break
        else:
          assert False, "invalid orientation"
      elif find_piece(coord_piece) == SWITCH:
        if find_orient(coord_piece) == SWITCH_NESW:
          if laser_dir == N:
            laser_dir = W
          elif laser_dir == E:
            laser_dir = S
          elif laser_dir == S:
            laser_dir = E
          elif laser_dir == W:
            laser_dir = N
        elif find_orient(coord_piece) == SWITCH_NWSE:
          if laser_dir == N:
            laser_dir = E
          elif laser_dir == E:
            laser_dir = N
          elif laser_dir == S:
            laser_dir = W
          elif laser_dir == W:
            laser_dir = S
        else:
          assert False, "invalid orientation"
      elif find_piece(coord_piece) == DEFENDER:
        if find_orient(coord_piece) == FEND_E:
          if laser_dir != W:
            piece_captured = True
        elif find_orient(coord_piece) == FEND_N:
          if laser_dir != S:
            piece_captured = True
        elif find_orient(coord_piece) == FEND_W:
          if laser_dir != E:
            piece_captured = True
        elif find_orient(coord_piece) == FEND_S:
          if laser_dir != N:
            piece_captured = True
        else:
          assert False, "invalid orientation"
        break
      elif find_piece(coord_piece) == KING:
        king_owner = find_player(coord_piece)
        
        # winner is the opponent of the owner's shot king
        if capture == True:
          self.winner = -king_owner
        piece_captured = True
        break
      elif find_piece(coord_piece) in {LASER, 0}:
        assert True
      else:
        assert False, "invalid piece"
      laser_coord = tuple_add(laser_coord, laser_dir)

    if capture and piece_captured:
      destroyed_piece = self.board[laser_coord]
      self.board[laser_coord] = 0

    self.turn = -self.turn  # change turns
    return (destroyed_piece, laser_path)
                               
  def shoot_laser(self, player_turn = None) -> Union[int, None]:
    """
    Before a player ends their turn, they shoot their laser
    and the laser's path depends entirely on which direction
    the laser shoots and how the mirrors are set up.

    If winner is determined, nothing happens.

    If player_turn is not specified, then player_turn defaults to self.turn

    Returns the piece eliminated, or None otherwise.
    """
    destroyed_piece = self._shoot_laser_path_piece(player_turn, capture=True)[0]
    return destroyed_piece

  def shoot_laser_path(self, player_turn = None, capture = True) \
      -> Sequence[Tuple[int, int]]:
    """
    After the player shoots the laser, the laser takes its own path.
    Returns a list of points.
    """
    laser_path = self._shoot_laser_path_piece(player_turn, capture)[1]
    return laser_path

  def move_then_laser(self, location: Tuple[int, int], \
                      move_type: Union[Tuple[int, int], int], \
                      player_turn = None) -> Tuple[bool, int]:
    """
    A player makes a move and then shoots the laser, in one go.
    Returns a tuple telling whether the move is valid or not,
    and if so, return the piece eliminated.

    This function is less cumbersome than make_move and shoot_laser
    separately, but if you want to use it separately, go ahead.

    requires: location is within the board and move_type is a valid mode 
    """
    if not player_turn is None:
      self.turn = player_turn
    
    valid_move = self.make_move(location, move_type, self.turn)
    if True == valid_move:
      piece_eliminated = self.shoot_laser(self.turn)
      # self.turn = -self.turn
    else:
      piece_eliminated = None
    if (not piece_eliminated is None) and find_piece(piece_eliminated) == KING: 
      self.winner = -find_player(piece_eliminated) # other player wins
    return (valid_move, piece_eliminated)

  def __str__(self) -> str:
    """
    Returns the string representing the board as a bunch of geometric shapes.
    """
    col_num_index = [str(n) for n in range(COLUMNS)]
    col_num = '  ' + ' '.join(col_num_index)
    whole_board = col_num + '\n'

    for i in range(ROWS):
      row_shape = [str(i) + ' ']
      for j in range(COLUMNS):
        row_shape.append(INT_TO_PRETTY[self.board[i, j]])
        row_shape.append(" ")
      row_shapes = ''.join(row_shape)
      whole_board = whole_board + row_shapes
      if i != ROWS - 1:
        whole_board = whole_board + '\n'
    return whole_board

  """
  def __repr__(self) -> str:
    
    Returns the official string representation of the board.
    
    player_str = ""
    if self.turn == FIRST:
      player_str = "FIRST"
    elif self.turn == SECOND:
      player_str = "SECOND"
    else:
      raise Exception("self.turn isn't FIRST or SECOND")

    return laser_repr
  """
