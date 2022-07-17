from copy import deepcopy

from src.globals import VEC, Direc

intvec = lambda v: VEC(int(v.x), int(v.y))
inttup = lambda t: (int(t[0]), int(t[1]))
sign   = lambda n: (n > 0) - (n < 0)

def rotate_dice(current: dict[Direc, dict[str, int]], direction: Direc):
    orig = deepcopy(current) # just ".copy()" won't copy nested dicts, thus deepcopy
    new = deepcopy(orig)
    if direction == Direc.UP:
        # the faces that needs to change positions, in an order so that every face needs to be moved to the face after it
        faces_to_rotate = [Direc.TOP, Direc.UP, Direc.BOTTOM, Direc.DOWN]
        new[Direc.RIGHT]["rot"] += 90 # Rotate the right 90 degrees CW
        if new[Direc.RIGHT]["rot"] == 360: # If the angle becomes 360 change it to 0
            new[Direc.RIGHT]["rot"] = 0
        new[Direc.LEFT]["rot"] -= 90 # Rotate the left CCW
        if new[Direc.LEFT]["rot"] == -90: # If the angle becomes -90 change it to 270
            new[Direc.LEFT]["rot"] = 270
    elif direction == Direc.DOWN:
        faces_to_rotate = [Direc.DOWN, Direc.BOTTOM, Direc.UP, Direc.TOP]
        new[Direc.LEFT]["rot"] += 90
        if new[Direc.LEFT]["rot"] == 360:
            new[Direc.LEFT]["rot"] = 0
        new[Direc.RIGHT]["rot"] -= 90
        if new[Direc.RIGHT]["rot"] == -90:
            new[Direc.RIGHT]["rot"] = 270
    elif direction == Direc.LEFT:
        faces_to_rotate = [Direc.TOP, Direc.LEFT, Direc.BOTTOM, Direc.RIGHT]
        new[Direc.UP]["rot"] += 90
        if new[Direc.UP]["rot"] == 360:
            new[Direc.UP]["rot"] = 0
        new[Direc.DOWN]["rot"] -= 90
        if new[Direc.DOWN]["rot"] == -90:
            new[Direc.DOWN]["rot"] = 270
    elif direction == Direc.RIGHT:
        faces_to_rotate = [Direc.RIGHT, Direc.BOTTOM, Direc.LEFT, Direc.TOP]
        new[Direc.DOWN]["rot"] += 90
        if new[Direc.DOWN]["rot"] == 360:
            new[Direc.DOWN]["rot"] = 0
        new[Direc.UP]["rot"] -= 90
        if new[Direc.UP]["rot"] == -90:
            new[Direc.UP]["rot"] = 270
    for i, face in enumerate(faces_to_rotate): # For every face in the faces that need to change positions
        # Set the face to the number of on the face in front it, at index 0 it becomes -1 thus looping back to the end of the list
        # which is why every face needs to be moved to the face after it instead of before, so that -1 index can be utilized python pog
        new[face] = orig[faces_to_rotate[i - 1]].copy()
    return new