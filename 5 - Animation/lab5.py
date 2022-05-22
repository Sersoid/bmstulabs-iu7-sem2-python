import arcade
from math import sqrt

# Window settings
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 576
SCREEN_TITLE = "Lab 5 - Animation"

# Movement vectors
PERSON_MOVEMENT_VECTOR = [
    (176, 288),
    (176, 400),
    (208, 432),
    (208, 464),
    (240, 464),
    (240, 528),
    (368, 528),
    (368, 496),
    (400, 496),
    (400, 464),
    (528, 464),
    (528, 368),
    (432, 368),
    (432, 240),
    (464, 208),
    (464, 144),
    (368, 144),
    (368, 112),
    (306, 112),
    (306, 80),
    (208, 80),
    (208, 48),
    (144, 48),
    (144, 144),
    (80, 144),
    (80, 208),
    (176, 208)
]
ENEMY_MOVEMENT_VECTOR = [
    (304, 432),
    (400, 432),
    (400, 400),
    (432, 400),
    (432, 240),
    (464, 208),
    (464, 144),
    (528, 144),
    (528, 48),
    (432, 48),
    (528, 48),
    (528, 144),
    (464, 144),
    (464, 208),
    (432, 240),
    (432, 272),
    (336, 272),
    (272, 208),
    (272, 176),
    (240, 176),
    (240, 144),
    (176, 144),
    (176, 208),
    (48, 208),
    (48, 272),
    (112, 272),
    (48, 272),
    (48, 208),
    (176, 208),
    (176, 272),
    (208, 272),
    (304, 368)
]

# Movement speed
MOVEMENT_SPEED = 2


# Entity class
class Entity:
    def __init__(self, width, height, color):
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0

        self.width = width
        self.height = height
        self.color = color

    def update(self):
        self.center_x += self.change_x
        self.change_x = 0
        self.center_y += self.change_y
        self.change_y = 0

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)


# Main class
class Main(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        # Scene
        self.tile_map = None
        self.scene = None

        # Person properties
        self.person = None
        self.person_to = 0

        # Enemy properties
        self.enemy = None
        self.enemy_to = 0

        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        self.generate_sprites()

    def generate_sprites(self):
        # Map initialization
        self.tile_map = arcade.load_tilemap("map.tmx", 1)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.wall_list = self.scene.get_sprite_list("Стены")
        self.floor_list = self.scene.get_sprite_list("Пол")

        # "Person" initialization
        self.person = Entity(16, 16, arcade.color.YELLOW)
        self.person.center_x = 272
        self.person.center_y = 288

        # "Enemy" initialization
        self.enemy = Entity(16, 16, arcade.color.RED)
        self.enemy.center_x = 304
        self.enemy.center_y = 288

    # Render
    def on_draw(self):
        self.floor_list.draw()
        self.wall_list.draw()
        self.person.draw()
        self.enemy.draw()

    # Update
    def on_update(self, delta):
        def get_deltas(to_values, from_values):
            return to_values[0] - from_values[0], to_values[1] - from_values[1]

        def get_distance(x, y):
            return sqrt(x ** 2 + y ** 2)

        # Person movement
        delta_x, delta_y = get_deltas((PERSON_MOVEMENT_VECTOR[self.person_to][0],
                                       (PERSON_MOVEMENT_VECTOR[self.person_to][1])),
                                      (self.person.center_x, self.person.center_y))
        if get_distance(delta_x, delta_y) <= MOVEMENT_SPEED:
            self.person.change_x = delta_x
            self.person.change_y = delta_y
            self.person_to = (self.person_to + 1) % len(PERSON_MOVEMENT_VECTOR)
        else:
            k = sqrt(MOVEMENT_SPEED / (delta_x ** 2 + delta_y ** 2))
            self.person.change_x = delta_x * k
            self.person.change_y = delta_y * k

        # Enemy movement
        delta_x, delta_y = get_deltas((ENEMY_MOVEMENT_VECTOR[self.enemy_to][0],
                                       (ENEMY_MOVEMENT_VECTOR[self.enemy_to][1])),
                                      (self.enemy.center_x, self.enemy.center_y))
        if get_distance(delta_x, delta_y) <= MOVEMENT_SPEED:
            self.enemy.change_x = delta_x
            self.enemy.change_y = delta_y
            self.enemy_to = (self.enemy_to + 1) % len(ENEMY_MOVEMENT_VECTOR)
        else:
            k = sqrt(MOVEMENT_SPEED / (delta_x ** 2 + delta_y ** 2))
            self.enemy.change_x = delta_x * k
            self.enemy.change_y = delta_y * k

        self.person.update()
        self.enemy.update()


# Start point
if __name__ == "__main__":
    Main(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
