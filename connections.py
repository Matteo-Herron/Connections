import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((1000,558))

#Textures
normal = pygame.image.load("Game Textures/normal.png").convert()
start = pygame.image.load("Game Textures/start.png").convert()
quit = pygame.image.load("Game Textures/quit.png").convert()
blank = pygame.image.load("Game Textures/blank.png").convert()
x_un = pygame.image.load("Game Textures/x_un.png").convert()
x_cli = pygame.image.load("Game Textures/x_cli.png").convert()
enter_un = pygame.image.load("Game Textures/enter_un.png").convert()
enter_cli = pygame.image.load("Game Textures/enter_cli.png").convert()
one_away = pygame.image.load("Game Textures/one_away.png").convert()
word_cover = pygame.image.load("Game Textures/word_cover.png").convert()
try_again = pygame.image.load("Game Textures/try_again.png").convert()
nice_job = pygame.image.load("Game Textures/nice_job.png").convert()



example_string = [["yellow","words that are red", "red", "red", "red", "red"],
                  ["green","words that are green", "green", "green", "green", "green"],
                  ["blue","words that are blue", "blue", "blue", "blue", "blue"],
                  ["purple","words that are purple", "purple", "purple", "purple", "purple"]]



#Block Positions
block_vec = [
[pygame.Rect(30.0, 62.0, 210.0, 62.0), 0],
[pygame.Rect(270.0, 62.0, 210.0, 62.0), 0],
[pygame.Rect(510.0, 62.0, 210.0, 62.0), 0],
[pygame.Rect(750.0, 62.0, 210.0, 62.0), 0],

[pygame.Rect(30.0, 155.0, 210.0, 62.0), 0],
[pygame.Rect(270.0, 155.0, 210.0, 62.0), 0],
[pygame.Rect(510.0, 155.0, 210.0, 62.0), 0],
[pygame.Rect(750.0, 155.0, 210.0, 62.0), 0],

[pygame.Rect(30.0, 248.0, 210.0, 62.0), 0],
[pygame.Rect(270.0, 248.0, 210.0, 62.0), 0],
[pygame.Rect(510.0, 248.0, 210.0, 62.0), 0],
[pygame.Rect(750.0, 248.0, 210.0, 62.0), 0],

[pygame.Rect(30.0, 341.0, 210.0, 62.0), 0],
[pygame.Rect(270.0, 341.0, 210.0, 62.0), 0],
[pygame.Rect(510.0, 341.0, 210.0, 62.0), 0],
[pygame.Rect(750.0, 341.0, 210.0, 62.0), 0],
]

#Collision Boxes
quit_rect = pygame.Rect(0.0, 0.0, 44.0, 46.0)
enter_rect = pygame.Rect(348.0, 420.0, 303.0, 133.0)

#Variables
normal_active = False
blank_active = False
x_cli_active = False
x_un_active = False
draw_active = False
enter_un_active = False
enter_cli_active = False
redraw_active = True
game_font = pygame.freetype.Font("font.ttf", 35)
row_counter = 0

#Clicked box vector
clicked_boxes = []


#Start Program, main menu state
run = True
gamestate = "menu"


while run:
    while gamestate == "menu":

        if normal_active == False:
            screen.blit(normal, (0,0))
            pygame.display.flip()
            normal_active = True

        pos = pygame.mouse.get_pos()

        if pos[1] >= 335 and pos[1] <= 466:
            if pos[0] >= 145 and pos[0] <= 444:
                screen.blit(start, (0,0))
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gamestate = "game"
            elif pos[0] >= 560 and pos[0] <= 859:
                screen.blit(quit, (0,0))
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gamestate = "quit"
                    run = False
            else:
                screen.blit(normal, (0,0))
                pygame.display.flip()
        else:
            screen.blit(normal, (0,0))
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = "quit"
                run = False
    normal_active = False

    while gamestate == "game":
        pos = pygame.mouse.get_pos()
        if blank_active == False:
            screen.blit(blank, (0,0))
            pygame.display.flip()
            blank_active = True

        if x_un_active == False:
            if not quit_rect.collidepoint(pos):
                x_cli_active = False
                screen.blit(x_un, (0,0))
                pygame.display.flip()
                x_un_active = True

        if enter_un_active == False:
            if not enter_rect.collidepoint(pos):
                enter_cli_active = False
                screen.blit(enter_un, (348,420))
                pygame.display.flip()
                enter_un_active = True
        
        if draw_active == False:
            for example in example_string:
                for i in range(4):
                    chosen_block = random.choice(block_vec)
                    while chosen_block[1] != 0:
                        chosen_block = random.choice(block_vec)
                    chosen_block[1] = example[2+i]
                    pygame.draw.rect(screen, pygame.Color(210, 180, 180, 255), chosen_block[0])
                    game_font.render_to(screen, (chosen_block[0].x + 30, chosen_block[0].y + 10), example[2+i], (0, 0, 0))
                    pygame.display.flip()
            draw_active = True

        if redraw_active == False:
            for block in block_vec:
                pygame.draw.rect(screen, pygame.Color(210, 180, 180, 255), block[0])
                game_font.render_to(screen, (block[0].x + 30, block[0].y + 10), block[1], (0, 0, 0))
                pygame.display.flip()
            redraw_active = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = "quit"
                run = False
            if quit_rect.collidepoint(pos):
                if x_cli_active == False:
                    x_un_active = False
                    screen.blit(x_cli, (0,0))
                    pygame.display.flip()
                    x_cli_active = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gamestate = "menu"
                    draw_active = False
                    enter_un_active = False
                    for block in block_vec:
                        block[1] = 0
                    row_counter = 0
            if enter_rect.collidepoint(pos) and len(clicked_boxes) == 4:
                if enter_cli_active == False:
                    enter_un_active = False
                    screen.blit(enter_cli, (348,420))
                    pygame.display.flip()
                    enter_cli_active = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    correct_counter = 0
                    answer_closeness = []
                    for example in example_string:
                        for i in range(4):
                            if clicked_boxes[i][1] in example:
                                correct_counter += 1
                        answer_closeness.append(correct_counter)
                        correct_counter = 0
                    if max(answer_closeness) == 4:
                        screen.blit(nice_job, (681, 470))
                        pygame.display.flip()
                        time.sleep(1.5)
                        screen.blit(word_cover, (681, 470))
                        pygame.display.flip()
                        redraw_active = False
                        for i in range(4):
                            word_hold = clicked_boxes[i][1]
                            clicked_boxes[i][1] = block_vec[4*row_counter + i][1]
                            block_vec[4*row_counter + i][1] = word_hold
                        row_counter += 1
                        clicked_boxes = []
                    elif max(answer_closeness) == 3:
                        screen.blit(one_away, (681, 470))
                        pygame.display.flip()
                        time.sleep(1.5)
                        screen.blit(word_cover, (681, 470))
                        pygame.display.flip()
                    else:
                        screen.blit(try_again, (681, 470))
                        pygame.display.flip()
                        time.sleep(1.5)
                        screen.blit(word_cover, (681, 470))
                        pygame.display.flip()        
            if event.type == pygame.MOUSEBUTTONDOWN:
                for block in block_vec:
                    block_identity = block[0]
                    if block_identity.collidepoint(pos):
                        if block in clicked_boxes and len(clicked_boxes) <= 4:
                            clicked_boxes.remove(block)
                            pygame.draw.rect(screen, pygame.Color(210, 180, 180, 255), block_identity)
                            game_font.render_to(screen, (block_identity.x + 30, block_identity.y + 10), block[1], (0, 0, 0))
                            pygame.display.flip()
                        elif len(clicked_boxes) < 4:
                            clicked_boxes.append(block)
                            pygame.draw.rect(screen, pygame.Color(210, 120, 120, 255), block_identity)
                            game_font.render_to(screen, (block_identity.x + 30, block_identity.y + 10), block[1], (0, 0, 0))
                            pygame.display.flip()

    
    blank_active = False
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

pygame.quit()