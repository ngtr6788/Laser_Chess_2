import laser_chess
from laser_chess import LaserChess
from laser_chess_consts import *

import numpy as np
from typing import Tuple, List, Union, Callable
from math import inf
from copy import deepcopy

PIECE_VALUE = 5
KING_VALUE = 15 * PIECE_VALUE
FUTURE_SIGHT = 0.6

# Type alliases:
MoveType = Union[int, Tuple[int, int]]  # MoveType is in LEGAL_MOVES
CoordType = Tuple[int, int]  # CoordType is between (0, 0) and (7, 9) inclusive

def minimax(lzch: LaserChess, depth: int, max_player: int) \
    -> Tuple[float, CoordType, MoveType]:
    """We use the minimax algorithm to find the *hopefully* optimal move given
    the player and the board."""
    move_thought = _minimax_filtered(lzch, depth, max_player, \
                                     allowed_moves = all_legal_moves)
    """
    if (max_player == FIRST and move_thought[0] == -inf) or \
       (max_player == SECOND and move_thought[0] == inf):
        move_thought = _minimax_filtered(lzch, depth, max_player, \
                                         allowed_moves=all_legal_moves)
    """
    return move_thought
        
# allowed_moves = Callable[[LaserChess, int], List[Tuple[CoordType, MoveType]]
def _minimax_filtered(
    lzch: LaserChess, depth: int, max_player: int, \
    allowed_moves, alpha = -inf, beta = inf) -> Tuple[float, CoordType, MoveType]:
    """We use the minimax algorithm to find the *hopefully* optimal move
    with some alpha-beta pruning."""
    
    if lzch.winner != 0 or depth == 0:
        return (evaluate_board(lzch, max_player), None, None)
    
    if max_player == FIRST:
        best_eval = -inf
        compare = lambda x, y: x >= y
        update = lambda a, b, e: (max(a, e), b)
    elif max_player == SECOND:
        best_eval = inf
        compare = lambda x, y: x <= y
        update = lambda a, b, e: (a, min(b, e))

    # Consider ALL legal moves
    moves_considered = allowed_moves(lzch, max_player)

    for coord, move in moves_considered:
        child_lzch = deepcopy(lzch)
        legal, piece = child_lzch.move_then_laser(coord, move, max_player)
        cur_eval = _minimax_filtered(child_lzch, depth - 1, -max_player, \
                                     allowed_moves, alpha, beta)[0]  # [0] = take eval only
        if compare(cur_eval, best_eval):
            best_eval = cur_eval
            best_coord = coord
            best_move = move
        alpha, beta = update(alpha, beta, cur_eval)
        del child_lzch
        if beta <= alpha:
            break
    return (best_eval, best_coord, best_move)
    
def evaluate_board(lzch: LaserChess, player: int) -> float:
    """Evaluates the heuristic value of the board position, depending on
    the current player. + means it leans to FIRST player, - means it
    leans to SECOND player.

    The heuristic value is determined by whose piece is eliminated and how
    close the laser is to either king."""

    """What's the game plan? The game plan is to measure the board like this:
    1. How many pieces you have compared to your opponent.
    2. # of pieces engaging with the laser (ie number of pieces in the paths
       of both lasers) compared to the other player
    3. How in danger your king is, compared to the opponent's king.
       How do measure that, you ask? Well...
       The PLAN is to find a path taken from the king, bounced from the
       pieces and see how it ends up. The thing is, you have to consider
       "what if a piece is in this location or in this orientation." NOW WHAT?"""

    if lzch.winner != 0:
        return inf * lzch.winner

    # NOTE TO SELF: REWRITE THIS FUNCTION.

    # number of pieces FIRST vs SECOND
    first_counts = count_player_pieces(lzch, FIRST)
    second_counts = count_player_pieces(lzch, SECOND)

    dif_pieces = first_counts - second_counts

    eval_points = PIECE_VALUE * dif_pieces
    
    # the current laser paths of both players
    piece1, path1 = lzch._shoot_laser_path_piece(FIRST, capture=False)
    piece2, path2 = lzch._shoot_laser_path_piece(SECOND, capture=False)

    laser1_end = path1[-1]
    laser2_end = path2[-1]

    laser_squares = set(path1) | set(path2)
    laser_engaged_pieces = 0
    for coord in laser_squares:
        if lzch.board[coord] > 0:
            laser_engaged_pieces += 1
        elif lzch.board[coord] < 0:
            laser_engaged_pieces -= 1

    eval_points += PIECE_VALUE * FUTURE_SIGHT * laser_engaged_pieces

    # Looking for the kings' positions.
    king1_coord = find_king(lzch.board, FIRST)
    king2_coord = find_king(lzch.board, SECOND)

    king_eval1 = eval_laser_in_kings(laser1_end, king1_coord, king2_coord)
    king_eval2 = eval_laser_in_kings(laser2_end, king1_coord, king2_coord)
    
    # This evaluates how in danger your king is.
    if player == FIRST:
        if king1_coord in {laser1_end, laser2_end}:
            eval_points -= KING_VALUE
        elif king2_coord == laser1_end:
            eval_points += KING_VALUE * FUTURE_SIGHT
        else:
            eval_points += king_eval1 + king_eval2
    elif player == SECOND:
        if king2_coord in {laser2_end, laser1_end}:
            eval_points += KING_VALUE
        elif king1_coord == laser2_end:
            eval_points -= KING_VALUE * FUTURE_SIGHT
        else:
            eval_points += king_eval1 + king_eval2

    return eval_points
        

def find_king(board: np.ndarray, player: int) -> Tuple[int, int]:
    """Finds the location of player's king, as a tuple.
       requires: board is 8 x 10
                 player is FIRST or SECOND
                 (not asserting them now.) """
    npx, npy = np.where(board == player * KING)
    x, y = npx[0], npy[0]
    return (x, y)

def count_player_pieces(lzch: LaserChess, player: int) -> int:
    """Counts the number of pieces player has."""
    if player == FIRST:
        return np.count_nonzero(lzch.board > 0)
    elif player == SECOND:
        return np.count_nonzero(lzch.board < 0)
    else:
        raise ValueError("player must be FIRST (1) or SECOND (-1)")

def dist_recip(p1: float, p2: float) -> float:
    p1y, p1x = p1
    p2y, p2x = p2
        
    # "distance reciprical"
    return (1 / ((p1x - p2x) ** 2 + (p1y - p2y) ** 2 + 1))

def eval_laser_in_kings(
    laser_pos: Tuple[int, int], king1_pos: Tuple[int, int], \
    king2_pos: Tuple[int, int]) -> float:
    """Evaluates the heuristic value of the laser being near either king.
    PROBABLY: MAYBE REWRITE THIS TO BETTER REFLECT THE FACT THAT THE LASER
    IS PRETTY UNPREDICTABLE, SO IF IT'S TOO FAR, IT DOESN'T MATTER, BUT WHEN
    IT'S TOO CLOSE, IT REALLY MATTERS."""
    ly, lx = laser_pos
    k1y, k1x = king1_pos
    k2y, k2x = king2_pos

    eval_points = dist_recip(laser_pos, king2_pos) - \
                  dist_recip(laser_pos, king1_pos)

    # eval_points /= ((PIECE_VALUE / 2) / dist_recip(king1_pos, king2_pos) - 1)
    
    return eval_points

def player_locations(lzch: LaserChess, player: int) -> np.ndarray:
    # Find the coordinates of all pieces belonging to player
    if player == FIRST:
        return np.array(np.where(lzch.board > 0)).T
    elif player == SECOND:
        return np.array(np.where(lzch.board < 0)).T
    else:
        raise ValueError("player must be FIRST (1) or SECOND (-1)")

def moves_that_change_laser(lzch: LaserChess, player: int) \
    -> List[Tuple[CoordType, MoveType]]:
    # Returns the moves that move the laser (that player can make)
    laser_change = []

    if lzch.winner != 0:
        return laser_change

    # First, you determine the initial path of the laser. Because
    # you shoot the laser, the piece could be lost, so you must
    # put it back and reset the winner, if need be.
    init_piece1, init_path1 = lzch._shoot_laser_path_piece(FIRST)
    if init_piece1 != None:
        lzch.board[init_path1[-1]] = init_piece1
    if lzch.winner != 0:
       lzch.winner = 0

    init_piece2, init_path2 = lzch._shoot_laser_path_piece(SECOND)
    if init_piece2 != None:
        lzch.board[init_path2[-1]] = init_piece2
    if lzch.winner != 0:
        lzch.winner = 0

    # Find the locations that player owns
    player_locs = player_locations(lzch, player)
    for coord in player_locs:
        coord = tuple(coord)
        for move in LEGAL_MOVES:
            moves_laser = False
            copy_lzch = deepcopy(lzch)
            if copy_lzch.make_move(coord, move, player):
                # If it changes the direction of the laser or
                # affects how the captured piece is captured,
                # it is considered. (That's both directions, btw.)
                final_piece1, final_path1 = copy_lzch._shoot_laser_path_piece(FIRST)
                if final_piece1 != None:
                    copy_lzch.board[final_path1[-1]] = final_piece1
                if lzch.winner != 0:
                    lzch.winner = 0

                if (final_path1 != init_path1) or (final_piece1 != init_piece1):
                    moves_laser = True

                final_piece2, final_path2 = copy_lzch._shoot_laser_path_piece(SECOND)
                if final_piece2 != None:
                    copy_lzch.board[final_path2[-1]] = final_piece2
                if lzch.winner != 0:
                    lzch.winner = 0

                if (final_path2 != init_path2) or (final_piece2 != init_piece2):
                    moves_laser = True

                if moves_laser == True:
                    laser_change.append((coord, move))
            del copy_lzch

    return laser_change

def all_legal_moves(lzch: LaserChess, player: int) \
    -> List[Tuple[CoordType, MoveType]]:
    # Returns the list of all legal moves.
    legal_moves = []
    player_locs = player_locations(lzch, player)
    for coord in player_locs:
        coord = tuple(coord)
        for move in LEGAL_MOVES:
            copy_lzch = deepcopy(lzch)
            if copy_lzch.make_move(coord, move, player):
                legal_moves.append((coord, move))
            del copy_lzch
    return legal_moves

def legal_minus_laser(lzch: LaserChess, player: int):
    # Returns the moves that don't move the laser.
    legal_moves = set(all_legal_moves(lzch, player))
    laser_moved = set(moves_that_change_laser(lzch, player))

    return legal_moves - laser_moved
    
if __name__ == "__main__":
    from time import process_time as ptime
    # yeah this weird. it can't find the obvious move to win for deep levels
    board =  np.array([[-11, 0,   0,  0, -43, -50, -43, -23, 0,  0],
                       [  0, 0, -22,  0,   0,   0,   0,   0, 0,  0],
                       [  0, 0,   0, 21,   0, -30,   0,   0, 0,  0],
                       [-20, 0,  22,  0,  30, -31,   0, -23, 0, 22],
                       [-23, 0,  20,  0,  31,  30,   0, -20, 0,  0],
                       [  0, 0,   0,  0,   0,   0, -23,   0, 0,  0],
                       [  0, 0,   0,  0,   0,   0,   0,  20, 0,  0],
                       [  0, 0,  21, 41,  50,  41,   0,   0, 0, 11]])
    turn = FIRST
    a = LaserChess(ACE)
    start = ptime()
    while a.winner == 0:
        evalu, coord, move = minimax(a, depth=3, max_player=turn)
        print(coord, move)
        a.move_then_laser(coord, move)
        print(a.board)
        turn /= -1
    print(ptime() - start)
