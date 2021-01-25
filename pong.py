##imports bc less work for me using othering ppls code
import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
from pygame import *
from gpiozero import MCP3008, Buzzer, Device


#####################################################################[init]#######################################################################

pygame.init() #initulize pygame

##############################################################[veriables]#########################################################################

white = (255,255,255) #white in RGB value as a veriable
ww = 800  #window width
wh = 600 #window height

surface = pygame.display.set_mode((ww,wh)) #veriable for the windows name (surface) will be used in rest of the code
pygame.display.set_caption("pong") # this just sets the name for the window

#controll veriables for player1 and 2 movment
P1up = False
P1down = False
P2up = False
P2down = False

#veriable list bc pygame.rect cant use index
player2 = pygame.Rect(775, 250, 20, 108)
player1 = pygame.Rect(5, 250, 20, 108)

#veirables related to the ball
ball = pygame.Rect(ww /2, wh /2, 20, 20)
x_speed = 3
y_speed = 3

#score veriables
score1 = 0
score2 = 0

#veriables for breadboard
p1_analog = MCP3008(channel=0)
p2_analog = MCP3008(channel=1)
wallbz = Buzzer(4)              #conect buzzer to GPIO4  (pin7)
playerbz = Buzzer(17)           #conect buzzer to GPIO17 (pin 11)
###################################################################[functions]#######################################################################

#function for moving player1
def move1():

    if P1up is True:   #is upDown true? if so do this
        if player1.y > 0 and player1.y -5 > 0:   #check if player1 is not touching the top of the screen (y = 0 is top x = 0 is left)
            player1.y -= 5                       #move the player down by 5 pixles each refresh
        elif player1.y > 0 and player1.y -5 < 0: #dont know
            player1.y = 0                        #dont move on the Y cords
            
    if P1down is True:                                                                   # is downDown true? if so do this
        if player1.y + player1.height < wh and (player1.y + player1.height) + 5 < wh:      # check if the y cord and the hight (bottom) of player 1 touches the bottom of the screen)
            player1.y +=5                                                                  # move the player up by 5 pixels every refresh
        elif player1.y + player1.height < wh and (player1.y + player1.height) + 5 > wh:   # not sure
            player1.y = wh - player1.height   # this makes player y(top) = 600 then subtract player hight (108) = player y = 492 player cant go lower


#function for moving player2         
def move2():    #to save my comenting EVERYTHING IN THIS FUNCTION IS SAME AS PLAYER1 JUST FOR PLAYER2
    
    if P2up is True:
        if player2.y > 0 and player2.y -5 > 0:
            player2.y -= 5
        elif player2.y > 0 and player2.y -5 < 0:
            player2.y = 0
            
    if P2down is True:
        if player2.y + player2.height < wh and (player2.y + player2.height) + 5 < wh:
            player2.y +=5
        elif player2.y + player2.height < wh and (player2.y + player2.height) + 5 > wh:
            player2.y = wh - player2.height

# function for the ball
def ball_ai():
    global ball, x_speed, y_speed, wallbz, playerbz, player1, player2, score1, score2
    
    ball.x += x_speed   # ball move right
    ball.y += y_speed   # ball move down

    # is the ball touching the top or bottom of the screen? if so do this
    if ball.top <= 0 or ball.bottom >= wh:
        y_speed *= -1   #bounce the ball in the opasit Y directions
        wallbz.on()                  #turns on buzzer (INPORTANT COMMENT OUT IF NOT USING BREADBOARD)
       # wallbz.beep(on_time=1, off_time=1, n=1, background=False)  # makes a single beep when ball touches the wall (IMPORTANT COMMENT OUT IF NOT USING BREADBOARD)
        wallbz.off()                 # turns buzzer off (IMPORTANT COMMENT OUT IF NOT USING BREADBOARD
    
    # did the ball hit off screen to the left? give player2 a point
    if ball.left <= 0:
        score2 += 1  #add a point to player2
        ball.center = (ww /2, wh /2)       #return ball to the center
        y_speed *= random.choice((1, -1))  #send it off in a random up or down
        x_speed *= random.choice((1, -1))  #send it off in a random left or right
        
        
    # did the ball hit off screen to the right? give player 1 a point
    if ball.right >= ww:
        score1 += 1 # add a point to player1
        ball.center = (ww /2, wh /2)  # return the ball to the center
        y_speed *= random.choice((1, -1))  # send teh ball of in a random up down 
        x_speed *= random.choice((1, -1))  #send the ball of in a random left right
        

    # did the ball touch one of the players? do this
    if ball.colliderect(player1) or ball.colliderect(player2):
        x_speed *= -1  # bounce the ball backwards
        playerbz.on()                    # turns the buzzer on (IMPORATNT COMMENT OUT IF NOT USING BREADBOARD)
        #playerbz.beep(on_time=1, off_time=1, n=1, background=False)    # makes a single beep when ball touched one of the players (IMPORATNT COMMENT OUT IF NOT USING BREAD BOARD)
        playerbz.off()                   # turns the buzzer off (IMPORTANT COMMENT OUT IF NOT USING BREADBOARD)
    
##############################################################[the game]########################################################################

#main loop for the game
while True:
    
    surface.fill((0,0,0)) # makes the background black ...if u want unplayable game comment this out hehehehe
    
    #ball draw
    pygame.draw.rect(surface, (255,255,255), ball)
    
    #background draw
    pygame.draw.rect(surface, (255,255,254), (ww/2, 0, 5, 600))

    #players draw
    pygame.draw.rect(surface, (254,255,255), player1)
    pygame.draw.rect(surface, (255,254,255), player2)
    
    move1() #this is calling the function moveplayer1
    move2() #this is calling the function moveplayer2

##############################################
    font = pygame.font.Font(None, 74)        #
    text = font.render(str(score1), 1, white)#
    surface.blit(text, (150,10))             # dont quite know how but this set the font for score
    text = font.render(str(score2), 1, white)#
    surface.blit(text, (620,10))             #
##############################################
    
    ball_ai() #this is calling the function ball
    
    
    for event in GAME_EVENTS.get():   #event list since refreshing the screen
        
        if event.type == pygame.KEYDOWN:  #when key is held down on the key board
            if event.key == pygame.K_DOWN: #down arrow is held down
                P1down = True            # set "P1down" veriabl to true
            if event.key == pygame.K_UP:   # up arrow is held down
                P1up = True              # set "P1up" veriable to true
            if event.key == pygame.K_s:    # S key is held down
                P2down = True                  # sets "P2down" veriable to true
            if event.key == pygame.K_w:    # w key is held down
                P2up = True                  # sets "P2up" veriable to true
                
#####################################################comment this box out if not using twisty knobs ###############
#                                                                                                                  #
#            if p1_analog.value >= 5:     #did player 1 turn his knob up high? if so do this                       #
#                P1down = False       #set P1down verible to false                                                 #
#                P1up = True          #set P1up verible to ture                                                    #
#                                                                                                                  #
#            if p1_analog.value < 5:       #did player1 turn his knob down low ? if so do this                     #
#                P1up = False       # set P1up verible to false                                                    #
#                P1down = True      # set P1down verible to true                                                   #
#                                                                                                                  #
#            if p2_analog.value >= 5:     # did player2 turn his knob up high? if so do this                       #
#                P2down = False    # set P2down verible to false                                                   #
#                P2up = True       # set P2up verible to true                                                      #
#                                                                                                                  #
#            if p2_analog.value < 5:     #did player2 turn his knob down?  if so do this                           #
#                P2up = False     #  set P2up verible to false                                                     #
#                P2down = True    # set P2down verible to true                                                     #
#                                                                                                                  #
###################################################################################################################
                    
        if event.type == pygame.KEYUP:    # when key is no longer held down
            if event.key == pygame.K_DOWN:# no longer holding down arrow down
                P1down = False          # sets "P1down" veriable to false
            if event.key == pygame.K_UP:  # no longer holding down up arrow
                P1up = False            # sets "P1up" veriable to fasle
            if event.key == pygame.K_s:   # no longer holding s down
                P2down = False                # sets P2down veriable to false
            if event.key == pygame.K_w:   # no longer holding down w
                P2up = False                # sets P2up veriable to false
        
        if event.type == GAME_GLOBALS.QUIT: #if we click the X button in top connor of the screen

            p1_analog.close()#
            p2_analog.close()#  these are just extra protection to clean up the gpiopins when u exit the game
            wallbz.close()   #
            playerbz.close() #
            pygame.quit()                   #quit pygame
            sys.exit()                      #shutdown the window
            
    pygame.display.update() #where done here go back to "while True"