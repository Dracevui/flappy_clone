import pygame
import sys
import random
import math
from level import Level


def instruction_screen():  # Displays Instruction Screen when game launches
    global running
    instruction_state = False
    while not instruction_state:
        WINDOW.fill(WHITE)
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                instruction_state = True
                running = False
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WINDOW.blit(instructions_surface, (0, 0))
        pygame.display.flip()


def level_select_screen():
    WINDOW.fill(WHITE)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    WINDOW.blit(level_select_surface, (0, 0))
    WINDOW.blit(ice_button_surface, (5, 462))
    WINDOW.blit(desert_button_surface, (297, 462))
    # pygame.display.update()


def level_select():
    level_state = False
    choice = ""
    while not level_state:
        level_button_hover()
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if desert_button_rect.collidepoint(mouse_position):
                    choice = "Desert"
                    level_state = True
                elif ice_button_rect.collidepoint(mouse_position):
                    choice = "Ice"
                    level_state = True
    return choice


def level_button_hover():
    for events in pygame.event.get():
        if events.type == pygame.MOUSEMOTION:
            if desert_button_rect.collidepoint(pygame.mouse.get_pos()):
                WINDOW.blit(desert_button_invert, (297, 462))
            if ice_button_rect.collidepoint(pygame.mouse.get_pos()):
                WINDOW.blit(ice_button_invert, (5, 462))
            if not desert_button_rect.collidepoint(pygame.mouse.get_pos()):
                WINDOW.blit(desert_button_surface, (297, 462))
            if not ice_button_rect.collidepoint(pygame.mouse.get_pos()):
                WINDOW.blit(ice_button_surface, (5, 462))
            pygame.display.update()
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def draw_back_buttons():
    if user_choice == "Ice":
        WINDOW.blit(ice_back_surface, (5, 0))
    else:
        WINDOW.blit(desert_back_surface, (5, 0))


def back_buttons_logic():
    global user_choice
    global running
    global game_active
    for events in pygame.event.get():
        if events.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            if ice_back_rect.collidepoint(mouse_position) or desert_back_rect.collidepoint(mouse_position):
                level_select_screen()
                user_choice = level_select()
                # running = True
                # game_active = False
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def asset_assignment(choice):
    if choice == "Desert":
        asset = Level(
            pygame.image.load("assets/desert-background.png").convert(),
            pygame.image.load("assets/desert-base.png").convert(),
            pygame.image.load("assets/dust_devil2.png").convert_alpha(),
            pygame.image.load("assets/grasshopper_df.png").convert_alpha(),
            pygame.image.load("assets/grasshopper_mf.png").convert_alpha(),
            pygame.image.load("assets/grasshopper_uf.png").convert_alpha(),
            pygame.transform.scale2x(pygame.image.load("assets/desert_message.png").convert_alpha()),
            pygame.mixer.Sound("sound/sfx_wing.wav")
        )
    else:
        asset = Level(
            pygame.image.load("assets/iceberg-background.png").convert(),
            pygame.image.load("assets/ice-base.png").convert(),
            pygame.image.load("assets/icicle.png").convert_alpha(),
            pygame.image.load("assets/peng-upflap.png").convert_alpha(),
            pygame.image.load("assets/peng-midflap.png").convert_alpha(),
            pygame.image.load("assets/peng-downflap.png").convert_alpha(),
            pygame.transform.scale2x(pygame.image.load("assets/ice_message.png").convert_alpha()),
            pygame.mixer.Sound("sound/sfx_wing.wav")
        )
    return asset


def draw_floor():  # Draws the floor asset onto the game window
    WINDOW.blit(floor_surface, (floor_x_pos, 900))
    WINDOW.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():  # Creates a pipe in a random position and adds it to the pipe list variable
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):  # Moves the pipes along the screen
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):  # Draws the pipes onto the game window
    for pipe in pipes:
        if pipe.bottom >= 1024:
            WINDOW.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            WINDOW.blit(flip_pipe, pipe)


def check_collision(pipes):  # Handles the logic of game collision
    global can_score
    for pipe in pipes:
        if sprite_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if sprite_rect.top <= -100 or sprite_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False

    return True


def rotate_sprite(sprite):  # Rotates the character sprite for animation
    new_sprite = pygame.transform.rotate(sprite, -sprite_mvmt * 2.5)
    return new_sprite


def sprite_animation():  # Animates the sprite for immersion purposes
    new_sprite = sprite_frames[sprite_index]
    new_sprite_rect = new_sprite.get_rect(center=(100, sprite_rect.centery))
    return new_sprite, new_sprite_rect


def score_display(game_state):  # Writes out the current score and high score onto the game window
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        WINDOW.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        WINDOW.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(hi_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        WINDOW.blit(high_score_surface, high_score_rect)


def update_score(scores, high_score):  # Handles the logic of updating the high score
    if scores > high_score:
        high_score = scores
    return high_score


def pipe_score_check():  # Checks to see if the current position of the character will allow for a score update
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


# Constants
pygame.init()
MONITOR = pygame.display.Info()
WIDTH = 576
HEIGHT = 1024
# WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
WINDOW = pygame.display.set_mode((math.floor(MONITOR.current_w * 0.3), math.floor(MONITOR.current_h * 0.94)))
pygame.display.set_caption("Penglide")
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)
running = False
WHITE = (255, 255, 255)

# Game Variables
gravity = 0.25
sprite_mvmt = 0
game_active = True
score = 0
hi_score = 0
can_score = True

# Asset Files
ICE_ASSETS = asset_assignment("Ice")
DESERT_ASSETS = asset_assignment("Desert")


level_select_surface = pygame.image.load("assets/level_selector.png").convert_alpha()
level_select_surface = pygame.transform.scale2x(level_select_surface)

ice_button_surface = pygame.image.load("assets/ice_button.png")
ice_button_surface = pygame.transform.scale2x(ice_button_surface)
ice_button_rect = ice_button_surface.get_rect(topleft=(5, 462))
ice_button_invert = pygame.transform.scale2x((pygame.image.load("assets/ice_button_invert.png").convert_alpha()))

desert_button_surface = pygame.image.load("assets/desert_button.png")
desert_button_surface = pygame.transform.scale2x(desert_button_surface)
desert_button_rect = desert_button_surface.get_rect(topleft=(297, 462))
desert_button_invert = pygame.transform.scale2x((pygame.image.load("assets/desert_button_invert.png").convert_alpha()))

instructions_surface = pygame.image.load("assets/Onscreen_Instructions.png").convert_alpha()
instructions_surface = pygame.transform.scale(instructions_surface, (576, 1024))

ice_back_surface = pygame.image.load("assets/ice_back.png").convert_alpha()
ice_back_rect = ice_back_surface.get_rect(topleft=(5, 0))
desert_back_surface = pygame.image.load("assets/desert_back.png").convert_alpha()
desert_back_rect = desert_back_surface.get_rect(topleft=(5, 0))


instruction_screen()  # shows instruction screen when game is launched

level_select_screen()  # shows the level select screen

user_choice = level_select()  # handles the logic of level selection

if user_choice == "Ice":
    bg_surface = ICE_ASSETS.background
    floor_surface = ICE_ASSETS.floor
    pipe_surface = ICE_ASSETS.pipe
    sprite_df = ICE_ASSETS.sprite1
    sprite_mf = ICE_ASSETS.sprite2
    sprite_uf = ICE_ASSETS.sprite3
    game_over_surface = ICE_ASSETS.game_over
    movement_sound = ICE_ASSETS.mvmt_sfx
else:
    bg_surface = DESERT_ASSETS.background
    floor_surface = DESERT_ASSETS.floor
    pipe_surface = DESERT_ASSETS.pipe
    sprite_df = DESERT_ASSETS.sprite1
    sprite_mf = DESERT_ASSETS.sprite2
    sprite_uf = DESERT_ASSETS.sprite3
    game_over_surface = DESERT_ASSETS.game_over
    movement_sound = ICE_ASSETS.mvmt_sfx


death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")


bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


sprite_frames = [sprite_df, sprite_mf, sprite_uf]
sprite_index = 0
sprite_surface = sprite_frames[sprite_index]
sprite_rect = sprite_surface.get_rect(center=(100, 512))


ICON = pygame.image.load("assets/penglide-icon.png").convert_alpha()
pygame.display.set_icon(ICON)


SPRITEFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(SPRITEFLAP, 250)


pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]


game_over_rect = game_over_surface.get_rect(center=(288, 512))


while not running:
    WINDOW.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    WINDOW.blit(bg_surface, (0, 0))
    WINDOW.blit(game_over_surface, game_over_rect)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(144)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                sprite_mvmt = 0
                sprite_mvmt -= 9
                movement_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                sprite_rect.center = (100, 512)
                sprite_mvmt = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == SPRITEFLAP:
            if sprite_index < 2:
                sprite_index += 1
            else:
                sprite_index = 0

            sprite_surface, sprite_rect = sprite_animation()

    WINDOW.blit(bg_surface, (0, 0))

    if game_active:
        # Sprite
        sprite_mvmt += gravity
        rotated_sprite = rotate_sprite(sprite_surface)
        sprite_rect.centery += sprite_mvmt
        WINDOW.blit(rotated_sprite, sprite_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display("main_game")

    else:
        WINDOW.blit(game_over_surface, game_over_rect, draw_back_buttons())
        hi_score = update_score(score, hi_score)
        score_display("game_over")
        back_buttons_logic()

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(144)
