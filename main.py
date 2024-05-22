import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mouse Cheese Collector"
CHARACTER_SCALING = 0.3
TILE_SCALING = 0.5
CHEESE_SCALING = 1
CAT_SCALING = 0.5
BOSS_SCALING = 1
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
ENEMY_MOVEMENT_SPEED = 1

LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3
LEVEL_4 = 4
LEVEL_5 = 5

MENU = 0
STORY = 1
GAME_RUNNING = 2
GAME_OVER = 3
GAME_WON = 4


class MouseGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AUROMETALSAURUS)

        self.game_state = MENU

        self.idle_texture = arcade.load_texture("img/mouse0.png")
        self.walk_textures = [
            arcade.load_texture("img/mouse1.png"),
            arcade.load_texture("img/mouse2.png")
        ]

        self.cat_idle_texture = arcade.load_texture("img/cat0.png")
        self.cat_walk_textures = [
            arcade.load_texture("img/cat0.png"),
            arcade.load_texture("img/cat1.png")
        ]

        self.boss_jump_texture = arcade.load_texture("img/boss_jump.png")
        self.boss_idle_texture = arcade.load_texture("img/boss_idle.png")

        self.wall_list = None
        self.player_list = None
        self.cheese_list = None
        self.enemy_list = None
        self.boss_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.current_level = LEVEL_1

        self.story_screen = arcade.load_texture("img/story.png")
        self.win_screen = arcade.load_texture("img/win.png")
        self.game_over_screen = arcade.load_texture("img/lose.png")

        self.play_button = arcade.load_texture("img/play.png")
        self.exit_button = arcade.load_texture("img/exit.png")

    def setup_level(self, level):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.cheese_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()

        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.player_sprite.stand_right_textures = [self.idle_texture]
        self.player_sprite.walk_right_textures = self.walk_textures
        self.player_sprite.stand_left_textures = [arcade.load_texture("img/mouse0.png", flipped_horizontally=True)]
        self.player_sprite.walk_left_textures = [arcade.load_texture("img/mouse1.png", flipped_horizontally=True),
                                                 arcade.load_texture("img/mouse2.png", flipped_horizontally=True)]
        self.player_sprite.texture = self.idle_texture
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        if level == LEVEL_1:
            for x in range(0, SCREEN_WIDTH, 64):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 32
                self.wall_list.append(wall)
            for x in range(128, SCREEN_WIDTH, 256):
                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 80
                self.cheese_list.append(cheese)

        elif level == LEVEL_2:
            for x in range(64, SCREEN_WIDTH, 150):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 32
                self.wall_list.append(wall)
            for x in range(64, SCREEN_WIDTH, 150):
                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 80
                self.cheese_list.append(cheese)
            for x in range(128, SCREEN_WIDTH, 512):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 200
                self.wall_list.append(wall)

                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 248
                self.cheese_list.append(cheese)

                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x + 256
                wall.center_y = 300
                self.wall_list.append(wall)
            cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
            cheese.center_x = 384
            cheese.center_y = 348
            self.cheese_list.append(cheese)

        elif level == LEVEL_3:
            for x in range(0, SCREEN_WIDTH, 64):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 32
                self.wall_list.append(wall)
            for x in range(128, SCREEN_WIDTH, 256):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 200
                self.wall_list.append(wall)

                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 248
                self.cheese_list.append(cheese)
            for x in range(128, SCREEN_WIDTH, 256):
                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 80
                self.cheese_list.append(cheese)

            for x in range(250, SCREEN_WIDTH, 300):
                cat = arcade.AnimatedWalkingSprite()
                cat.stand_right_textures = [self.cat_idle_texture]
                cat.walk_right_textures = self.cat_walk_textures
                cat.stand_left_textures = [arcade.load_texture("img/cat0.png", flipped_horizontally=True)]
                cat.walk_left_textures = [arcade.load_texture("img/cat0.png", flipped_horizontally=True),
                                          arcade.load_texture("img/cat1.png", flipped_horizontally=True)]
                cat.texture = self.cat_idle_texture
                cat.center_x = x
                cat.center_y = 110
                cat.boundary_left = cat.center_x - 100
                cat.boundary_right = cat.center_x + 100
                cat.change_x = ENEMY_MOVEMENT_SPEED
                self.enemy_list.append(cat)

        elif level == LEVEL_4:
            for x in range(64, SCREEN_WIDTH, 150):
                for y in range(100, SCREEN_HEIGHT, 350):
                    wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

                    cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                    cheese.center_x = x
                    cheese.center_y = y + 50
                    self.cheese_list.append(cheese)
            for x in range(128, SCREEN_WIDTH, 150):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 280
                self.wall_list.append(wall)

                cheese = arcade.Sprite("img/cheese.png", CHEESE_SCALING)
                cheese.center_x = x
                cheese.center_y = 330
                self.cheese_list.append(cheese)

        elif level == LEVEL_5:
            for x in range(0, SCREEN_WIDTH, 64):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 32
                self.wall_list.append(wall)
            boss = arcade.Sprite("img/boss_idle.png", BOSS_SCALING)
            boss.center_x = 330
            boss.center_y = 158
            boss.change_y = 0
            boss.jumping = False
            self.boss_list.append(boss)
            cheese = arcade.Sprite("img/cheese.png", 4)
            cheese.center_x = 700
            cheese.center_y = 295
            self.cheese_list.append(cheese)
            for x in range(600, SCREEN_WIDTH, 64):
                wall = arcade.Sprite("img/platform.png", TILE_SCALING)
                wall.center_x = x
                wall.center_y = 200
                self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def setup(self):
        self.current_level = LEVEL_1
        self.setup_level(self.current_level)

    def on_draw(self):
        arcade.start_render()

        if self.game_state == MENU:
            arcade.draw_text("Mouse Cheese Collector", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 100, 100, self.play_button)
            arcade.draw_text("Play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, 100, 100, self.exit_button)
            arcade.draw_text("Exit", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 210,
                             arcade.color.WHITE, font_size=20, anchor_x="center")

        elif self.game_state == STORY:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.story_screen)

        elif self.game_state == GAME_RUNNING:
            self.wall_list.draw()
            self.player_list.draw()
            self.cheese_list.draw()
            self.enemy_list.draw()
            self.boss_list.draw()

            cheese_count = len(self.cheese_list)
            if cheese_count > 0:
                output = f"Cheese remaining: {cheese_count}"
            else:
                output = "Exit open!"
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        elif self.game_state == GAME_OVER:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over_screen)
            arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 100, 100, self.play_button)
            arcade.draw_text("Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, 100, 100, self.exit_button)
            arcade.draw_text("Exit", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 210,
                             arcade.color.WHITE, font_size=20, anchor_x="center")

        elif self.game_state == GAME_WON:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.win_screen)
            arcade.draw_text("You Win!", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                             arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 100, 100, self.play_button)
            arcade.draw_text("Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, 100, 100, self.exit_button)
            arcade.draw_text("Exit", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 210,
                             arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.game_state == GAME_RUNNING:
            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                self.player_sprite.texture = self.player_sprite.walk_left_textures[0]
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                self.player_sprite.texture = self.player_sprite.walk_right_textures[0]

    def on_key_release(self, key, modifiers):
        if self.game_state == GAME_RUNNING:
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = 0
                self.player_sprite.texture = self.player_sprite.stand_left_textures[0]
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = 0
                self.player_sprite.texture = self.player_sprite.stand_right_textures[0]

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state == MENU:
            if SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50:
                if SCREEN_HEIGHT / 2 - 50 < y < SCREEN_HEIGHT / 2 + 50:
                    self.game_state = STORY
                    arcade.schedule(self.start_game, 1.5)
                elif SCREEN_HEIGHT / 2 - 200 < y < SCREEN_HEIGHT / 2 - 100:
                    arcade.close_window()
        elif self.game_state == GAME_OVER or self.game_state == GAME_WON:
            if SCREEN_WIDTH / 2 - 50 < x < SCREEN_WIDTH / 2 + 50:
                if SCREEN_HEIGHT / 2 - 50 < y < SCREEN_HEIGHT / 2 + 50:
                    self.setup()
                    self.game_state = GAME_RUNNING
                elif SCREEN_HEIGHT / 2 - 200 < y < SCREEN_HEIGHT / 2 - 100:
                    arcade.close_window()

    def start_game(self, delta_time):
        self.game_state = GAME_RUNNING
        arcade.unschedule(self.start_game)
        self.setup_level(self.current_level)

    def on_update(self, delta_time):
        if self.game_state == GAME_RUNNING:
            self.physics_engine.update()

            for enemy in self.enemy_list:
                enemy.center_x += enemy.change_x
                if enemy.left < enemy.boundary_left or enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1
                    enemy.texture = enemy.walk_left_textures[0] if enemy.change_x < 0 else enemy.walk_right_textures[0]
                enemy.update_animation()

            for boss in self.boss_list:
                if not boss.jumping and boss.center_y <= 158:
                    boss.change_y = 30
                    boss.texture = self.boss_jump_texture
                    boss.jumping = True
                elif boss.center_y > 158:
                    boss.change_y -= GRAVITY
                else:
                    boss.change_y = 0
                    boss.texture = self.boss_idle_texture
                    boss.jumping = False

                boss.center_y += boss.change_y

            cheese_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.cheese_list)

            for cheese in cheese_hit_list:
                cheese.remove_from_sprite_lists()

            if self.player_sprite.center_y < 0:
                self.game_state = GAME_OVER

            enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

            for enemy in enemy_hit_list:
                if self.player_sprite.center_y > enemy.center_y + enemy.height * 0.5:
                    enemy.remove_from_sprite_lists()
                else:
                    self.game_state = GAME_OVER

            boss_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.boss_list)

            for boss in boss_hit_list:
                self.game_state = GAME_OVER

            if len(self.cheese_list) == 0:
                if self.current_level == LEVEL_1 and self.player_sprite.right >= SCREEN_WIDTH:
                    self.current_level = LEVEL_2
                    self.setup_level(LEVEL_2)
                elif self.current_level == LEVEL_2 and self.player_sprite.right >= SCREEN_WIDTH:
                    self.current_level = LEVEL_3
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 128
                    self.setup_level(LEVEL_3)
                elif self.current_level == LEVEL_3 and self.player_sprite.right >= SCREEN_WIDTH:
                    self.current_level = LEVEL_4
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 128
                    self.setup_level(LEVEL_4)
                elif self.current_level == LEVEL_4 and self.player_sprite.right >= SCREEN_WIDTH:
                    self.current_level = LEVEL_5
                    self.player_sprite.center_x = 64
                    self.player_sprite.center_y = 128
                    self.setup_level(LEVEL_5)
                elif self.current_level == LEVEL_5:
                    self.game_state = GAME_WON

            if self.player_sprite.change_x != 0:
                self.player_sprite.update_animation()

def main():
    window = MouseGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
