import numpy as np

# The board's dimensions
ROWS = 8
COLUMNS = 10

# Player type
FIRST = 1
SECOND = -1

PLAYER = {FIRST, SECOND}

# //////////////////////////////////////////////////////////////////////

# Each player has 
KING = 50 # 1 of each
DEFENDER = 40 # 2 of each, FEND for short
SWITCH = 30 # 2 of each
DEFLECTOR = 20 # 7 of them, FLEC for short
LASER = 10 # one each at the corners of the board

PIECE_TYPES = {KING, DEFENDER, SWITCH, DEFLECTOR, LASER}

# Orientation types
KING_ORIENT = 0
FEND_E, FEND_N, FEND_W, FEND_S = 0, 1, 2, 3
SWITCH_NESW, SWITCH_NWSE = 0, 1 # Reflection orientation
FLEC_NE, FLEC_NW, FLEC_SW, FLEC_SE = 0, 1, 2, 3
LASER_HORT, LASER_VERT = 0, 1

# //////////////////////////////////////////////////////////////////////

# Each player chooses their piece on the board and do one of the moves
# on the piece.

# "Move" action types
N = (-1, 0)
NE = (-1, 1)
E = (0, 1)
SE = (1, 1)
S = (1, 0)
SW = (1, -1)
W = (0, -1)
NW = (-1, -1)

MOVE_MOVES = {N, NE, E, SE, S, SW, W, NW}

# "Rotation" action types
CW = -1 # clockwise
CCW = 1 # "counterclockwise" but typos could occur and it could cause bugs
ACW = CCW # "anticlockwise". 

ROTATION_MOVES = {CW, ACW}

LEGAL_MOVES = MOVE_MOVES.union(ROTATION_MOVES)

# //////////////////////////////////////////////////////////////////////

"""
How to read the integers.
The sign tells us the player. + is FIRST, - is SECOND
The first digit tells us the piece type. You can look at lines 11 to 29 in 
the module.
The second digit tells us about the pieces's orientation.
"""

# Piece integers, in its full glory
KING_1, KING_2 = 50, -50

FEND_E1, FEND_N1, FEND_W1, FEND_S1 = 40, 41, 42, 43
FEND_E2, FEND_N2, FEND_W2, FEND_S2 = -40, -41, -42, -43

SWITCH_NESW1, SWITCH_NWSE1 = 30, 31
SWITCH_NESW2, SWITCH_NWSE2 = -30, -31

FLEC_NE1, FLEC_NW1, FLEC_SW1, FLEC_SE1 = 20, 21, 22, 23
FLEC_NE2, FLEC_NW2, FLEC_SW2, FLEC_SE2 = -20, -21, -22, -23

LASER_H1, LASER_V1 = 10, 11
LASER_H2, LASER_V2 = -10, -11

# //////////////////////////////////////////////////////////////////////

# Unicode characters for pretty printing
EMPTY = '⋅'  # chr(0x22C5)  

# KINGS
KING_CHR_1 = '□'  # chr(9633) 
KING_CHR_2 = '■'  # chr(9632) 

# LASERS with their orientations, using arrows
LASER_CHR_H1, LASER_CHR_V1 = '←', '↑'  # chr(0x2190), chr(0x2191)
LASER_CHR_H2, LASER_CHR_V2 = '→', '↓'  # chr(0x2192), chr(0x2193)

# DEFLECTORS
FLEC_CHR_NE1, FLEC_CHR_NW1, FLEC_CHR_SW1, FLEC_CHR_SE1 = '◺', '◿', '◹', '◸'  # chr(9722), chr(9727), chr(9721), chr(9720)
FLEC_CHR_NE2, FLEC_CHR_NW2, FLEC_CHR_SW2, FLEC_CHR_SE2 = '◣', '◢', '◥', '◤'  # chr(9699), chr(9698), chr(9701), chr(9700)

# SWITCHES
# They are arrows pointing to the direction of the player who owns the switch
SWITCH_CHR_NWSE1, SWITCH_CHR_NESW1 = '↙', '↘'  # chr(0x2199), chr(0x2198) 
SWITCH_CHR_NWSE2, SWITCH_CHR_NESW2 = '↗', '↖'  # chr(0x2197), chr(0x2196)

# DEFENDERS are triangles, and the flat part is the laser blocking part
FEND_CHR_E1, FEND_CHR_N1, FEND_CHR_W1, FEND_CHR_S1 = '◁', '▽', '▷', '△'  # chr(0x25c1), chr(0x25bd), chr(0x25b7), chr(0x25b3)
FEND_CHR_E2, FEND_CHR_N2, FEND_CHR_W2, FEND_CHR_S2 = '◀', '▼', '▶', '▲'   # chr(0x25c0), chr(0x25bc), chr(0x25b6), chr(0x25b2)

# //////////////////////////////////////////////////////////////////////

# Recommended Laser Chess board setups.

ACE = [[-11, 0,   0,  0, -43, -50, -43, -23, 0,  0],
       [  0, 0, -22,  0,   0,   0,   0,   0, 0,  0],
       [  0, 0,   0, 21,   0,   0,   0,   0, 0,  0],
       [-20, 0,  22,  0, -30, -31,   0, -23, 0, 21],
       [-23, 0,  21,  0,  31,  30,   0, -20, 0, 22],
       [  0, 0,   0,  0,   0,   0, -23,   0, 0,  0],
       [  0, 0,   0,  0,   0,   0,   0,  20, 0,  0],
       [  0, 0,  21, 41,  50,  41,   0,   0, 0, 11]]
ACE = np.array(ACE)

CURIOSITY = [[-11,  0,   0,  0, -43, -50, -43, -31,   0,  0],
             [  0,  0,   0,  0,   0,   0,   0,   0,   0,  0],
             [  0,  0,   0, 21,   0,   0, -20,   0,   0,  0],
             [-20, 22,   0,  0,  23, -31,   0,   0, -23, 21],
             [-23, 21,   0,  0,  31, -21,   0,   0, -20, 22],
             [  0,  0,   0, 22,   0,   0, -23,   0,   0,  0],
             [  0,  0,   0,  0,   0,   0,   0,   0,   0,  0],
             [  0,  0,  31, 41,  50,  41,   0,   0,   0, 11]]
CURIOSITY = np.array(CURIOSITY)

GRAIL = [[-11,   0,   0,   0, -22, -43, -23,   0,   0,   0],
         [  0,   0,   0,   0,   0, -50,   0,   0,   0,   0],
         [-20,   0,   0,   0, -22, -43, -31,   0,   0,   0],
         [-23,   0, -30,   0,  21,   0,  23,   0,   0,   0],
         [  0,   0,   0, -21,   0, -23,   0,  30,   0,  21],
         [  0,   0,   0,  31,  41,  20,   0,   0,   0,  22],
         [  0,   0,   0,   0,  50,   0,   0,   0,   0,   0],
         [  0,   0,   0,  21,  41,  20,   0,   0,   0,  11]]
GRAIL = np.array(GRAIL)

MERCURY = [[-11,   0,   0,   0, -22, -50, -23,   0,   0,  31],
           [  0,   0,   0,   0,   0, -43, -23,   0,   0,   0],
           [-23,   0,   0, -31,   0, -43,   0,   0,   0,   0],
           [-20,   0,   0,   0,  21,   0,   0,   0,  22,   0],
           [  0, -20,   0,   0,   0, -23,   0,   0,   0,  22],
           [  0,   0,   0,   0,  41,   0,  31,   0,   0,  21],
           [  0,   0,   0,  21,  41,   0,   0,   0,   0,   0],
           [-31,   0,   0,  21,  50,  20,   0,   0,   0,  11]]
MERCURY = np.array(MERCURY)

SOPHIE = [[-11,   0,   0,   0, -50,  21, -23,   0,   0,   0],
          [  0,   0,   0, -43,   0, -40,   0,   0,   0,  22],
          [-20,   0,   0,   0, -22, -23,   0,  31,   0,  21],
          [  0,   0,   0,   0,   0,   0,   0, -30,   0,   0],
          [  0,   0,  30,   0,   0,   0,   0,   0,   0,   0],
          [-23,   0, -31,   0,  21,  20,   0,   0,   0,  22],
          [-20,   0,   0,   0,  42,   0,  41,   0,   0,   0],
          [  0,   0,   0,  21, -23,  50,   0,   0,   0,  11]]
SOPHIE = np.array(SOPHIE)

# //////////////////////////////////////////////////////////////////////

# This is a dictionary converting the numerical piece representation
# to a Unicode character, looking like the piece.

INT_TO_PRETTY = {0: EMPTY,
                 KING_1: KING_CHR_1,
                 KING_2: KING_CHR_2,
                 FEND_E1: FEND_CHR_E1,
                 FEND_N1: FEND_CHR_N1,
                 FEND_W1: FEND_CHR_W1,
                 FEND_S1: FEND_CHR_S1,
                 FEND_E2: FEND_CHR_E2,
                 FEND_N2: FEND_CHR_N2,
                 FEND_W2: FEND_CHR_W2,
                 FEND_S2: FEND_CHR_S2,
                 SWITCH_NESW1: SWITCH_CHR_NESW1,
                 SWITCH_NWSE1: SWITCH_CHR_NWSE1,
                 SWITCH_NESW2: SWITCH_CHR_NESW2,
                 SWITCH_NWSE2: SWITCH_CHR_NWSE2,
                 FLEC_NE1: FLEC_CHR_NE1,
                 FLEC_NW1: FLEC_CHR_NW1,
                 FLEC_SW1: FLEC_CHR_SW1,
                 FLEC_SE1: FLEC_CHR_SE1,
                 FLEC_NE2: FLEC_CHR_NE2,
                 FLEC_NW2: FLEC_CHR_NW2,
                 FLEC_SW2: FLEC_CHR_SW2,
                 FLEC_SE2: FLEC_CHR_SE2,
                 LASER_H1: LASER_CHR_H1,
                 LASER_V1: LASER_CHR_V1,
                 LASER_H2: LASER_CHR_H2,
                 LASER_V2: LASER_CHR_V2,
                 None: 'None'}
