import pygame

run=True

pygame.init()
pygame.font.init()

WIN_WIDTH = 300
WIN_HEIGHT = 300
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = pygame.color.Color('0x505050')

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * size[0]
        self.rect.y = pos[1] * size[1]
        self.pos = pos
        self.color = (100, 100, 100)
        self.is_wall = False
        #cost to step onto the tile
        self.cost = 1

    def update(self):
        if(self.is_wall):
            self.color = (0,0,0)
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 1)

tile_lst = []
tile_group = pygame.sprite.Group()
for x in range(0, 15):
    lst = []
    for y in range(0, 15):
        tile = Tile((x, y), (20, 20))
        lst.append(tile)
        tile_group.add(tile)
    tile_lst.append(lst)

path_lst=[]
start_tile = None
end_tile = None
path_complete = True
path_delay=0

wall_lst = [
    (8,0),
    (8,1),
    (8,2),
    (8,3),
    (8,4),
    (8,5),
    (8,6),
    (8,7),
    (7,7),
    (6,7),
    (5,7),
    (4,7),
    (3,7),
    (2,7),
    (2,6),
    (2,5),
    (2,4),
]

for wall in wall_lst:
    tile_lst[wall[0]][wall[1]].is_wall = True
    tile_lst[wall[0]][wall[1]].color = (0,0,0)


water_lst = [
    ((4, 10), 2),
    ((4, 11), 2),
    ((4, 12), 2),
    ((4, 13), 2),
    ((4, 14), 2),
    ((3, 10), 2),
    ((3, 11), 2),
    ((3, 12), 2),
    ((3, 13), 2),
    ((3, 10), 2),
    ((2, 11), 2),
    ((2, 12), 2),
    ((2, 13), 2),
    ((2, 14), 2),
]
for water in water_lst:
    water_coords = water[0]
    tile_lst[water_coords[0]][water_coords[1]].cost = water[1]
    tile_lst[water_coords[0]][water_coords[1]].color = (10, 10, 100)

def get_next_tile2(current_pos, end_pos, path_lst):
    print(current_pos)
    distance_x = end_pos[0] - current_pos[0]
    distance_y = end_pos[1] - current_pos[1]
    next_x = current_pos[0]
    next_y = current_pos[1]

    if (distance_x > 0):
        next_x += 1
    elif (distance_x < 0):
        next_x -= 1
    if (distance_y > 0):
        next_y += 1
    elif (distance_y < 0):
        next_y -= 1
    if (not tile_lst[next_x][next_y].is_wall):
        next_pos = (next_x, next_y)
    else:
        next_pos = current_pos
    return next_pos

def get_next_tile1(current_pos, end_pos, path_lst):
    print(current_pos)
    distance_x = end_pos[0] - current_pos[0]
    distance_y = end_pos[1] - current_pos[1]
    next_x = current_pos[0]
    next_y = current_pos[1]

    if (distance_x > 0):
        next_x += 1
    elif (distance_x < 0):
        next_x -= 1
    if (distance_y > 0):
        next_y += 1
    elif (distance_y < 0):
        next_y -= 1
    if(not tile_lst[next_x][next_y].is_wall):
        next_pos = (next_x, next_y)
    else:
        next_pos = current_pos
    return next_pos

def get_adj_tiles(pos):
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]
    adj_tiles = []
    for move in moves:
        tile = (pos[0] + move[0], pos[1] + move[1])
        if(0 <= tile[0] < len(tile_lst) and 0 <= tile[1] < len(tile_lst[0]) and not tile_lst[tile[0]][tile[1]].is_wall):
            adj_tiles.append(tile)
    return adj_tiles

def dijkstra(start_pos, end_pos):
    # stores distance of tiles from start pos
    distance = {tile.pos: float('inf') for row in tile_lst for tile in row}
    # sets start pos distance to 0
    distance[start_pos] = 0
    # a queue of tiles that haven't or are being explored
    queue = [start_pos]
    # tiles that have been explored
    visited = []
    # stores tiles so they can be used to find shortest path.
    came_from = {start_pos: None}
    loop_count = 0
    while queue:
        loop_count += 1
        if loop_count >= 1000:
            print('break')
            break
        # adds the current tile to the queue
        current_tile = queue[0]
        # gets the adj_tiles for the current_tile
        a = get_adj_tiles(current_tile)
        # tiles that have not been visited
        adj_tiles = [tile for tile in a if tile not in visited]
        for tile in adj_tiles:
            # Store the previous tile for backtracking
            came_from.setdefault(tile, current_tile)
            # assigns distance to the current_tile
            t = tile_lst[tile[0]][tile[1]]
            distance[tile] = distance[current_tile] + t.cost
            print(t.cost)
            tile_lst[tile[0]][tile[1]].color = (120,120,0)
        queue += adj_tiles
        visited += adj_tiles
        queue.remove(current_tile)
        visited.append(current_tile)
        if current_tile == end_pos:
            break
    path = []
    current = end_pos
    print(came_from)
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Important!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def dijkstra2(start_pos, end_pos):
    distances = {start_pos: 0}
    queue = [start_pos]
    visited_tiles = [start_pos]
    loop_count = 0

    came_from = {start_pos: None}

    while len(queue)>0:
        # print(queue)
        #failsafe
        loop_count += 1
        if loop_count >= 1000:
            print('break')
            break

        #get list of all adjacent tiles that have not been visited
        current_tile = queue[0]
        a = get_adj_tiles(current_tile)

        for tile in a:
            t = tile_lst[tile[0]][tile[1]]
            new_distance = distances[current_tile] + t.cost
            print(new_distance)
            if(new_distance < distances.get(tile, float('inf'))):
                distances[tile] = new_distance
                came_from[tile] = current_tile
                visited_tiles.append(tile)
                queue.append(tile)
        queue.remove(current_tile)
        # visited_tiles.append(current_tile)

        #end loop if end point is reached
        if current_tile == end_pos:
            break
    path=[]
    current_tile = end_pos
    while current_tile is not None:
        if(current_tile in came_from):
            #print(came_from[current_tile])
            if(current_tile==start_pos):
                break
            else:
                path = [current_tile] + path
                current_tile = came_from[current_tile]
        else:
            print('path error')
            break
    return path

def get_path(start_pos, end_pos, path_lst=[], tile_limit=-1):
    tile_cnt = 0
    print(end_pos)
    if(len(path_lst)==0):
        current_pos = start_pos
    else:
        current_pos = path_lst[-1]

    while current_pos != end_pos:
        '''
        print(current_pos)
        distance_x = end_pos[0] - current_pos[0]
        distance_y = end_pos[1] - current_pos[1]
        next_x = current_pos[0]
        next_y = current_pos[1]

        if (distance_x > 0):
            next_x+=1
        elif (distance_x < 0):
            next_x-=1
        if (distance_y > 0):
            next_y+=1
        elif (distance_y < 0):
            next_y-=1

        next_pos = (next_x, next_y)
        '''
        #find next tile
        next_pos = get_next_tile2(current_pos, end_pos, path_lst)
        #add next tile to path lst
        path_lst.append(next_pos)
        #increase tiles found this frame
        tile_cnt+=1
        #end the current search if tile limit per frame is hit
        if(len(path_lst)>100 or current_pos==next_pos):
            path_lst.append(end_pos)
            print('break')
            break
        if (tile_limit > 0 and tile_cnt >= tile_limit):
            break
        #update current tile
        current_pos = next_pos
    return path_lst

while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked_tile = tile_lst[pygame.mouse.get_pos()[0] // 20][pygame.mouse.get_pos()[1] // 20]
            if (clicked_tile.is_wall != True and path_complete==True):
                if event.button == 1:
                    if start_tile is not None:
                        start_tile.color = (100, 100, 100)
                    clicked_tile.color = (255, 100, 100)
                    start_tile = clicked_tile
                if event.button == 3:
                    if end_tile is not None:
                        end_tile.color = (100, 100, 100)
                    clicked_tile.color = (100, 100, 255)
                    end_tile = clicked_tile
            if start_tile is not None and end_tile is not None and path_complete==True:
                path_complete = False
                # for tile in path_lst:
                #     tile_lst[tile[0]][tile[1]].color = (100,100,100)
                path_lst = []

    if(path_complete==False and path_delay<=0):
        #path_lst = get_path(start_tile.pos, end_tile.pos,path_lst,-1)
        path_lst = dijkstra2(start_tile.pos, end_tile.pos)
        if(path_lst[-1]==end_tile.pos):
            path_complete = True
        #get_path(first_dir, second_dir, start_tile.pos, end_tile.pos)

        end_tile.color = (100, 100, 255)
        path_delay=5
    path_delay-=1

    tile_group.update()

    #_____Draw_____
    window.fill(BG_COLOR)

    tile_group.draw(window)
    for tile in path_lst:
        t = tile_lst[tile[0]][tile[1]]
        r = (t.pos[0] * t.rect.width, t.pos[1] * t.rect.height, t.rect.width, t.rect.height)
        if(tile==end_tile.pos):
            pygame.draw.rect(window, (100, 100, 255), r)
        else:
            pygame.draw.rect(window, (150, 150, 150), r)
        # tile_lst[tile[0]][tile[1]].color = (150, 150, 150)


    pygame.display.flip()
    clock.tick(FPS)
