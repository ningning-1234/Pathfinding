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

# todo
#  Make path go diagonally until it can't. Then go strait.
#  Move one tile then check where to move next.

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * size[0]
        self.rect.y = pos[1] * size[1]
        self.pos = pos
        self.color = (100, 100, 100)

    def update(self):
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 1)

def get_path(start_pos, end_pos):
    next_path = start_pos

    distance_x = end_pos[0] - start_pos[0]
    distance_y = end_pos[1] - start_pos[1]

    if(distance_x>0):
        next_path = (start_pos[0] + 1, start_pos[1])
    elif(distance_x<0):
        next_path = (start_pos[0] - 1, start_pos[1])
    else:
        if (distance_y > 0):
            next_path = (start_pos[0] + distance_x, start_pos[1] + 1)
        if (distance_y < 0):
            next_path = (start_pos[0] + distance_x, start_pos[1] - 1)
    return next_path

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
pre_path_lst = []
start_tile = None
end_tile = None
first_dir = None
second_dir = None
while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if start_tile is not None:
                    start_tile.color = (100, 100, 100)
                tile_lst[pygame.mouse.get_pos()[0] // 20][pygame.mouse.get_pos()[1] // 20].color = (255, 100, 100)
                start_tile = tile_lst[pygame.mouse.get_pos()[0] // 20][pygame.mouse.get_pos()[1] // 20]
            if event.button == 3:
                if end_tile is not None:
                    end_tile.color = (100, 100, 100)
                tile_lst[pygame.mouse.get_pos()[0] // 20][pygame.mouse.get_pos()[1] // 20].color = (100, 100, 255)
                end_tile = tile_lst[pygame.mouse.get_pos()[0] // 20][pygame.mouse.get_pos()[1] // 20]
            if start_tile is not None and end_tile is not None:
                for tile in path_lst:
                    print('test')
                    tile_lst[tile[0]][tile[1]].color = (100,100,100)
                    print(tile_lst[tile[0]][tile[1]].color)
                path_lst = []

                next_start = start_tile.pos
                print(start_tile.pos)
                print(end_tile.pos)
                print(path_lst)
                print(len(path_lst))
                print()
                #get_path(first_dir, second_dir, start_tile.pos, end_tile.pos)
                while next_start != end_tile.pos:
                    path = get_path(next_start, end_tile.pos)
                    path_lst.append(path)
                    next_start = path_lst[-1]
                for tile in path_lst:
                    tile_lst[tile[0]][tile[1]].color = (150, 150, 150)

    tile_group.update()

    #_____Draw_____
    window.fill(BG_COLOR)

    tile_group.draw(window)

    pygame.display.flip()
    clock.tick(FPS)
