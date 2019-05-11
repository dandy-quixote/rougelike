
import tcod as libtcod
import math


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
           self.x += dx
           self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

    def move_astar(self, target, entities, game_map):
        #create new fov map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        #scan for the current map each turn and set all the walls
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)
                #scan all the objects to see if there are objects that must be navigated around
                #check also that the object isn't self or the target (so that the start and the end points are free)
                # the ai class handles the situation if self is next to the target so it will not use this a* function anyway
                for entity in entities:
                    if entity.blocks and entity != self and entity != target:
                        #set the tile as a wall so it must be navigated around
                        libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

                        #allocate a a* path
                        #1.41 is the normal diagonal cost of moving, it can be set to 0.0 if diagonal moves are prohibited
                my_path = libtcod.path_new_using_map(fov, 1.41)

                 #compute the path between self's coordinates and the targets coordinates
                libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
                        # check if the path exists, and in this case, also the path is shorter than 25 tiles
                        # the path size matters if you want the monster to use alternate longer paths (for example through other rooms) if for example the player is in a corridor
                        #it makes sense to keep path size relatively low to keep the monsters form running around the map if there's an alternate path really far away
                if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
                     # find the next coordinates in the computed full path
                     x, y = libtcod.path_walk(my_path, True)
                     if x or y:
                         #set self's coordinates to the next path tile
                         self.x = x
                         self.y = y
                else:
                    #keep old move functino as a backup so that if there are no paths (for example another monster blocks a corridor)
                    # it will still try to move towards the player (closer to the corridor opening)
                    self.move_towards(target.x, target.y, game_map, entities)

                    #delete the path to free memory
                libtcod.path_delete(my_path)
                
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
        if not (game_map.is_blocked(self.x  + dx, self.y + dy) or
                get_blcoking_entities_at_location(entities, self.x +dx, self.y + dy)):
            self.move(dx, dy)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
            
    return None
