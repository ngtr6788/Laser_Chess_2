from laser_chess import *
from laser_chess_consts import *
import pytest
import unittest

def board_with_corner_kings():
  """
  This creates a board with two lasers and two kings on the board
  and returns the LaserChess object "encapsulating" the board.
  """
  board_setup = make_empty_board()
  board_setup[1, 1] = KING_2
  board_setup[6, 8] = KING_1
  test_board = LaserChess(board_setup)
  return test_board

"""This tests the methods in LaserChess, as well as the functions.

The helper functions are already tested in Repl.it's 
Unit Test thing, but I copied it over here."""

class TestHelperFuncs(unittest.TestCase):
  def test_make_piece(self):
    self.assertEqual(make_piece(FIRST, DEFENDER, FEND_S), FEND_S1)
    self.assertEqual(make_piece(FIRST, LASER, LASER_HORT), LASER_H1)
    self.assertEqual(make_piece(SECOND, DEFLECTOR, FLEC_NW), FLEC_NW2)
    self.assertEqual(make_piece(SECOND, SWITCH, SWITCH_NWSE), SWITCH_NWSE2)
    self.assertEqual(make_piece(SECOND, KING, KING_ORIENT), KING_2)
  
  def test_find_player(self):
    self.assertEqual(find_player(SWITCH_NWSE2), SECOND)
    self.assertEqual(find_player(LASER_V1), FIRST)
    self.assertEqual(find_player(FEND_S2), SECOND)
    self.assertEqual(find_player(KING_1), FIRST)

  def test_find_piece(self):
    self.assertEqual(find_piece(FLEC_NW1), DEFLECTOR)
    self.assertEqual(find_piece(SWITCH_NWSE2), SWITCH)
    self.assertEqual(find_piece(LASER_V1), LASER)

  def test_find_orient(self):
    self.assertEqual(find_orient(KING_2), KING_ORIENT)
    self.assertEqual(find_orient(FEND_W1), FEND_W)
    self.assertEqual(find_orient(SWITCH_NESW2), SWITCH_NESW)

  def test_tuple_add(self):
    self.assertEqual(tuple_add((1, 5, 4), (2, 4, 7)), (3, 9, 11))
    self.assertEqual(tuple_add((-4, -3, -5, -9, -2), (9, 8, 2, 1, 3)), (5, 5, -3, -8, 1))
    self.assertEqual(tuple_add((1, ), (2, )), (3, ))
    self.assertEqual(tuple_add(N, E), NE)
    self.assertEqual(tuple_add(W, S), SW)
    self.assertEqual(tuple_add(N, S), (0, 0))

  def test_coord_within_bounds(self):
    self.assertTrue(coord_within_bounds((0, 0)))
    self.assertTrue(coord_within_bounds((2, 4)))
    self.assertFalse(coord_within_bounds((0, 10)))
    self.assertFalse(coord_within_bounds((5, 11)))
    self.assertFalse(coord_within_bounds((8, 3)))
    self.assertFalse(coord_within_bounds((11, 15)))



board_setup1 = make_empty_board()
board_setup1[1, 1] = KING_1
board_setup1[6, 8] = KING_2
board_setup1[0, 7] = FEND_E1
board_setup1[7, 2] = FEND_W2
board_setup1[2, 1] = SWITCH_NWSE1
board_setup1[3, 8] = SWITCH_NWSE2
board_setup1[5, 0] = FLEC_NW2
board_setup1[1, 9] = FLEC_SE1
board_setup1[3, 7] = SWITCH_NESW2
test_board1 = LaserChess(board_setup1)

# test_board1.pretty_print()

class TestIllegalMoves():
  # Empty square
  def test_empty_square(self):
    assert test_board1.make_move((2, 5), N, SECOND) == False
    assert test_board1.make_move((3, 2), E, FIRST) == False

  # Moving the laser
  def test_moving_laser(self):
    assert test_board1.make_move((0, 0), E, SECOND) == False
    assert test_board1.make_move((0, 0), S, SECOND) == False
    assert test_board1.make_move((0, 0), SE, SECOND) == False
    
    assert test_board1.make_move((7, 9), W, FIRST) == False
    assert test_board1.make_move((7, 9), N, FIRST) == False
    assert test_board1.make_move((7, 9), NW, FIRST) == False

  # Forbidden squares in the corner there.
  def test_forbidden_corner(self):
    assert test_board1.make_move((6, 8), S, FIRST) == False
    assert test_board1.make_move((1, 1), N, SECOND) == False
    assert test_board1.make_move((7, 2), W, SECOND) == False
    assert test_board1.make_move((0, 7), E, FIRST) == False

  # Forbidden squares on the edges.
  def test_forbidden_edge(self):
    assert test_board1.make_move((2, 1), SW, FIRST) == False
    assert test_board1.make_move((2, 1), W, FIRST) == False
    assert test_board1.make_move((2, 1), NW, FIRST) == False

    assert test_board1.make_move((3, 9), NE, SECOND) == False
    assert test_board1.make_move((3, 9), E, SECOND) == False
    assert test_board1.make_move((3, 9), SE, SECOND) == False

  # Going over the edge
  def test_edge(self):
    assert test_board1.make_move((7, 2), S, SECOND) == False
    assert test_board1.make_move((7, 2), SW, SECOND) == False
    assert test_board1.make_move((7, 2), SE, SECOND) == False

    assert test_board1.make_move((0, 7), N, FIRST) == False
    assert test_board1.make_move((0, 7), NW, FIRST) == False
    assert test_board1.make_move((0, 7), NE, FIRST) == False

    assert test_board1.make_move((5, 0), W, SECOND) == False
    assert test_board1.make_move((5, 0), SW, SECOND) == False
    assert test_board1.make_move((5, 0), NW, SECOND) == False

    assert test_board1.make_move((1, 9), E, FIRST) == False
    assert test_board1.make_move((1, 9), NE, FIRST) == False
    assert test_board1.make_move((1, 9), SE, FIRST) == False

  def test_forbidden_switch(self):
    # Switch can't switch with kings
    assert test_board1.make_move((2, 1), N, FIRST) == False
    # Switch can't swtich with other switches
    assert test_board1.make_move((3, 7), E, SECOND) == False
    assert test_board1.make_move((3, 8), W, SECOND) == False

  # Can't touch other player's pieces
  def test_other_player(self):
    assert not test_board1.make_move((5, 0), E, FIRST)
    assert not test_board1.make_move((1, 1), SE, SECOND)

  # Can't switch pieces on the forbidden squares on the edge.
  def test_forbidden_edge_switch(self):
    test_board = board_with_corner_kings()
    
    test_board.board[4, 8] = SWITCH_NESW2
    test_board.board[3, 9] = FLEC_NE1
    test_board.board[4, 9] = FEND_W1
    test_board.board[5, 9] = FLEC_SW1

    test_board.board[4, 1] = SWITCH_NWSE1
    test_board.board[3, 0] = FLEC_NW2
    test_board.board[4, 0] = FEND_E2
    test_board.board[5, 0] = FLEC_SE2

    for second_move in (NE, E, SE):
      assert not test_board.make_move((4, 8), second_move, SECOND)

    for first_move in (SW, W, NW):
      assert not test_board.make_move((4, 1), first_move, FIRST)

"""The following tests test allowed moves."""
board_setup2 = make_empty_board()
board_setup2[1, 1] = KING_2
board_setup2[6, 8] = KING_1
board_setup2[3, 2] = SWITCH_NESW1
board_setup2[4, 3] = FLEC_SE1
board_setup2[2, 6] = SWITCH_NWSE2
board_setup2[3, 6] = FEND_N2
test_board2 = LaserChess(board_setup2)
# print(test_board)

# move to an empty space
class TestLegalMoves():
  def test_move_to_empty(self):
    assert test_board2.make_move((1, 1), SE, SECOND)
    assert test_board2.make_move((6, 8), NW, FIRST)

  # switch special move, baby.
  def test_allowed_switch(self):
    assert test_board2.make_move((3, 2), SE, FIRST)
    assert test_board2.make_move((2, 6), S, SECOND)

  # rotations are always legal
  def test_rotation_moves(self):
    assert test_board2.make_move((2, 6), CCW, SECOND)
    assert test_board2.make_move((3, 2), CW, FIRST)

  # more move to an empty space
  def test_more_move(self):
    assert test_board2.make_move((2, 6), N, SECOND)
    assert test_board2.make_move((3, 2), S, FIRST)
    assert test_board2.make_move((3, 6), E, SECOND)
    assert test_board2.make_move((4, 3), SW, FIRST)



"""This tests the capabilities of the Laser."""

class TestLaserHitsDefenders():
  def test_south_laser_and_defenders(self):
    test_board = board_with_corner_kings()
    
    test_board.board[2, 0] = FEND_S1
    test_board.board[3, 0] = FEND_W1
    test_board.board[4, 0] = FEND_E1
    test_board.board[5, 0] = FEND_N1

    print(test_board)
    for piece_gone in (FEND_S1, FEND_W1, FEND_E1):
      assert test_board.shoot_laser(SECOND) == piece_gone

    """
    assert test_board.shoot_laser(SECOND) == FEND_S1    
    assert test_board.shoot_laser(SECOND) == FEND_W1
    assert test_board.shoot_laser(SECOND) == FEND_E1
    """
    assert test_board.shoot_laser(SECOND) is None

  def test_east_laser_and_defenders(self):
    test_board = board_with_corner_kings()
    test_board.make_move((0, 0), CCW, SECOND)

    test_board.board[0, 2] = FEND_E1
    test_board.board[0, 3] = FEND_N1
    test_board.board[0, 4] = FEND_S1
    test_board.board[0, 5] = FEND_W1

    print(test_board)

    assert test_board.shoot_laser(SECOND) == FEND_E1
    assert test_board.shoot_laser(SECOND) == FEND_N1
    assert test_board.shoot_laser(SECOND) == FEND_S1
    assert test_board.shoot_laser(SECOND) is None

  def test_north_laser_and_defenders(self):
    test_board = board_with_corner_kings()
    
    test_board.board[2, 9] = FEND_S1
    test_board.board[3, 9] = FEND_W1
    test_board.board[4, 9] = FEND_E1
    test_board.board[5, 9] = FEND_N1

    print(test_board)
    assert test_board.shoot_laser(FIRST) == FEND_N1
    assert test_board.shoot_laser(FIRST) == FEND_E1
    assert test_board.shoot_laser(FIRST) == FEND_W1
    assert test_board.shoot_laser(FIRST) is None

  def test_west_laser_and_defenders(self):
    test_board = board_with_corner_kings()
    test_board.make_move((7, 9), CCW, FIRST)

    test_board.board[7, 8] = FEND_W1
    test_board.board[7, 7] = FEND_N1
    test_board.board[7, 6] = FEND_S1
    test_board.board[7, 5] = FEND_E1

    print(test_board)

    assert test_board.shoot_laser(FIRST) == FEND_W1
    assert test_board.shoot_laser(FIRST) == FEND_N1
    assert test_board.shoot_laser(FIRST) == FEND_S1
    assert test_board.shoot_laser(FIRST) is None

class TestLaserHitsDeflectors():
  def test_north_laser_hits_deflectors(self):
    test_board = board_with_corner_kings()

    test_board.board[4, 9] = FLEC_NE2
    test_board.board[3, 9] = FLEC_NW1
    test_board.board[2, 9] = FLEC_SW1
    test_board.board[2, 4] = FLEC_SE2
    test_board.board[4, 4] = FEND_S2

    print(test_board)

    assert test_board.shoot_laser(FIRST) == FLEC_NE2
    assert test_board.shoot_laser(FIRST) == FLEC_NW1
    assert test_board.shoot_laser(FIRST) == FEND_S2

  def test_south_laser_hits_deflectors(self):
    test_board = board_with_corner_kings()

    test_board.board[3, 0] = FLEC_SW1
    test_board.board[4, 0] = FLEC_SE2
    test_board.board[5, 0] = FLEC_NE2
    test_board.board[5, 5] = FLEC_NW2
    test_board.board[3, 5] = FEND_W1

    print(test_board)

    assert test_board.shoot_laser(SECOND) == FLEC_SW1
    assert test_board.shoot_laser(SECOND) == FLEC_SE2
    assert test_board.shoot_laser(SECOND) == FEND_W1
  
  def test_east_laser_hits_deflectors(self):
    test_board = board_with_corner_kings()

    test_board.make_move((0, 0), CCW, SECOND)

    test_board.board[0, 3] = FLEC_SE1
    test_board.board[0, 4] = FLEC_NE2
    test_board.board[0, 5] = FLEC_SW2
    test_board.board[5, 5] = FLEC_NW1
    test_board.board[5, 4] = FEND_S1

    print(test_board)

    assert test_board.shoot_laser(SECOND) == FLEC_SE1
    assert test_board.shoot_laser(SECOND) == FLEC_NE2
    assert test_board.shoot_laser(SECOND) == FEND_S1

  def test_west_laer_hits_deflectors(self):
    test_board = board_with_corner_kings()

    test_board.make_move((7, 9), CCW, FIRST)

    test_board.board[7, 6] = FLEC_NW2
    test_board.board[7, 4] = FLEC_SW1
    test_board.board[7, 2] = FLEC_NE1
    test_board.board[2, 2] = FLEC_SE2
    test_board.board[2, 6] = FEND_N2

    print(test_board)

    assert test_board.shoot_laser(FIRST) == FLEC_NW2
    assert test_board.shoot_laser(FIRST) == FLEC_SW1
    assert test_board.shoot_laser(FIRST) == FEND_N2

class TestLaserHitsSwitches():
  def test_nesw_switch(self):
    test_board = board_with_corner_kings()
    test_board.board[4, 0] = SWITCH_NESW2
    test_board.board[4, 3] = SWITCH_NESW1
    test_board.board[6, 3] = SWITCH_NWSE2
    test_board.board[6, 0] = SWITCH_NESW2
    test_board.board[5, 0] = FEND_N1

    print(test_board)

    assert test_board.shoot_laser(SECOND) == FEND_N1
  
  def test_nwse_switch(self):
    test_board = board_with_corner_kings()
    test_board.make_move((7, 9), CCW, FIRST)
    test_board.board[7, 4] = FLEC_NE1
    test_board.board[5, 4] = SWITCH_NWSE1
    test_board.board[5, 7] = SWITCH_NWSE2
    test_board.board[3, 7] = SWITCH_NESW1
    test_board.board[3, 4] = SWITCH_NWSE2
    test_board.board[4, 4] = FEND_S2

    print(test_board)

    assert test_board.shoot_laser(FIRST) == FEND_S2  

class TestLaserMisc():
  def test_straight_laser(self):
    test_board = board_with_corner_kings()
    test_board.board[0, 9] = FEND_N2
    test_board.board[7, 0] = FEND_S1
    print(test_board)
    assert test_board.shoot_laser(FIRST) == FEND_N2
    assert test_board.shoot_laser(SECOND) == FEND_S1

  def test_flec_reflect_hit(self):
    test_board = board_with_corner_kings()
    test_board.board[3, 8] = FLEC_SW1
    test_board.board[3, 1] = FLEC_SW2
    test_board.make_move((3, 8), E, FIRST)
    print(test_board)
    assert test_board.shoot_laser(FIRST) == FLEC_SW2
  
  def test_hit_defender_face(self):
    test_board = board_with_corner_kings()
    test_board.board[7, 4] = FEND_E1
    test_board.make_move((7, 9), CW, FIRST)
    print(test_board)
    assert test_board.shoot_laser(FIRST) is None

  def test_hit_defender_side(self):
    test_board = board_with_corner_kings()
    test_board.board[0, 3] = FEND_S2
    test_board.make_move((0, 0), CCW, SECOND)
    print(test_board)
    assert test_board.shoot_laser(SECOND) == FEND_S2

  def test_switch_reflect(self):
    test_board = board_with_corner_kings()
    test_board.board[2, 9] = SWITCH_NESW1
    test_board.board[2, 2] = SWITCH_NWSE2
    print(test_board)
    assert test_board.shoot_laser(FIRST) is None

  def test_laser_hit_laser(self):
    test_board = board_with_corner_kings()
    test_board.board[5, 9] = FLEC_SW1
    test_board.board[5, 0] = FLEC_NE2
    print(test_board)
    assert test_board.shoot_laser(SECOND) is None
    assert test_board.shoot_laser(FIRST) is None

  def test_laser_goes_offboard(self):
    test_board = board_with_corner_kings()
    test_board.board[0, 2] = SWITCH_NWSE2
    assert test_board.shoot_laser(SECOND) is None
    test_board.board[6, 9] = SWITCH_NWSE1
    assert test_board.shoot_laser(FIRST) is None
    print(test_board)

  def test_zigzagly_laser_and_hit_king(self):
    test_board = board_with_corner_kings()

    test_board.board[1, 9] = SWITCH_NESW1
    test_board.board[1, 2] = FLEC_SE2
    test_board.board[6, 2] = FLEC_NE1
    test_board.board[6, 5] = FLEC_NW1
    test_board.board[2, 5] = SWITCH_NWSE2
    test_board.board[2, 7] = SWITCH_NESW2
    test_board.board[4, 7] = FLEC_NW1
    test_board.board[4, 4] = FLEC_NE2
    test_board.board[3, 4] = FLEC_SW1
    test_board.board[3, 0] = FLEC_SE2
    test_board.board[5, 0] = FLEC_NE2
    test_board.board[5, 1] = FLEC_NW1
    print(test_board)
    assert test_board.shoot_laser(FIRST) == KING_2

def main():
    pytest.main()

if __name__ == "__main__":
    main()
