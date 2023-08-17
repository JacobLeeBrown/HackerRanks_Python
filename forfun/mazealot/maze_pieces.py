# Each piece represents the 4 possible entry points to the center of a 3x3 grid
# The indices map to left, up, right, down, respectively.
# 0 = open, 1 = closed
# So p0110 = [0, 1, 1, 0] corresponds to a 3x3 grid of:
#   1  1  1
#   0  0  1
#   1  0  1
# where the user can enter/exit from the left and bottom

p0000 = [0, 0, 0, 0]
p0001 = [0, 0, 0, 1]
p0010 = [0, 0, 1, 0]
p0011 = [0, 0, 1, 1]
p0100 = [0, 1, 0, 0]
p0101 = [0, 1, 0, 1]
p0110 = [0, 1, 1, 0]
p0111 = [0, 1, 1, 1]
p1000 = [1, 0, 0, 0]
p1001 = [1, 0, 0, 1]
p1010 = [1, 0, 1, 0]
p1011 = [1, 0, 1, 1]
p1100 = [1, 1, 0, 0]
p1101 = [1, 1, 0, 1]
p1110 = [1, 1, 1, 0]
# Can't have p1111, since that would be a segment with no way in... no way out

all_pieces = [p0000, p0001, p0010, p0011, p0100,
              p0101, p0110, p0111, p1000, p1001,
              p1010, p1011, p1100, p1101, p1110]

open_left  = [p0000, p0001, p0010, p0011, p0100, p0101, p0110, p0111]
open_up    = [p0000, p0001, p0010, p0011, p1000, p1001, p1010, p1011]
open_right = [p0000, p0001, p0100, p0101, p1000, p1001, p1100, p1101]
open_down  = [p0000, p0010, p0100, p0110, p1000, p1010, p1100, p1110]
