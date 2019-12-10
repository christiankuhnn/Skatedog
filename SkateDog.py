import arcade

# Physics
MOVEMENT_SPEED = 8
JUMP_SPEED = 28
GRAVITY = 1.1

# Map
MAP_WIDTH = 80 * 128
MAP_HEIGHT = 7 * 128
TILE_WIDTH = 128

#Player
RIGHT_FACING = 0
LEFT_FACING = 1

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 896
WINDOW_HALF_WIDTH = WINDOW_WIDTH // 2
UPDATES_PER_FRAME = 3
CHARACTER_SCALING = .5
ENEMY_SCALING = .25

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]
def load_texture_pair_motorcycle(filename):
    return [
        arcade.load_texture(filename, scale=ENEMY_SCALING),
        arcade.load_texture(filename, scale=ENEMY_SCALING, mirrored=True)
    ]

class Menu(arcade.View):

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text("Skate Dog", WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Press space to play", WINDOW_WIDTH/2, WINDOW_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game = SkateDog()
            self.window.show_view(game)

class GameOver(arcade.View):

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text("Skate Dog", WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Press space to play", WINDOW_WIDTH/2, WINDOW_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game = SkateDog()
            self.window.show_view(game)
            SkateDog.setup(self)


class PlayerCharacter(arcade.Sprite):

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Player Data
        self.jumping = False

        # --- Load Textures ---

        main_path = "images/player/dog"
        jump_path = "images/player/jump"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path} (1).gif")

        self.jump_texture_pair = load_texture_pair(f"{jump_path} (0).gif")

        # Load textures for walking
        self.walk_textures = []
        for i in range(5):
            texture = load_texture_pair(f"{main_path} ({i}).gif")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Jumping animation
        if self.center_y > 260:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return

        # Skating animation
        self.cur_texture += 1
        if self.cur_texture > 5 * 2:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

    def takeDamage(self):
        self.lives -= 1

class Motorcycle(arcade.Sprite):

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        # --- Load Textures ---

        main_path = "images/motorcycle/motorcycle"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair_motorcycle(f"{main_path} (0).gif")

        # Load textures for walking
        self.ride_textures = []
        for i in range(4):
            texture = load_texture_pair_motorcycle(f"{main_path} ({i}).gif")
            self.ride_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 5 * 2:
            self.cur_texture = 0
        self.texture = self.ride_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

class Motorcycle2(arcade.Sprite):

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        # --- Load Textures ---

        main_path = "images/motorcycle2/motorcycle"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair_motorcycle(f"{main_path} (0).gif")

        # Load textures for walking
        self.ride_textures = []
        for i in range(4):
            texture = load_texture_pair_motorcycle(f"{main_path} ({i}).gif")
            self.ride_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 5 * 2:
            self.cur_texture = 0
        self.texture = self.ride_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]


class SkateDog(arcade.View):
    def __init__(self):
        super().__init__()
        self.ground_list = None
        self.bones_list = None
        self.player_list = None
        self.enemy_list = None
        self.enemy2_list = None
        self.enemy3_list = None
        self.enemy4_list = None
        self.physics_engine = None
        self.collected_bones = 0
        self.lives = 3
        self.lost = False
        self.takenDamageEnemy1 = False
        self.takenDamageEnemy2 = False
        self.takenDamageEnemy3 = False
        self.takenDamageEnemy4 = False
        self.setup()

    def youLoose(self):
        self.lost = True
        self.gOver = GameOver()
        self.window.show_view(self.gOver)

    def win(self):
        self.gameOver()

    def setup(self):
        my_map = arcade.read_tiled_map("maps/my-map1.tmx", 1)
        self.ground_list = arcade.generate_sprites(my_map, "ground", 1)
        self.bones_list = arcade.generate_sprites(my_map, "bones", 1)
        self.streettop_list = arcade.generate_sprites(my_map, "streettop", 1)
        self.background = arcade.load_texture("images/sky.png")
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy2_list = arcade.SpriteList()
        self.enemy3_list = arcade.SpriteList()
        self.enemy4_list = arcade.SpriteList()
        # Set up player
        self.player = PlayerCharacter()
        self.player.center_x = 300
        self.player.center_y = 500
        self.player.scale = 1
        self.player_list.append(self.player)
        # Set up enemy
        self.enemy = Motorcycle()
        self.enemy.center_x = 3000
        self.enemy.center_y = 260
        self.enemy.scale = .5
        self.enemy_list.append(self.enemy)
        # Set up enemy 2
        self.enemy2 = Motorcycle2()
        self.enemy2.center_x = 5500
        self.enemy2.center_y = 260
        self.enemy2.scale = .5
        self.enemy2_list.append(self.enemy2)
        # Set up enemy 3
        self.enemy3 = Motorcycle()
        self.enemy3.center_x = 7500
        self.enemy3.center_y = 260
        self.enemy3.scale = .5
        self.enemy3_list.append(self.enemy3)
        # Set up enemy 4
        self.enemy4 = Motorcycle2()
        self.enemy4.center_x = 9500
        self.enemy4.center_y = 260
        self.enemy4.scale = .5
        self.enemy4_list.append(self.enemy4)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list, gravity_constant=GRAVITY)
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy, self.ground_list, gravity_constant=GRAVITY)
        self.enemy2_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy2, self.ground_list, gravity_constant=GRAVITY)
        self.enemy3_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy3, self.ground_list, gravity_constant=GRAVITY)
        self.enemy4_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy4, self.ground_list, gravity_constant=GRAVITY)
        self.player.change_x = MOVEMENT_SPEED


    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(MAP_WIDTH // 2, MAP_HEIGHT // 2,
                                      MAP_WIDTH, MAP_HEIGHT, self.background)
        self.ground_list.draw()
        self.streettop_list.draw()
        self.player_list.draw()
        self.bones_list.draw()
        self.enemy_list.draw()
        self.enemy2_list.draw()
        self.enemy3_list.draw()
        self.enemy4_list.draw()
        arcade.draw_text(f"Collected Bones: {self.collected_bones}", arcade.get_viewport()[0] + 10, arcade.get_viewport()[2] + 830, arcade.color.WHITE, font_size=20)
        arcade.draw_text(f"Lives: {self.lives}", arcade.get_viewport()[0] + 10, arcade.get_viewport()[2] + 860, arcade.color.WHITE, font_size=20)

    def clamp(self, value, mini, maxi):
        return max(min(value, maxi), mini)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.enemy_physics_engine.update()
        self.enemy2_physics_engine.update()
        self.enemy3_physics_engine.update()
        self.enemy4_physics_engine.update()
        self.player.center_x = self.clamp(self.player.center_x, 0, MAP_WIDTH)
        self.player_list.update_animation()
        self.enemy_list.update_animation()
        self.enemy2_list.update_animation()
        self.enemy3_list.update_animation()
        self.enemy4_list.update_animation()
        self.enemy.center_x = self.clamp(self.enemy.center_x, 0, MAP_WIDTH)
        self.enemy2.center_x = self.clamp(self.enemy2.center_x, 0, MAP_WIDTH)
        self.enemy3.center_x = self.clamp(self.enemy3.center_x, 0, MAP_WIDTH)
        self.enemy4.center_x = self.clamp(self.enemy4.center_x, 0, MAP_WIDTH)

        # Move enemy's x position
        self.enemy.change_x = -MOVEMENT_SPEED
        self.enemy2.change_x = -MOVEMENT_SPEED
        self.enemy3.change_x = -MOVEMENT_SPEED
        self.enemy4.change_x = -MOVEMENT_SPEED

        # Reset enemy's position
        if self.enemy.center_x < 10:
            self.takenDamageEnemy1 = False
            self.enemy.center_x = 79 * 128
        if self.enemy2.center_x < 10:
            self.takenDamageEnemy2 = False
            self.enemy2.center_x = 79 * 128
        if self.enemy3.center_x < 10:
            self.takenDamageEnemy3 = False
            self.enemy3.center_x = 79 * 128
        if self.enemy4.center_x < 10:
            self.takenDamageEnemy4 = False
            self.enemy4.center_x = 79 * 128

        if self.player.center_x > WINDOW_HALF_WIDTH and self.player.center_x < MAP_WIDTH - TILE_WIDTH - WINDOW_HALF_WIDTH:
            change_view = True
        else:
            change_view = False

        if change_view:
            arcade.set_viewport(self.player.center_x - WINDOW_HALF_WIDTH, self.player.center_x + WINDOW_HALF_WIDTH, 0, WINDOW_HEIGHT)

        # Bone Collision
        bones_hit = arcade.check_for_collision_with_list(self.player, self.bones_list)
        for bone in bones_hit:
            self.collected_bones += 1
            bone.kill()
        # Enemy Collision
        enemy_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in enemy_hit:
            if not self.takenDamageEnemy1:
                self.takenDamageEnemy1 = True
                self.player.change_y = JUMP_SPEED
                PlayerCharacter.takeDamage(self)
        # Enemy 2 Collision
        enemy2_hit = arcade.check_for_collision_with_list(self.player, self.enemy2_list)
        for enemy2 in enemy2_hit:
            if not self.takenDamageEnemy2:
                self.takenDamageEnemy2 = True
                self.player.change_y = JUMP_SPEED
                PlayerCharacter.takeDamage(self)
        # Enemy 3 Collision
        enemy3_hit = arcade.check_for_collision_with_list(self.player, self.enemy3_list)
        for enemy3 in enemy3_hit:
            if not self.takenDamageEnemy3:
                self.takenDamageEnemy3 = True
                self.player.change_y = JUMP_SPEED
                PlayerCharacter.takeDamage(self)
        # Enemy 4 Collision
        enemy4_hit = arcade.check_for_collision_with_list(self.player, self.enemy4_list)
        for enemy4 in enemy4_hit:
            if not self.takenDamageEnemy4:
                self.takenDamageEnemy4 = True
                self.player.change_y = JUMP_SPEED
                PlayerCharacter.takeDamage(self)

        if self.collected_bones == 26:
            self.win()

        if self.lives < 1:
            if not self.lost:
                self.youLoose()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if symbol == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if symbol == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Skate Dog")
    menu = Menu()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()