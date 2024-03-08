#Trying to create the simple game
#Aurthour - Wai Yean Hein
#Reference - From YouTube
#Note - I take reference from 'Tech with Tim' but I try to improving it so please support me
#Note - If you know the bugs please contect me.I really appriate it.
#Social - Wai Yean(Facebook),09674526141(Telegram)


import pygame
import math
from pygame import mixer
pygame.init()
screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width,screen_height))
mixer.init()
pygame.display.set_caption("First game")
walkRight = [pygame.image.load('R1.png'),pygame.image.load('R2.png'),pygame.image.load('R3.png'),pygame.image.load('R4.png'),pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'),pygame.image.load('L2.png'),pygame.image.load('L3.png'),pygame.image.load('L4.png'),pygame.image.load('L5.png'),pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png')]
music = pygame.mixer.music.load('music.mp3')
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
clock = pygame.time.Clock()
bullet_sound = pygame.mixer.Sound('Game_bullet.mp3')
hit_sound = pygame.mixer.Sound('Game_hit.mp3')
score = 0
pygame.mixer.music.play(-1)
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.JumpCount = 10
        self.walkCount = 0
        self.left = False
        self.right = False
        self.standing = True
        self.hitbox = (self.x+17,self.y + 11,29,52)
    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox = (self.x+17,self.y+11,29,52)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        self.isJump = False
        jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font_1 = pygame.font.SysFont('comicsans',10,True)
        text = font_1.render('-5',1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
                
class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing
    def draw(self,win):
        pygame.draw.circle(win,self.colour,(self.x,self.y),self.radius)
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'),pygame.image.load('R2E.png'),pygame.image.load('R3E.png'),pygame.image.load('R4E.png'),pygame.image.load('R5E.png'),pygame.image.load('R6E.png'),pygame.image.load('R7E.png'),pygame.image.load('R8E.png'),pygame.image.load('R9E.png'),pygame.image.load('R10E.png'),pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'),pygame.image.load('L2E.png'),pygame.image.load('L3E.png'),pygame.image.load('L4E.png'),pygame.image.load('L5E.png'),pygame.image.load('L6E.png'),pygame.image.load('L7E.png'),pygame.image.load('L8E.png'),pygame.image.load('L9E.png'),pygame.image.load('L10E.png'),pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.vel = 4
        self.path = [self.x,self.end]
        self.hitbox = (self.x + 17,self.y +3,31,57)
        self.health = 10
        self.visible = True
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkcount+1 >=33:
                self.walkcount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount += 1
            else:
                win.blit(self.walkLeft[self.walkcount // 3],(self.x,self.y))
                self.walkcount += 1
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0],self.hitbox[1]-20,50 - ((50/10) *(10 - self.health)),10))
            self.hitbox = (self.x + 17,self.y + 3,31,57)
            #pygame.draw.rect(win,(0,255,0),self.hitbox,2)
            self.visible = True
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
#mainloop
font = pygame.font.SysFont('comicsans',30,True)
man = player((300),(410),64,64)
globlin = enemy(100,410,64,64,450)
run = True
bullets = []
shootloop = 0
def redrawGameWindow():
    win.blit(bg,(0,0))
    text = font.render("Score :"+ str(score),1,(0,0,0))
    win.blit(text,(340,7))
    man.draw(win)
    globlin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if globlin.visible == True:
        if man.hitbox[1] < globlin.hitbox[1] + globlin.hitbox[3] and man.hitbox[3] + man.hitbox[1] > globlin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > globlin.hitbox[0] and man.hitbox[0] < globlin.hitbox[0] + globlin.hitbox[2]:
                man.hit()
                score -= 3
        for bullet in bullets:
            if bullet.y - bullet.radius < globlin.hitbox[1] + globlin.hitbox[3] and bullet.y + bullet.radius > globlin.hitbox[1]:
                if bullet.x + bullet.radius > globlin.hitbox[0] and bullet.x - bullet.radius < globlin.hitbox[0] + globlin.hitbox[2]:
                    hit_sound.play()
                    globlin.hit()
                    score +=1
                    bullets.pop(bullets.index(bullet))

            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop =0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and shootloop == 0:
        bullet_sound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 6:
            bullets.append(projectile(round(man.x + man.width // 2),round(man.y + man.height // 2),6,(0,0,0),facing))
        shootloop = 1
    if keys[pygame.K_RIGHT] and man.x < screen_width - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    if keys[pygame.K_s]:
        pass
    elif keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.right = False
        man.left = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump):
        if keys[pygame.K_UP] and man.y > man.vel:
            man.y -= man.vel
        if keys[pygame.K_DOWN] and man.y < screen_height - man.height - man.vel:
            man.y += man.vel
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
    else:
        if man.JumpCount >= -10:
            neg = 1
            if man.JumpCount < 0 :
                neg = -1
            man.y -= (man.JumpCount**2) *0.25 * neg
            man.JumpCount -= 1
        else:
            man.isJump = False
            man.JumpCount = 10
    redrawGameWindow()
pygame.quit()
