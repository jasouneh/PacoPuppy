import pygame, sys, math, random
from config import *

#init screen
screenSize=[600,800]

pygame.init() 
screen = pygame.display.set_mode(screenSize)
screen.fill((255,255,255))
pygame.display.set_caption('Paco Puppy')
clock=pygame.time.Clock()
menuFont = pygame.font.SysFont('comicsansms', 160)
font = pygame.font.SysFont('comicsansms',40)

#init imgs
bg_surface = pygame.image.load('game_imgs/ocean.png')
bg_surface=pygame.transform.scale(bg_surface,screenSize)

#global vars
floor_start_y = screenSize[1]-100
score = 0
can_score = True
pipe_speed = 5
SPAWNPIPE = 0


def run(state):
    while state != None:
        state = state()


def game_exit():
    return None

def game_intro():   
    #add for future game intro
    return game_menu

click = False
def game_menu():    
    #creating buttons and text
    button_width=screenSize[0]/5
    screen_divider_x=screenSize[0]/5
    button_start_y = (6*screenSize[1]/8)
    screen_divider_y=screenSize[1]/6
    
    button_1_image = pygame.image.load('game_imgs\Button_White (4).png')
    button_1_image.convert()

    
    rect1 = button_1_image.get_rect()
    pygame.Rect.move_ip(rect1, screen_divider_x,screen_divider_y*3)
    rect2 = button_1_image.get_rect()
    pygame.Rect.move_ip(rect2, screen_divider_x,screen_divider_y*4)
    rect3 = button_1_image.get_rect()
    pygame.Rect.move_ip(rect3, screen_divider_x,screen_divider_y*5)

    text1 = font.render("START", True, BLUE)
    text2 = font.render("OPTIONS", True, BLUE)
    text3 = font.render("EXIT", True, BLUE)
    buttons = [
        [text1,rect1,button_1_image],
        [text2,rect2,button_1_image],
        [text3,rect3,button_1_image]
    ]
    

    inMenu=0
    while True:
        screen.blit(bg_surface,(0,0) )
        draw_menu_text('Menu',menuFont,(255,255,255),screen,screenSize[0]/2,screenSize[1]/8)
        mouse_pos= pygame.mouse.get_pos()

        #handle events
        for e in pygame.event.get():
            #quit event
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            #color change for button hover
            elif e.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button[1].collidepoint(mouse_pos):
                        button[2]=BUTTON_HOVER_COLOR
                    else:
                        button[2]=BLACK
                    
            #handle clicks
            if e.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if e.button == 1 and button[1].collidepoint(mouse_pos):
                        #options event handle
                        if button[0]==text1:
                            return game_play
                        #play event handle
                        elif button[0]==text2:
                            return game_options
                        #quit event handle
                        elif button[0]==text3:
                            return game_exit

            
        
        #drawing buttons and text
        screen.blit(button_1_image, rect1)
        screen.blit(button_1_image, rect2)
        screen.blit(button_1_image, rect3)
        for text, rect, surface in buttons:
            screen.blit(text,rect)
        


        pygame.display.update()
        clock.tick(30)
        
  

def game_play(highscore=0):  
    global score, SPAWNPIPE
    #game variables
    gravity = .5
    jump_distance = 6
    isGameActive = True

    #game sounds
    
    #init floor img
    floor_img = pygame.image.load('game_imgs\grassMid.png').convert()
    floor_rect_test = pygame.Rect((0,floor_start_y), (screenSize[0], 100 ))
    floor_surface = pygame.Surface((floor_rect_test.width,floor_rect_test.height))
    floor_img = pygame.transform.scale(floor_img,(floor_rect_test.w,floor_rect_test.h),floor_surface)

    #init player img
    player_image = pygame.image.load('game_imgs\p1_front.png')
    player_rect = player_image.get_rect()
    player_rect.bottomleft = (0,floor_start_y-200)
    
    

    #pipes
    pipe_surface = pygame.image.load('game_imgs/pipe-green.png')
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE,1500)

    scrollIter = 0
    while True:

        #Background loop
        screen.blit(bg_surface,(scrollIter,0))
        screen.blit(bg_surface,(screenSize[0]+scrollIter,0))
        if scrollIter <= -screenSize[0]:
            scrollIter =0
        #pygame.draw.rect(screen,RED,floor_rect_test)
        screen.blit(floor_img, (scrollIter,floor_rect_test.y))
        screen.blit(floor_img, (screenSize[0]+scrollIter,floor_start_y))
        if scrollIter==-screenSize[1]:
            screen.blit(bg_surface,(screenSize[0]+scrollIter,0))
            screen.blit(floor_img, (screenSize[0]+scrollIter,floor_start_y))
            scrollIter=0
        scrollIter-=1

        #drawing pipes and score
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_surface, pipe_list)

        score_surface = font.render('Score: '+str(score),True, WHITE)
        highscore_surface = font.render('Best: '+str(highscore),True,WHITE)
        score_rect = score_surface.get_rect(topleft=(0,0))  
        highscore_rect=highscore_surface.get_rect(topleft=(0,score_rect.h))
        pipe_score_check(player_rect, pipe_list)
        screen.blit(score_surface,score_rect)
        screen.blit(highscore_surface,highscore_rect)
        if score >= highscore:
            highscore=score
            
        #drawing player img
        jump_distance+=gravity
        player_rect.centery += jump_distance
        rotated_player = rotate_player(player_image, jump_distance)
        screen.blit(rotated_player,player_rect)
        isGameActive = check_collision(player_rect, pipe_list)

        if isGameActive == False:
            return game_restart(highscore)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_SPACE and isGameActive:
                    jump_distance = 0
                    jump_distance -= 12
                
                    
            if e.type == SPAWNPIPE:
                pipe_list.extend(create_pipe(pipe_surface))
                
        
        pygame.display.update()
        clock.tick(60)


def game_options():
    pass

def draw_menu_text(text, font, color, surface, x, y):
    textobj = menuFont.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_pipe(pipe_surface):
    pipe_heights=[400,450,500]
    random_pipe_height = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop=(screenSize[0],random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(screenSize[0],random_pipe_height-300))
    return bottom_pipe,top_pipe

def move_pipes(pipe_list):
    global pipe_speed, score, can_score
    #balance ---------------
    if score==10 and can_score == False:
        pygame.time.set_timer(SPAWNPIPE, 1000)
        pipe_speed += .1
    for pipe in pipe_list:
        pipe.centerx -= pipe_speed
    visible_pipes = [pipe for pipe in pipe_list if pipe.right > 0]
    return visible_pipes

def draw_pipes(pipe_surface, pipe_list):
    for pipe in pipe_list:
        if pipe.bottom >= screenSize[1]:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,pipe)
    
def check_collision(p_rect, pipe_list):
    for pipe in pipe_list:
        if p_rect.colliderect(pipe):
            return False
        if p_rect.bottom >= floor_start_y:
            return False
        elif p_rect.top <= 0:
            return False
    return True

def game_restart(highscore=0):
    global score, pipe_speed
    pipe_speed=5
    score=0
    return game_play(highscore)

def rotate_player(surface,theta):
    return pygame.transform.rotozoom(surface,theta,1)

def pipe_score_check(player, pipe_list):
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if player.left < pipe.centerx < player.right and can_score:
                score += 1 
                can_score=False
            if pipe.centerx < 0:
                can_score=True

run(game_intro)