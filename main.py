import random
import pygame

pygame.init()

HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Flying Game')
font = pygame.font.Font('freesansbold.ttf', 20)
fps = 144
timer = pygame.time.Clock()
new_map = True
map_rects = []
rect_width = 1
total_rects = WIDTH // rect_width
spacer = 1
player_x = 100
player_y = 300
flying = False
y_speed = 0
gravity = 0.1
map_speed = 2
score = 0
high_score = 0
active = True
#chicken = pygame.transform.scale(pygame.image.load('Chicken.png'), (60, 60))
#chicken_death = pygame.transform.scale(pygame.image.load('Chicken Death.png'), (60, 60))


def generate_new():
    global player_y
    rects = []
    top_height = random.randint(0, 300)
    player_y = top_height + 150
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        top_rect = pygame.draw.rect(screen, 'red', [i * rect_width, 0, rect_width, top_height])
        bot_rect = pygame.draw.rect(screen, 'red', [i * rect_width, top_height + 300, rect_width, HEIGHT])
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects


def draw_map(rects):
    for i in range(len(rects)):
        pygame.draw.rect(screen, 'red', rects[i])
    pygame.draw.rect(screen, 'dark gray', [0, 0, WIDTH, HEIGHT], 12)


def draw_player():
  player = pygame.draw.circle(screen, 'white', (player_x, player_y), 20)
  #if active == True:
    #screen.blit(chicken, (player_x - 40, player_y - 30))
  return player


def move_player(y_pos, speed, fly):
    if fly:
        speed += gravity
    else:
        speed -= gravity
    y_pos -= speed
    return y_pos, speed


def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - map_speed, rects[i][1], rect_width, rects[i][3])
        if rects[i][0] + rect_width < 0:
            rects.pop(1)
            rects.pop(0)
            top_height = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if top_height < 0:
                top_height = 0
            elif top_height > 300:
                top_height = 300
            rects.append((rects[-2][0] + rect_width, 0, rect_width, top_height))
            rects.append((rects[-2][0] + rect_width, top_height + 300, rect_width, HEIGHT))
            score += 1
    return rects


def check_collision(rects, circle, act):
    for i in range(len(rects)):
        if circle.colliderect(rects[i]):
          #screen.blit(chicken_death, (player_x - 40, player_y - 30))
          act = False
    return act


run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if new_map:
        map_rects = generate_new()
        new_map = False
    draw_map(map_rects)
    player_circle = draw_player()
    if active:
        player_y, y_speed = move_player(player_y, y_speed, flying)
        map_rects = move_rects(map_rects)
    active = check_collision(map_rects, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying = True
            if event.key == pygame.K_RETURN:
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 2
                    if score > high_score:
                        high_score = score
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flying = False
    map_speed = 2 + score//1000
    spacer = 1 + score//2000

    screen.blit(font.render(f'Score: {score}', True, 'black'), (20, 15))
    screen.blit(font.render(f'High Score: {high_score}', True, 'black'), (20, 565))
    if not active:
        screen.blit(font.render('Press Enter to Restart', True, 'black'), (300, 15))
        screen.blit(font.render('Press Enter to Restart', True, 'black'), (300, 565))
    pygame.display.flip()
pygame.quit()
