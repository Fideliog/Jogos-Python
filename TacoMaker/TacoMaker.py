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

Ingre_trasform = pygame.image.load(os.path.join(diretorio_imagens,'Ingredientes.png'))


pygame.init()

largura = 900
altura = 700
janela = pygame.display.set_mode([largura,altura])
delay = 0

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
    global RodarMainPage, protax, protay, RodarFase
    RodarMainPage = False
    RodarFase = True
    protax = 70
    protay = 450

class Ingredientes(pygame.sprite.Sprite):

    def __init__(self, Tipo):
        self.Tipo = Tipo

        pygame.sprite.Sprite.__init__(self)

        self.Sprites_Ingre = []
        
        for i in range(3):
            img = Ingre_trasform.subsurface((i * 21,0),(21,17))
            self.Sprites_Ingre.append(img)

        self.image = self.Sprites_Ingre[self.Tipo]
        self.image = pygame.transform.scale(self.image, (21*5, 17*5))
        self.rect = self.image.get_rect()
        self.rect.topleft = randint(80, 660), 40


    def update(self):
        self.image = self.Sprites_Ingre[int(self.Tipo)]
        self.image = pygame.transform.scale(self.image, (21*5, 17*5))
        self.velocidade = 5
        self.rect.y = self.rect.y + self.velocidade

        if (self.rect.bottomleft[1] >= 560 ):
            self.rect.x = randint(80, 660)
            self.rect.y = 40

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
        self.sprite_atual = self.sprite_atual + 0.15
        if self.sprite_atual >= len(self.Sprite_TelaInicial):
            self.sprite_atual = 0

        self.image = self.Sprite_TelaInicial[int(self.sprite_atual)]
        self.image = pygame.transform.scale(self.image, (180*5, 140*5))

Sprites_Geral = pygame.sprite.Group()
Sprite_Tela = pygame.sprite.Group()
Sprites_Al = pygame.sprite.Group()
Sprites_Car = pygame.sprite.Group()
Sprites_To = pygame.sprite.Group()

Alface = Ingredientes(0)
Carne = Ingredientes(1)
Tomate = Ingredientes(2)
TacoBalde = TacoProta()
MainPageTaco = MainPage()

Sprites_Al.add(Alface)
Sprites_To.add(Tomate)
Sprites_Car.add(Carne)

Sprites_Geral.add(TacoBalde)
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
        Sprites_Geral.draw(janela)
        Sprites_Geral.update()
        
        Sprites_Al.draw(janela)
        Sprites_Al.update()

        if delay > 30:
            Sprites_To.draw(janela)
            Sprites_To.update()

        if delay > 60:
            Sprites_Car.draw(janela)
            Sprites_Car.update()

        delay = delay + 1

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.sprite.spritecollide(TacoBalde, Sprites_Al, True):
            Alface = Ingredientes(0)
            Sprites_Al.add(Alface)
            Sprites_Al.draw(janela)
            Sprites_Al.update()
            
        if pygame.sprite.spritecollide(TacoBalde, Sprites_To, True):
            Tomate = Ingredientes(2)
            Sprites_To.add(Tomate)
            Sprites_To.draw(janela)
            Sprites_To.update()
            
        if pygame.sprite.spritecollide(TacoBalde, Sprites_Car, True):
            Carne = Ingredientes(1)
            Sprites_Car.add(Carne)
            Sprites_Car.draw(janela)
            Sprites_Car.update()

        pygame.display.flip()

