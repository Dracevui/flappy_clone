import pygame
import sys
import random
import math
from level import Level


def draw_floor():
    WINDOW.blit(floor_surface, (floor_x_pos, 900))
    WINDOW.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            WINDOW.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            WINDOW.blit(flip_pipe, pipe)


def check_collision(pipes):
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


def rotate_sprite(sprite):
    new_sprite = pygame.transform.rotate(sprite, -sprite_mvmt * 2.5)
    return new_sprite


def sprite_animation():
    new_sprite = sprite_frames[sprite_index]
    new_sprite_rect = new_sprite.get_rect(center=(100, sprite_rect.centery))
    return new_sprite, new_sprite_rect


def score_display(game_state):
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


def update_score(scores, high_score):
    if scores > high_score:
        high_score = scores
    return high_score


def pipe_score_check():
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
# WIDTH = 576
# HEIGHT = 1024
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
ICE_ASSETS = Level(
    pygame.image.load("assets/iceberg-background.png").convert(),
    pygame.image.load("assets/ice-base.png").convert(),
    pygame.image.load("assets/icicle.png").convert_alpha(),
    pygame.image.load("assets/peng-upflap.png").convert_alpha(),
    pygame.image.load("assets/peng-midflap.png").convert_alpha(),
    pygame.image.load("assets/peng-downflap.png").convert_alpha(),
    pygame.transform.scale2x(pygame.image.load("assets/ice_message.png").convert_alpha()),
    pygame.mixer.Sound("sound/sfx_wing.wav")
)

DESERT_ASSETS = Level(
    pygame.image.load("assets/desert-background.png").convert(),
    pygame.image.load("assets/desert-base.png").convert(),
    pygame.image.load("assets/dust_devil1.png").convert_alpha(),
    pygame.image.load("assets/grasshopper_df.png").convert_alpha(),
    pygame.image.load("assets/grasshopper_mf.png").convert_alpha(),
    pygame.image.load("assets/grasshopper_uf.png").convert_alpha(),
    pygame.transform.scale2x(pygame.image.load("assets/desert_message.png").convert_alpha()),
    pygame.mixer.Sound("sound/sfx_wing.wav")
)

user_choice = "Desert"

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
    movement_sound = DESERT_ASSETS.mvmt_sfx


death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")

bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


sprite_frames = [sprite_df, sprite_mf, sprite_uf]
sprite_index = 0
sprite_surface = sprite_frames[sprite_index]
sprite_rect = sprite_surface.get_rect(center=(100, 512))


pygame.display.set_icon(sprite_uf)


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
        WINDOW.blit(game_over_surface, game_over_rect)
        hi_score = update_score(score, hi_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(144)
