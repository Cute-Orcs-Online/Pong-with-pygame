import pygame, random
pygame.init()

def serve(x, y, wind_x, wind_y):
    y_serve = randrange(wind_y + 1)

    balance = randrange(10)
    if balance <= 5:
        x_serve = (x + wind_x/16)
    if balanxe > 5:
        x_serve = (x - wind_x/16)
    tuple_serve = [x_serve, y_serve]

    return tuple_serve

#window
size = 768, 576
window = pygame.display.set_mode(size)
pygame.display.set_caption('NieR: Automata')

#clock
timer = pygame.time.Clock()
FPS = 60

#scoring
p1_score = 0
p2_score = 0
scored = False
scoring_counter = 0
p_scored = ''
rally = 0

p1_goal = 0, 0, int((size[0]/8) + 12), size[1]
p2_goal = int((size[0] - (size[0]/8)) -12), 0, 200, size[1]

#colour
white = 255, 255, 255
black = 0, 0, 0
bg_pink = 232, 128, 128
goal_pink = 105, 58, 58

#font
StatusFont = pygame.font.Font("fonts/Roboto-Bold.ttf", 16)
ScoreFont = pygame.font.Font("fonts/Roboto-Bold.ttf", 46)

#objects
player_size = 23, 103
ball_size = 15, 15

#position
p1_x = size[0]/8
p1_y = size[1]/2

p2_x = (size[0] - (size[0]/8)) - player_size[0]
p2_y = size[1]/2

x_default = size[0]/2 - (ball_size[0]/2)
ball_x = x_default
y_default = size[1]/2 - (ball_size[1]/2)
ball_y = y_default

#movement
up1 = False
down1 = False
up2 = False
down2 = False
player_speed = 5 #player speed = pixel/frame

x_speed = 1
y_speed = 1
SPEEDBOOST = 3

#GAME LOOP
loop = 1
while loop:

    timer.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:   #player 1
                up1 = True
            if event.key == pygame.K_s:
                down1 = True
            if event.key == pygame.K_UP:  #player 2
                up2 = True
            if event.key == pygame.K_DOWN:
                down2 = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  #player 1
                up1 = False
            if event.key == pygame.K_s:
                down1 = False
            if event.key == pygame.K_UP:  #player 2
                up2 = False
            if event.key == pygame.K_DOWN:
                down2 = False

    #UPDATE
    if scored == True:
        scoring_counter += 1

    if scoring_counter == (5*FPS):
        scored = False
        scoring_counter = 0

    if up1 == True:
        p1_y -= player_speed
    if down1 == True:
        p1_y += player_speed

    if up2 == True:
        p2_y -= player_speed
    if down2 == True:
        p2_y += player_speed

    if (p1_y + player_size[1]) >= size[1]:
        p1_y = (size[1] - player_size[1])
    if p1_y <= 0:
        p1_y = 0

    p1_block = p1_x, p1_y, player_size[0], player_size[1]

    if (p2_y + player_size[1]) >= size[1]:
        p2_y = (size[1] - player_size[1])

    if p2_y <= 0:
        p2_y = 0

    p2_block = p2_x, p2_y, player_size[0], player_size[1]

    # ___
    #|   |    /\    |     |
    #|--<    /__\   |     |
    #|___|  /    \  |___  |___
    #

    ball_x += x_speed * (SPEEDBOOST * (1 + rally/10))
    ball_y += y_speed * (SPEEDBOOST * (1 + rally/10))

    ball_side = [ball_x, ball_y, (ball_x + ball_size[0]), (ball_y + ball_size[1])]     #ball_sides = [left[0], top[1], right[2], bottom[3]]

    #Wall Collision:
    if ball_side[0] <= 0:
        ball_x = 0
        x_speed = 1

    if ball_side[2] >= size[0]:
        ball_x = (size[0] - ball_size[0])
        x_speed = -1

    if ball_side[1] <= 0:
        ball_y = 0
        y_speed = 1

    if ball_side[3] >= size[1]:
        ball_y = (size[1] - ball_size[1])
        y_speed = -1

    #Paddle Collision:
    if ball_side[0] <= (p1_x + player_size[0]) and ball_side[0] > p1_x and ball_side[3] >= p1_y and ball_side[1] <= (p1_y + player_size[1]):
        ball_x = p1_x + player_size[0]
        rally += 1
        x_speed = 1

    if ball_side[2] >= p2_x and (ball_side[2] < p2_x + player_size[0]) and ball_side[3] >= p2_y and ball_side[1] <= (p2_y + player_size[1]):
        ball_x = p2_x - ball_size[0]
        rally += 1
        x_speed = -1

    #Goal Scoring
    if ball_side[0] < (p1_goal[0] + p1_goal[2]) and scored == False:
        p2_score += 1
        p_scored = 'Player Two'
        scored = True
        rally = 0

    if ball_side[2] > (p2_goal[0]) and scored == False:
        p1_score += 1
        p_scored = 'Player One'
        scored = True
        rally = 0

    #||===\\  ||==== ||====  ||    ||  //====>>
    #||    || ||     ||   >> ||    || || 
    #||    || ||==   ||====  ||    || ||  ===\\
    #||    || ||     ||   >> ||    || ||     ||
    #||===//  ||==== ||====   \\==//   \\====//

#    print('FPS:', timer.get_fps())
#    print('Ball X:', ball_x)
#    print('Ball Y:', ball_y)
#    print('-----------------')


    ball = [ball_x, ball_y , ball_size[0], ball_size[1]]

    fps_got = timer.get_fps()
    status_bar = ('FPS:', round(fps_got, 2), 'Rally:', rally, 'Player 1 Score:', p1_score, 'Player 2 Score:', p2_score)
    score_message = str((p_scored, "Scored!"))

    line1 = StatusFont.render(str(status_bar), True, black)
    line2 = ScoreFont.render((score_message), True, black)

    score_dist = ScoreFont.size(score_message)
    score_blit = (size[0]/2) - (score_dist[0]/2), (size[1]/2) - (score_dist[1]/2)

    #DRAW
    window.fill(bg_pink)

    pygame.draw.rect(window, goal_pink, (p1_goal))
    pygame.draw.rect(window, goal_pink, (p2_goal))

    window.blit(line1, (0,0))
    if scored == True:
        window.blit(line2, (score_blit))

    pygame.draw.rect(window, white, (p1_block))
    pygame.draw.rect(window, white, (p2_block))
    pygame.draw.rect(window, white, (ball))
    pygame.display.flip()
#end
