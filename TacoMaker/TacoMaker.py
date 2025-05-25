import pygame
from pygame.locals import *
from sys import exit 
from random import randint
import os

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')

TelaInicial_transform = pygame.image.load(os.path.join(diretorio_imagens,'TacoMainPage.png'))

TelaGame_transform = pygame.image.load(os.path.join(diretorio_imagens,'TelaGame.png'))
TelaGame = pygame.transform.scale(TelaGame_transform,(180*5, 140*5))

Taco_transform = pygame.image.load(os.path.join(diretorio_imagens,'Taco.png'))

pygame.init()

largura = 900
altura = 700
janela = pygame.display.set_mode([largura,altura])

pygame.display.set_caption('TacoMaker')
relogio = pygame.time.Clock()
RodarJogo = True
RodarFase = False
RodarMainPage = True
loop = True

def VoltarMain():
    global RodarMainPage, RodarFase
    RodarFase = False
    RodarMainPage = True

def ReiniciarJogo():
    global ganhou, RodarMainPage, protax, protay, RodarFase, perdeu
    RodarMainPage = False
    RodarFase = True
    ganhou = False
    perdeu = False
    protax = 70
    protay = 450

class TacoProta(pygame.sprite.Sprite):

    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.TacoSprite = []
        self.TacoSprite.append(Taco_transform)

        self.atual = 0
        self.image = self.TacoSprite[self.atual]
        self.image = pygame.transform.scale(self.image, (44*4, 29*4))
        self.rect = self.image.get_rect()
        self.rect.topleft = 390, 450

    def update(self):
        self.atual = self.atual + 0.20
        if self.atual >= len(self.TacoSprite):
            self.atual = 0
        self.image = self.TacoSprite[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (44*4, 29*4))

        if pygame.key.get_pressed()[K_a]:
            if (self.rect.x >= 90 ):
                self.rect.x = self.rect.x - 20
        if pygame.key.get_pressed()[K_d]:
            if (self.rect.x < 650):
                self.rect.x = self.rect.x + 20


class MainPage(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.Sprite_TelaInicial = []

        for i in range(5):
            img = TelaInicial_transform.subsurface((i * 180,0),(180,140))
            self.Sprite_TelaInicial.append(img)

        self.sprite_atual = 0
        self.image = self.Sprite_TelaInicial[self.sprite_atual]
        self.image = pygame.transform.scale(self.image, (180*5, 140*5))
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0

    def update(self):
        self.sprite_atual = self.sprite_atual + 0.20
        if self.sprite_atual >= len(self.Sprite_TelaInicial):
            self.sprite_atual = 0

        self.image = self.Sprite_TelaInicial[int(self.sprite_atual)]
        self.image = pygame.transform.scale(self.image, (180*5, 140*5))

Sprites_prota = pygame.sprite.Group()
Sprite_Tela = pygame.sprite.Group()

TacoBalde = TacoProta()
MainPageTaco = MainPage()

Sprites_prota.add(TacoBalde)
Sprite_Tela.add(MainPageTaco)


while RodarJogo:

    while RodarMainPage:
        relogio.tick(30)

        Sprite_Tela.draw(janela)
        Sprite_Tela.update()

        for events in pygame.event.get():
            if events.type == QUIT:
                pygame.quit()
                exit()
            if events.type == KEYDOWN:
                if events.key == K_SPACE:
                    ReiniciarJogo()

        
        pygame.display.flip()


    while RodarFase:

        relogio.tick(30)        
        janela.blit(TelaGame, (0,0))
        Sprites_prota.draw(janela)
        Sprites_prota.update()
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()

