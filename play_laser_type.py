from laser_chess import *

"""This is the Laser Chess game. You play by typing in the coordinates
of your pieces and the direction to move the pieces on the console.

NOTE TO SELF: Best be played on Repl.it than locally on the computer.
"""

def main():
  board = LaserChess()
  print(board)

  while board.winner == 0:

    if board.turn == FIRST:
      print("First player's turn")
    else:
      print("Second player's turn")

    # print(board.piece_locations(board.turn))

    # This takes the coordinates as a two integer tuple.
    str_locate = input("Coordinates: ")
    piece_location = eval(str_locate)

    # This takes the moves. It can only be one of ...
    str_move = input("Move: ")
    if str_move in {'N', 'E', 'W', 'S', 'NE', 'NW', 'SW', 'SE', 'CW', 'CCW', 'ACW'}:
      move = eval(str_move)
    else:
      print("Not a valid move. Try again")
      continue

    # We then determine whether or not the input is valid or not
    # (look above and below.)
    if not coord_within_bounds(piece_location):
      print("Not a valid move. Try again.")
      continue

    # It then tests whether the move is valid or not
    # and what pieces are eliminated from the board.
    # Turn change is automatic by move_then_laser.
    valid_move, piece_gone = board.move_then_laser(piece_location, move)

    if valid_move == False:
      print("Not a valid move. Try again.")
    else:
      print("Piece eliminated: " + INT_TO_PRETTY[piece_gone])
      
    print(board)
    board.print_winner()

if __name__ == "__main__":
    main()
