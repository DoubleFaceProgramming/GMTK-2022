from copy import deepcopy

from src.globals import VEC, DIREC
# from globals import VEC, DIREC

intvec = lambda v: VEC(int(v.x), int(v.y))
inttup = lambda t: (int(t[0]), int(t[1]))
newvec = lambda v: VEC(v.x, v.y)
sign   = lambda n: (n > 0) - (n < 0)

def rotate_dice(current: dict[DIREC, dict[str, int]], direction: DIREC):
    orig = deepcopy(current) # just ".copy()" won't copy nested dicts, thus deepcopy
    new = deepcopy(orig)
    if direction == DIREC.UP:
        # the faces that needs to change positions, in an order so that every face needs to be moved to the face after it
        faces_to_rotate = [DIREC.TOP, DIREC.UP, DIREC.BOTTOM, DIREC.DOWN]
        new[DIREC.RIGHT]["rot"] += 90 # Rotate the right 90 degrees CW
        if new[DIREC.RIGHT]["rot"] == 360: # If the angle becomes 360 change it to 0
            new[DIREC.RIGHT]["rot"] = 0
        new[DIREC.LEFT]["rot"] -= 90 # Rotate the left CCW
        if new[DIREC.LEFT]["rot"] == -90: # If the angle becomes -90 change it to 270
            new[DIREC.LEFT]["rot"] = 270
    elif direction == DIREC.DOWN:
        faces_to_rotate = [DIREC.DOWN, DIREC.BOTTOM, DIREC.UP, DIREC.TOP]
        new[DIREC.LEFT]["rot"] += 90
        if new[DIREC.LEFT]["rot"] == 360:
            new[DIREC.LEFT]["rot"] = 0
        new[DIREC.RIGHT]["rot"] -= 90
        if new[DIREC.RIGHT]["rot"] == -90:
            new[DIREC.RIGHT]["rot"] = 270
    elif direction == DIREC.LEFT:
        faces_to_rotate = [DIREC.TOP, DIREC.LEFT, DIREC.BOTTOM, DIREC.RIGHT]
        new[DIREC.UP]["rot"] += 90
        if new[DIREC.UP]["rot"] == 360:
            new[DIREC.UP]["rot"] = 0
        new[DIREC.DOWN]["rot"] -= 90
        if new[DIREC.DOWN]["rot"] == -90:
            new[DIREC.DOWN]["rot"] = 270
    elif direction == DIREC.RIGHT:
        faces_to_rotate = [DIREC.RIGHT, DIREC.BOTTOM, DIREC.LEFT, DIREC.TOP]
        new[DIREC.DOWN]["rot"] += 90
        if new[DIREC.DOWN]["rot"] == 360:
            new[DIREC.DOWN]["rot"] = 0
        new[DIREC.UP]["rot"] -= 90
        if new[DIREC.UP]["rot"] == -90:
            new[DIREC.UP]["rot"] = 270
    for i, face in enumerate(faces_to_rotate): # For every face in the faces that need to change positions
        # Set the face to the number of on the face in front it, at index 0 it becomes -1 thus looping back to the end of the list
        # which is why every face needs to be moved to the face after it instead of before, so that -1 index can be utilized python pog
        new[face] = orig[faces_to_rotate[i - 1]].copy()
    return new

# Test code
# faces = {
#     DIREC.TOP: {"num": 1, "rot": 0},
#     DIREC.BOTTOM: {"num": 4, "rot": 0},
#     DIREC.UP: {"num": 2, "rot": 0},
#     DIREC.DOWN: {"num": 5, "rot": 0},
#     DIREC.LEFT: {"num": 6, "rot": 0},
#     DIREC.RIGHT: {"num": 3, "rot": 0}
# }
# faces = rotate_dice(faces, DIREC.UP)
# for direction, data in faces.items():
#     print(direction.name, data["num"], data["rot"])