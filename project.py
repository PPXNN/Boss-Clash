import pygame
import time
import tkinter as tk
from tkinter import simpledialog
import random
import sys
import math

pygame.init()

main_background = pygame.image.load("picture/main_background.png")
main_background = pygame.transform.scale(main_background, (1280, 800))

background_in_game = pygame.image.load("picture/background.png")
background_in_game = pygame.transform.scale(background_in_game, (1280, 800))

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Clash")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 40)

icon_dash = pygame.image.load("picture/dash_icon.png")
icon_ability = None
icon_deflect = pygame.image.load("picture/deflect_icon.png")
icon_dash = pygame.transform.scale(icon_dash, (50, 50))
icon_deflect = pygame.transform.scale(icon_deflect, (85, 85))

DASH_COOLDOWN = 5
ABILITY_COOLDOWN = 10

dash_last_used = 0
ability_last_used = 0

class CharacterSelection:
    def __init__(self):
        char_width, char_height = 200, 200
        spacing = 50
        start_x = (WIDTH - ((char_width * 3) + (spacing * 2))) // 2

        char1_img = pygame.image.load("picture/freeze_char.png").convert_alpha()
        char2_img = pygame.image.load("picture/wall_char.png").convert_alpha()
        char3_img = pygame.image.load("picture/invisible_char.png").convert_alpha()

        char1_img = pygame.transform.scale(char1_img, (char_width, char_height))
        char2_img = pygame.transform.scale(char2_img, (char_width, char_height))
        char3_img = pygame.transform.scale(char3_img, (char_width, char_height))

        self.characters = [
            {"color": RED, "rect": pygame.Rect(start_x, 250, char_width, char_height), "image": char1_img, "name": "Cryo"},
            {"color": BLUE, "rect": pygame.Rect(start_x + char_width + spacing, 250, char_width, char_height), "image": char2_img, "name": "Bastille"},
                    {"color": GREEN, "rect": pygame.Rect(start_x + 2 * (char_width + spacing), 250, char_width, char_height), "image": char3_img, "name": "Wraith"}
        ]

        self.selected_character = None
        self.player_name = ""

        button_width, button_height = 200, 50
        self.quit_button = pygame.Rect((WIDTH - button_width) // 2, 650, button_width, button_height)
        self.button_font = pygame.font.Font(None, 36)


    def draw_title(self):
        title_text = font.render("Boss Clash", True, WHITE)
        text_rect = title_text.get_rect(center=(WIDTH // 2, 70))
        screen.blit(title_text, text_rect)

    def draw_quit_button(self):
        pygame.draw.rect(screen, RED, self.quit_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.quit_button, 2, border_radius=10)  # Border

        quit_text = self.button_font.render("Quit Game", True, WHITE)
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_rect)

    def draw_characters(self):
        for index, char in enumerate(self.characters):
            screen.blit(char['image'], char['rect'])

            if self.selected_character == index:
                border_rect = pygame.Rect(char['rect'].x - 5, char['rect'].y - 5,
                                          char['rect'].width + 10, char['rect'].height + 10)
                pygame.draw.rect(screen, (255, 215, 0), border_rect, 5)

            name_text = input_font.render(char['name'], True, WHITE)

            name_x = char["rect"].centerx - name_text.get_width() // 2
            screen.blit(name_text, (name_x, char["rect"].bottom + 10))


    def get_player_name(self):
        self.draw_characters()
        pygame.display.flip()

        root = tk.Tk()
        root.withdraw()
        self.player_name = simpledialog.askstring("Character Name", "Enter your name:")

        if self.player_name:
            return True
        else:
            self.selected_character = None
            return False

    def draw_instructions(self):
        instructions_text = input_font.render("Click to select your character", True, WHITE)
        instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions_text, instructions_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for index, char in enumerate(self.characters):
                        if char["rect"].collidepoint(event.pos):
                            self.selected_character = index
                            if self.get_player_name():
                                return True

                    if self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_character = 0
                    if self.get_player_name():
                        return True
                elif event.key == pygame.K_2:
                    self.selected_character = 1
                    if self.get_player_name():
                        return True
                elif event.key == pygame.K_3:
                    self.selected_character = 2
                    if self.get_player_name():
                        return True
        return False

class Ball:
    def __init__(self, x, y, speed=3):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = speed
        self.active = True
        self.target_x = None
        self.target_y = None
        self.frozen = False
        self.freeze_time = 0
        self.random_target_x = random.randint(0, WIDTH)
        self.random_target_y = random.randint(0, HEIGHT)

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius + 3)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

        if self.frozen:
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius + 3)
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius + 5, 3)

    def move_towards_player(self, player):
        if not self.frozen and self.active and self.target_x is None and self.target_y is None:
            if player.transparent:
                dx = self.random_target_x - self.x
                dy = self.random_target_y - self.y
            else:
                hitbox = player.get_hitbox()
                dx = hitbox.centerx - self.x
                dy = hitbox.centery - self.y

            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

            if player.transparent and random.random() < 0.01:
                self.random_target_x = random.randint(0, WIDTH)
                self.random_target_y = random.randint(0, HEIGHT)

            if player.get_hitbox().colliderect(
                    pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)):
                player.take_damage(20)
                self.active = False

    def move_towards_boss(self, boss_x, boss_y):
        self.target_x = boss_x + 100
        self.target_y = boss_y + 100

    def reset_position(self, boss_x, boss_y):
        self.x = boss_x
        self.y = boss_y
        self.target_x = None
        self.target_y = None
        self.active = True

    def update_position(self):
        if self.target_x is not None and self.target_y is not None:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

            if abs(self.x - self.target_x) < 2 and abs(self.y - self.target_y) < 2:
                self.reset_position(self.target_x, self.target_y)

    def freeze_for_duration(self, duration):
        self.frozen = True
        self.freeze_time = time.time() + duration

    def update(self):
        if self.frozen and time.time() > self.freeze_time:
            self.frozen = False
            self.move_towards_boss(self.x, self.y)

    def reach_boss(self, boss, damage=False):
        if damage:
            boss.hp -= 20
            self.move_towards_boss(boss.x,boss.y)
        else:
            self.reset_position(boss.x + boss.width // 2, boss.y + boss.height // 2)

class Player:
    def __init__(self, x, y, color, name, type = None):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.moving = None
        self.hp = 100
        self.deflect_range = 100

        self.freeze_time = 0
        self.wall = None
        self.transparent = False
        self.invisibility_end_time = 0

        self.boss_type = type
        self.dash_count_fire = 0
        self.dash_count_ice = 0
        self.frozen = False
        self.freeze_end_time = 0
        self.speed_reduction = 1

        self.image_width = 150
        self.image_height = 150
        self.hitbox_width = 50
        self.hitbox_height = 50
        self.hitbox_x = (self.image_width - self.hitbox_width) // 2
        self.hitbox_y = (self.image_height - self.hitbox_height) // 2

        self.boss_defeated = 0

        self.deflect_particles = []

        if color == RED:
            self.image = pygame.image.load("picture/freeze_char_ingame.png").convert_alpha()
        elif color == BLUE:
            self.image = pygame.image.load("picture/wall_char_ingame.png").convert_alpha()
        elif color == GREEN:
            self.image = pygame.image.load("picture/invisible_char_ingame.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))

    def get_hitbox(self):
        return pygame.Rect(self.x + self.hitbox_x, self.y + self.hitbox_y, self.hitbox_width, self.hitbox_height)

    def draw(self):
        player_surface = pygame.Surface((self.image_width, self.image_height), pygame.SRCALPHA)
        player_surface.blit(self.image, (0, 0))

        if self.frozen:
            frozen_overlay = pygame.Surface((self.image_width, self.image_height), pygame.SRCALPHA)
            alpha_mask = pygame.surfarray.array_alpha(self.image)

            for x in range(self.image_width):
                for y in range(self.image_height):
                    if alpha_mask[y][x] > 0:
                        frozen_overlay.set_at((x, y), (0, 150, 255, 150))

            player_surface.blit(frozen_overlay, (0, 0), special_flags=pygame.BLEND_MULT)

        elif self.transparent:
            alpha_surface = pygame.Surface((self.image_width, self.image_height), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, 153))
            player_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(player_surface, (self.x, self.y))

    def take_damage(self, amount):
        self.hp -= amount

    def dash(self):
        global dash_last_used
        if time.time() - dash_last_used >= DASH_COOLDOWN:
            if self.moving == "right":
                self.x += 100
            elif self.moving == "left":
                self.x -= 100
            elif self.moving == "up":
                self.y -= 100
            elif self.moving == "down":
                self.y += 100
            dash_last_used = time.time()
        if self.boss_type == 'fire':
            self.dash_count_fire += 1
        elif self.boss_type == 'ice':
            self.dash_count_ice += 1

    def use_ability(self, ball):
        global ability_last_used
        if time.time() - ability_last_used >= ABILITY_COOLDOWN:
            if self.color == RED:
                ball.freeze_for_duration(3)
            elif self.color == BLUE:
                self.wall = Wall(self.x, self.y - 50)
            elif self.color == GREEN:
                self.transparent = True
                self.invisibility_end_time = time.time() + 3
            ability_last_used = time.time()
            ability_last_used = time.time()

    def deflect(self, ball, boss, boss_x, boss_y):
        if self.frozen or time.time() < self.freeze_end_time + 0.5:  # Small buffer
            return

        player_center_x = self.x + self.hitbox_x + self.hitbox_width // 2
        player_center_y = self.y + self.hitbox_y + self.hitbox_height // 2

        distance = ((player_center_x - ball.x) ** 2 + (player_center_y - ball.y) ** 2) ** 0.5
        if distance <= self.deflect_range:
            for _ in range(15):
                self.deflect_particles.append(DeflectParticle(ball.x, ball.y))
            chance = random.random()

            if chance < 0.4:
                ball.move_towards_boss(boss_x, boss_y)
            else:
                ball.reach_boss(boss, damage=True)

    def update_movement(self, keys):
        if self.frozen:
            return

        move_speed = 5 * self.speed_reduction

        if keys[pygame.K_w] and self.y > 10:
            self.y -= move_speed
            self.moving = 'up'
        if keys[pygame.K_s] and self.y < HEIGHT - 60:
            self.y += move_speed
            self.moving = 'down'
        if keys[pygame.K_a] and self.x > 10:
            self.x -= move_speed
            self.moving = 'left'
        if keys[pygame.K_d] and self.x < WIDTH - 60:
            self.x += move_speed
            self.moving = 'right'

    def update(self):
        if self.frozen and time.time() > self.freeze_end_time:
            self.frozen = False
            self.speed_reduction = 1.0

        if self.transparent and time.time() > self.invisibility_end_time:
            self.transparent = False

        for particle in self.deflect_particles[:]:
            if not particle.update():
                self.deflect_particles.remove(particle)


class DeflectParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 8)
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.lifetime = random.uniform(0.4, 0.8)
        self.birth_time = time.time()

    def update(self):
        # Move particle
        self.x += self.speed_x
        self.y += self.speed_y
        self.size = max(0, self.size - 0.1)
        return time.time() - self.birth_time < self.lifetime

    def draw(self):
        alpha = min(255, int(255 * (1 - (time.time() - self.birth_time) / self.lifetime)))
        deflect = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(deflect, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(deflect, (self.x - self.size, self.y - self.size))

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 10
        self.speed = 3
        self.active = True

    def move(self):
        if self.active:
            self.y -= self.speed

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def check_collision(self, ball):
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
        wall_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if ball_rect.colliderect(wall_rect):
            self.active = False
            return True
        return False

class Boss:
    def __init__(self, x, y, type = None):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.hp = 200

        self.boss_type = type

        self.fireball_cooldown = 5
        self.last_fireball_time = time.time()
        self.fireballs = []
        self.lavas = []
        self.lava_time = None
        self.last_lava_hit = time.time()

        self.snow_patches = []
        self.snow_time = None
        self.snowball_cooldown = 5
        self.last_snow_time = time.time()
        self.snowballs = []

        self.fire_boss_img = pygame.image.load("picture/fire_boss.png").convert_alpha()
        self.fire_boss_img = pygame.transform.scale(self.fire_boss_img, (self.width, self.height))
        self.ice_boss_img = pygame.image.load("picture/ice_boss.png").convert_alpha()
        self.ice_boss_img = pygame.transform.scale(self.ice_boss_img, (self.width, self.height))

    def fireball(self, player):
        if time.time() - self.last_fireball_time >= self.fireball_cooldown:
            for i in range(3):
                fireball = Fireball(self.x + self.width // 2, self.y + self.height // 2, player, speed=random.randint(1, 4))
                fireball.target_x = player.x + 25
                fireball.target_y = player.y + 25
                self.fireballs.append(fireball)

            self.last_fireball_time = time.time()

    def update_fireballs(self, player):
        if self.hp <= 100:
            for fireball in self.fireballs:
                fireball.move_towards_player(player)
                fireball.update(player)
                if fireball.active:
                    fireball.draw()

    def create_lava(self, player):
        if hasattr(self, 'lavas'):
            self.lavas = [lava for lava in self.lavas if lava.active]
        else:
            self.lavas = []

        if len(self.lavas) < 4 and (self.lava_time is None or time.time() - self.lava_time >= 2):
            min_distance_from_player = 200
            min_distance_between = 150
            lava_width, lava_height = 200, 150
            max_attempts = 50
            created = 0

            min_x, max_x = 50, WIDTH - lava_width - 50
            min_y, max_y = HEIGHT // 2 - 18, HEIGHT - lava_height - 50

            while created < 4 and max_attempts > 0:
                max_attempts -= 1
                valid_position = True

                new_x = random.randint(min_x, max_x)
                new_y = random.randint(min_y, max_y)
                new_rect = pygame.Rect(new_x, new_y, lava_width, lava_height)

                player_rect = pygame.Rect(player.x, player.y, 50, 50)
                if new_rect.colliderect(player_rect.inflate(min_distance_from_player, min_distance_from_player)):
                    valid_position = False

                for patch in self.lavas:
                    patch_rect = pygame.Rect(patch.x, patch.y, patch.width, patch.height)
                    if new_rect.colliderect(patch_rect.inflate(min_distance_between, min_distance_between)):
                        valid_position = False
                        break

                if valid_position:
                    self.lavas.append(Lava(new_x, new_y))
                    created += 1

            self.lava_time = time.time()

    def update_lavas(self, player):
        duration = 4
        for lava in self.lavas:
            if self.hp <= 100:
                duration = 2
            if time.time() - self.lava_time >= duration:
                lava.active = False
            else:
                lava.update()
                lava.draw()
                if time.time() - self.last_lava_hit > 1.0:
                    if lava.check_collision(player):
                        player.take_damage(5)
                        self.last_lava_hit = time.time()

    def snowball(self, player):
        if time.time() - self.last_snow_time >= self.snowball_cooldown:
            for i in range(3):
                snowball = Snowball(self.x + self.width // 2, self.y + self.height // 2, player, speed=random.randint(1, 4))
                snowball.target_x = player.x + 25
                snowball.target_y = player.y + 25
                self.snowballs.append(snowball)

            self.last_snow_time = time.time()

    def update_snowballs(self, player):
        if self.hp <= 100:
            for snowball in self.snowballs:
                snowball.move_towards_player(player)
                snowball.update(player)
                if snowball.active:
                    snowball.draw()

    def create_snow(self, player):
        if hasattr(self, 'snow_patches'):
            self.snow_patches = [snow for snow in self.snow_patches if snow.active]
        else:
            self.snow_patches = []

        if len(self.snow_patches) < 4 and (self.snow_time is None or time.time() - self.snow_time >= 2):
            min_distance_from_player = 200
            min_distance_between = 150
            snow_width, snow_height = 200, 150
            max_attempts = 50
            created = 0

            min_x, max_x = 50, WIDTH - snow_width - 50
            min_y, max_y = HEIGHT // 2 - 18, HEIGHT - snow_height - 50

            while created < 4 and max_attempts > 0:
                max_attempts -= 1
                valid_position = True

                new_x = random.randint(min_x, max_x)
                new_y = random.randint(min_y, max_y)
                new_rect = pygame.Rect(new_x, new_y, snow_width, snow_height)

                player_rect = pygame.Rect(player.x, player.y, 50, 50)
                if new_rect.colliderect(player_rect.inflate(min_distance_from_player, min_distance_from_player)):
                    valid_position = False

                for patch in self.snow_patches:
                    patch_rect = pygame.Rect(patch.x, patch.y, patch.width, patch.height)
                    if new_rect.colliderect(patch_rect.inflate(min_distance_between, min_distance_between)):
                        valid_position = False
                        break

                if valid_position:
                    self.snow_patches.append(Snow(new_x, new_y))
                    created += 1

            self.snow_time = time.time()

    def update_snow(self, player):
        duration = 4
        if hasattr(self, 'snow_patches'):
            player.speed_reduction = 1.0
            player_on_snow = False

            for snow in self.snow_patches:
                if time.time() - self.snow_time >= duration:
                    snow.active = False
                else:
                    snow.update()
                    snow.draw()

                    if snow.check_collision(player):
                        player_on_snow = True
                        if (snow.player_on_snow_time is not None and time.time() - snow.player_on_snow_time >= 2):
                            player.frozen = True
                            player.freeze_end_time = time.time() + 2  # Freeze for 2 sec
                            snow.player_on_snow_time = None

            if player_on_snow:
                player.speed_reduction = 0.5

    def draw(self):
        if self.boss_type == "fire":
            screen.blit(self.fire_boss_img, (self.x, self.y))
        elif self.boss_type == "ice":
            screen.blit(self.ice_boss_img, (self.x, self.y))


class Snow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 150
        self.active = True
        self.time_created = time.time()
        self.player_on_snow_time = None
        self.player_was_on_snow = False

    def draw(self):
        if self.active:
            snow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            snow_surface.fill((200, 230, 255, 150))
            screen.blit(snow_surface, (self.x, self.y))

    def check_collision(self, player):
        player_hitbox = player.get_hitbox()
        snow_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        is_on_snow = player_hitbox.colliderect(snow_rect)

        if is_on_snow:
            if not self.player_was_on_snow:
                self.player_on_snow_time = time.time()
            self.player_was_on_snow = True
            player.speed_reduction = 0.5

            if (self.player_on_snow_time is not None and
                    time.time() - self.player_on_snow_time >= 2):
                player.frozen = True
                player.freeze_end_time = time.time() + 2
        else:
            if self.player_was_on_snow:
                player.speed_reduction = 1.0
            self.player_was_on_snow = False
            self.player_on_snow_time = None

        return is_on_snow

    def update(self):
        pass

class Lava:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 150
        self.duration = 4
        self.time_created = time.time()
        self.active = True


    def draw(self):
        if self.active:
            lava_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            lava_surface.fill((255, 69, 0, 150))
            screen.blit(lava_surface, (self.x, self.y))

    def check_collision(self, player):
        player_rect = pygame.Rect(player.x, player.y, 50, 50)
        lava_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if player_rect.colliderect(lava_rect):
            return True
        return False

    def update(self):
        if time.time() - self.time_created > self.duration:
            self.active = False

class Fireball:
    def __init__(self, x, y, player, speed):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = speed
        self.active = True
        self.image = pygame.image.load('picture/fireball.png')
        self.image = pygame.transform.scale(self.image, (30, 30))

        hitbox = player.get_hitbox()
        dx = hitbox.centerx - self.x
        dy = hitbox.centery - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.direction_x = dx / distance
        self.direction_y = dy / distance

    def draw(self):
        screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))

    def move_towards_player(self, player):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

        if player.get_hitbox().colliderect(
                pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)):
            player.take_damage(2)
            self.active = False

    def update(self, player):
        if self.active:
            self.move_towards_player(player)

class Snowball:
    def __init__(self, x, y, player, speed):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = speed
        self.active = True
        self.image = pygame.image.load('picture/snowball.png')
        self.image = pygame.transform.scale(self.image, (30, 30))

        hitbox = player.get_hitbox()
        dx = hitbox.centerx - self.x
        dy = hitbox.centery - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.direction_x = dx / distance
        self.direction_y = dy / distance

    def draw(self):
        screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))

    def move_towards_player(self, player):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

        if player.get_hitbox().colliderect(
                pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)):
            player.take_damage(10)
            self.active = False

    def update(self, player):
        if self.active:
            self.move_towards_player(player)


def draw_bottom_fade():
    fade_height = 150
    fade_surface = pygame.Surface((WIDTH, fade_height), pygame.SRCALPHA)

    for y in range(fade_height):
        alpha = int(150 * (y / fade_height))
        pygame.draw.line(fade_surface, (255, 255, 255, alpha),(0, y), (WIDTH, y))

    screen.blit(fade_surface, (0, HEIGHT - fade_height))


def draw_ui():
    draw_bottom_fade()

    dash_remaining = max(0, DASH_COOLDOWN - (time.time() - dash_last_used))
    ability_remaining = max(0, ABILITY_COOLDOWN - (time.time() - ability_last_used))

    temp_icon = icon_dash.copy()
    temp_icon.set_alpha(100 if dash_remaining > 0 else 255)
    screen.blit(temp_icon, (50, HEIGHT - 120))
    if dash_remaining > 0:
        cooldown_text = pygame.font.Font(None, 30).render(str(int(dash_remaining)), True, BLACK)
        screen.blit(cooldown_text, (70, HEIGHT - 100))
    dash_text = pygame.font.Font(None, 30).render("LShift", True, BLACK)
    screen.blit(dash_text, (40, HEIGHT - 60))

    temp_icon = icon_ability.copy()
    temp_icon.set_alpha(100 if ability_remaining > 0 else 255)
    screen.blit(temp_icon, (120, HEIGHT - 120))
    if ability_remaining > 0:
        cooldown_text = pygame.font.Font(None, 30).render(str(int(ability_remaining)), True, BLACK)
        screen.blit(cooldown_text, (140, HEIGHT - 100))
    ability_text = pygame.font.Font(None, 30).render("Q", True, BLACK)
    screen.blit(ability_text, (140, HEIGHT - 60))

    temp_icon = icon_deflect.copy()
    screen.blit(temp_icon, (170, HEIGHT - 130))
    deflect_text = pygame.font.Font(None, 30).render("E", True, BLACK)
    screen.blit(deflect_text, (208, HEIGHT - 60))

class AnimatedHealthBar:
    def __init__(self, x, y, width, height, max_value, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.current_value = max_value
        self.display_value = max_value
        self.color = color
        self.last_update = time.time()
        self.damage_animation = 0

    def update(self, new_value):
        self.current_value = new_value

        if self.current_value == self.max_value:
            self.display_value = self.max_value
        elif self.current_value == 0:
            self.display_value = 0
        else:
            if abs(self.display_value - self.current_value) > 1:
                self.display_value += (self.current_value - self.display_value) * 0.1

        if self.current_value < self.display_value:
            self.damage_animation = min(1.0, self.damage_animation + 0.1)
        else:
            self.damage_animation = max(0.0, self.damage_animation - 0.05)

    def draw(self):
        pygame.draw.rect(screen, (40, 40, 40), (self.x, self.y, self.width, self.height))

        fill_width = int(self.width * (self.display_value / self.max_value))

        if self.damage_animation > 0:
            flash_width = int(self.width * (self.current_value / self.max_value))
            pygame.draw.rect(screen, (255, 100, 100, int(200 * self.damage_animation)),(self.x, self.y, flash_width, self.height))

        for i in range(fill_width):
            pos_ratio = i / self.width
            r = int(self.color[0] * (0.7 + 0.3 * pos_ratio))
            g = int(self.color[1] * (0.7 + 0.3 * pos_ratio))
            b = int(self.color[2] * (0.7 + 0.3 * pos_ratio))
            pygame.draw.rect(screen, (r, g, b), (self.x + i, self.y, 1, self.height))

        if (self.display_value / self.max_value) < 0.3:
            pulse = abs(math.sin(time.time() * 3))
            border_color = (min(255, 200 + 55 * pulse),max(0, 100 - 100 * pulse),max(0, 100 - 100 * pulse))

            pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3)

        else:
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, self.height), 2)

        percent = int(100 * self.display_value / self.max_value)
        text = font.render(f"{percent}%", True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        shadow = font.render(f"{percent}%", True, (0, 0, 0))
        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text, text_rect)

class GameOverScreen:
    def __init__(self):
        self.button_font = pygame.font.Font(None, 36)
        button_width, button_height = 200, 50

        self.retry_button = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2, button_width, button_height)
        self.menu_button = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 + 70, button_width, button_height)

    def draw(self,player, time):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - 50))

        time_text = input_font.render(f"Time Survived: {self.format_time(time)}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 3 + 20))

        boss_defeat_text = input_font.render(f"Boss Defated: {player.boss_defeated}", True, WHITE)
        screen.blit(boss_defeat_text, (WIDTH // 2 - boss_defeat_text.get_width() // 2, HEIGHT // 3 + 90))

        pygame.draw.rect(screen, GRAY, self.retry_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.retry_button, 2, border_radius=10)

        pygame.draw.rect(screen, BLUE, self.menu_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.menu_button, 2, border_radius=10)

        retry_text = self.button_font.render("Retry", True, WHITE)
        menu_text = self.button_font.render("Main Menu", True, WHITE)

        screen.blit(retry_text, (self.retry_button.centerx - retry_text.get_width() // 2,
                                 self.retry_button.centery - retry_text.get_height() // 2))
        screen.blit(menu_text, (self.menu_button.centerx - menu_text.get_width() // 2,
                                self.menu_button.centery - menu_text.get_height() // 2))

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.retry_button.collidepoint(event.pos):
                        return "retry"
                    elif self.menu_button.collidepoint(event.pos):
                        return "menu"
        return None

class Game:
    def __init__(self):
        self.character_selection = CharacterSelection()
        self.player = None
        self.ball = None

        self.boss_type = ['fire', 'ice']
        self.boss_num = random.randint(0, 1)
        self.boss = Boss(WIDTH // 2 - 50, 10, self.boss_type[self.boss_num])

        self.game_start_time = time.time()
        self.game_time = 0
        self.timer_font = pygame.font.Font(None, 36)

        self.boss.lava_time = self.game_start_time

        self.game_over_screen = GameOverScreen()
        self.boss_defeated = False

        self.boss_health_bar = AnimatedHealthBar(WIDTH // 2 - 250, 30, 500, 30, 200, (200, 50, 50))
        self.player_health_bar = AnimatedHealthBar(40, HEIGHT - 150, 200, 30, 100, (50, 200, 50))

        self.initialize_boss()

    def update_health_bars(self):
        self.boss_health_bar.update(self.boss.hp)
        self.player_health_bar.update(self.player.hp)

    def draw_health_bars(self):
        self.boss_health_bar.draw()
        self.player_health_bar.draw()

    def initialize_boss(self):
        self.boss_num = random.randint(0, 1)
        self.boss = Boss(WIDTH // 2 - 110, 50, self.boss_type[self.boss_num])
        self.boss.lava_time = time.time()
        self.boss_defeated = False

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def draw_timer(self):
        timer_text = self.timer_font.render(f"Time: {self.format_time(self.game_time)}", True, WHITE)
        screen.blit(timer_text, (WIDTH - 350, 60))

    def start_game(self):
        global icon_ability
        player_pos = [WIDTH // 2 - 75, HEIGHT - 200]
        clock = pygame.time.Clock()

        selected_color = [RED, BLUE, GREEN][self.character_selection.selected_character]

        if selected_color == RED:
            icon_ability = pygame.image.load("picture/freeze_ability_icon.png")
        elif selected_color == BLUE:
            icon_ability = pygame.image.load("picture/ability_icon.png")
        elif selected_color == GREEN:
            icon_ability = pygame.image.load("picture/invisible_ability_icon.png")

        icon_ability = pygame.transform.scale(icon_ability, (50, 50))

        self.player = Player(player_pos[0], player_pos[1],
                             self.character_selection.characters[self.character_selection.selected_character]["color"],
                             self.character_selection.player_name, self.boss_type[self.boss_num])

        self.ball = Ball(self.boss.x + self.boss.width // 2, self.boss.y + self.boss.height // 2)

        running = True

        while running:
            screen.blit(background_in_game, (0, 0))

            self.game_time = time.time() - self.game_start_time
            if self.player.hp <= 0:
                self.game_over_screen.draw(self.player ,self.game_time)
                pygame.display.flip()

                event = None
                while event is None:
                    event = self.game_over_screen.handle_input()
                    pygame.time.delay(100)

                if event == "retry":
                    self.player.x = player_pos[0]
                    self.player.y = player_pos[1]
                    self.player.hp = 100

                    self.boss_num = random.randint(0, 1)
                    self.boss.boss_type = self.boss_type[self.boss_num]
                    self.boss.hp = 200
                    self.boss.fireballs = []
                    self.boss.lavas = []
                    self.boss.snow_patches = []
                    self.boss.snowballs = []

                    self.game_start_time = time.time()
                    continue
                elif event == "menu":
                    return "menu"

            if self.boss.hp <= 0 and not self.boss_defeated:
                self.boss_defeated = True
                time.sleep(0.1)
                self.initialize_boss()

                self.player.boss_defeated += 1
                self.player.x = player_pos[0]
                self.player.y = player_pos[1]
                continue

            if self.ball and self.ball.active:
                self.ball.move_towards_player(self.player)
                self.ball.draw()

            self.player.draw()
            self.boss.draw()
            self.player.update()
            self.draw_timer()

            for particle in self.player.deflect_particles:
                particle.draw()

            if self.boss_type[self.boss_num] == "fire":
                self.boss.fireball(self.player)
                self.boss.update_fireballs(self.player)

                self.boss.create_lava(self.player)
                self.boss.update_lavas(self.player)

            elif self.boss_type[self.boss_num] == "ice":
                self.boss.snowball(self.player)
                self.boss.update_snowballs(self.player)

                self.boss.create_snow(self.player)
                self.boss.update_snow(self.player)

            self.update_health_bars()
            self.draw_health_bars()
            draw_ui()

            if self.player.wall and self.player.wall.active:
                self.player.wall.move()
                self.player.wall.draw()

                if self.player.wall.check_collision(self.ball):
                    self.ball.move_towards_boss(self.boss.x, self.boss.y)

                for fireball in self.boss.fireballs:
                    if self.player.wall.check_collision(fireball):
                        fireball.active = False

            keys = pygame.key.get_pressed()
            self.player.update_movement(keys)

            if not self.ball.active:
                self.ball.reset_position(self.boss.x + self.boss.width // 2, self.boss.y + self.boss.height // 2)

            if self.ball.target_x is not None and self.ball.target_y is not None:
                self.ball.update_position()

            self.ball.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()
                    elif event.key == pygame.K_q:
                        self.player.use_ability(self.ball)
                    elif event.key == pygame.K_e:
                        self.player.deflect(self.ball, self.boss, self.boss.x, self.boss.y)

            pygame.display.flip()
            clock.tick(60)

        return "quit"

def run():
    pygame.init()

    while True:
        character_selection = CharacterSelection()
        show_menu = True

        while show_menu:
            screen.blit(main_background, (0,0))
            character_selection.draw_title()
            character_selection.draw_characters()
            character_selection.draw_instructions()
            character_selection.draw_quit_button()
            pygame.display.flip()

            show_menu = not character_selection.handle_input()

        game = Game()
        game.character_selection = character_selection
        game_result = game.start_game()

        if game_result == "quit":
            pygame.quit()
            sys.exit()

run()

