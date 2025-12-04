import pygame

pygame.init()

screen = pygame.display.set_mode((1000,558))

#Textures
normal = pygame.image.load("game pics/normal.png").convert()
start = pygame.image.load("game pics/start.png").convert()
quit = pygame.image.load("game pics/quit.png").convert()
blank = pygame.image.load("game pics/blank.png").convert()
x_un = pygame.image.load("game pics/x_un.png").convert()
x_cli = pygame.image.load("game pics/x_cli.png").convert()

#Block Positions
block_vec = [
pygame.Rect(30.0, 62.0, 210.0, 62.0),
pygame.Rect(270.0, 62.0, 210.0, 62.0),
pygame.Rect(510.0, 62.0, 210.0, 62.0),
pygame.Rect(750.0, 62.0, 210.0, 62.0),

pygame.Rect(30.0, 186.0, 210.0, 62.0),
pygame.Rect(270.0, 186.0, 210.0, 62.0),
pygame.Rect(510.0, 186.0, 210.0, 62.0),
pygame.Rect(750.0, 186.0, 210.0, 62.0),

pygame.Rect(30.0, 310.0, 210.0, 62.0),
pygame.Rect(270.0, 310.0, 210.0, 62.0),
pygame.Rect(510.0, 310.0, 210.0, 62.0),
pygame.Rect(750.0, 310.0, 210.0, 62.0),

pygame.Rect(30.0, 434.0, 210.0, 62.0),
pygame.Rect(270.0, 434.0, 210.0, 62.0),
pygame.Rect(510.0, 434.0, 210.0, 62.0),
pygame.Rect(750.0, 434.0, 210.0, 62.0),
]

#Collision Boxes
quit_rect = pygame.Rect(0.0,0.0, 44.0, 46.0)

#Variables
normal_active = False
blank_active = False
x_cli_active = False
x_un_active = False
draw_active = False

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
        
        if draw_active == False:
            for block in block_vec:
                pygame.draw.rect(screen, pygame.Color(210, 180, 180, 255), block)
                pygame.display.flip()
            draw_active = True
        
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                for block in block_vec:
                    if block.collidepoint(pos):
                        if block in clicked_boxes and len(clicked_boxes) <= 4:
                            clicked_boxes.remove(block)
                            pygame.draw.rect(screen, pygame.Color(210, 180, 180, 255), block)
                            pygame.display.flip()
                        elif len(clicked_boxes) < 4:
                            clicked_boxes.append(block)
                            pygame.draw.rect(screen, pygame.Color(210, 120, 120, 255), block)
                            pygame.display.flip()

    
    blank_active = False
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

pygame.quit()





'''
16 rectangles objects offset by 0
print one random word in each
check if mouse is touching one
if it is and it clicks and the rectangle isn't black:
    highlight black
    push rectangle to clicked list
if it is and it clicks and the rectangle is black:
    unhighlight black
    pop rectangle from clicked list
if four rectangles are in the clicked list:
    submit button is clickable
    click:
        if one is incorrect
            print "one away"
            update try counter by -1
        if they are correct
            print 4 members next to each other on top row offset by number of correct answers
            highlight with the category color and print category and words
            trash the 4 rects so they can't be rehighlighted
        if >1 are incorrect
            update try counter by -1
if try counter = 0
    print "better luck next time"
    group available words and highlight/print one category at a time
    popup - quit or restart
'''