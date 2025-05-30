import pygame
from pygame.locals import *
from sys import exit 
from random import randint
import os

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')

Rainig_taco = os.path.join(diretorio_sons,'Chovendo_Taco.mp3')

TelaInicial_transform = pygame.image.load(os.path.join(diretorio_imagens,'TacoMainPage.png'))

TelaGame_transform = pygame.image.load(os.path.join(diretorio_imagens,'TelaGame.png'))
TelaGame = pygame.transform.scale(TelaGame_transform,(180*5, 140*5))

TelaFinal_transform = pygame.image.load(os.path.join(diretorio_imagens,'TelaFinal.png'))
TelaFinal = pygame.transform.scale(TelaFinal_transform,(180*5, 140*5))

Taco_transform = pygame.image.load(os.path.join(diretorio_imagens,'Taco.png'))

Ingre_trasform = pygame.image.load(os.path.join(diretorio_imagens,'Ingredientes.png'))

pygame.init()

tempo_inicial = pygame.time.get_ticks()
intervalo_subida = 1000
caveira_extra_adicionada = False
largura = 900
altura = 700
janela = pygame.display.set_mode([largura,altura])
sprite_sheet_coracao = pygame.image.load(os.path.join(diretorio_imagens,'CoracaoBril.png')).convert_alpha()
delay = 0
IngredientesRec = 0
Vidas = 3
vel_alface = 2.0
vel_tomate = 2.0
vel_carne = 2.0
vel_queijo = 2.0
vel_caveira = 4.0
vel_maxima = 15.0
pygame.display.set_caption('TacoMaker')
relogio = pygame.time.Clock()
RodarJogo = True
RodarFase = False
RodarMainPage = True
loop = True
fonte = pygame.font.SysFont('Times New Roman', 80, True, True)
velocidade = 1

def VoltarMain():
    global RodarMainPage, RodarFase
    RodarFase = False
    RodarMainPage = True

def ReiniciarJogo():
    global RodarMainPage, protax, protay, RodarFase, IngredientesRec, Vidas, delay, vel_alface, vel_tomate, vel_carne, vel_queijo, vel_caveira
    RodarMainPage = False
    RodarFase = True
    protax = 70
    protay = 450
    Vidas = 3
    IngredientesRec = 0
    delay = 1
    vel_alface = 2.0
    vel_tomate = 2.0
    vel_carne = 2.0
    vel_queijo = 2.0
    vel_caveira = 4.0
    Sprite_coracao.add(corasao3)
    Sprite_coracao.add(corasao2)

    Sprites_Al.empty()
    Sprites_To.empty()
    Sprites_Car.empty()
    Sprites_Que.empty()
    Sprites_Morte.empty()

    global Alface, Tomate, Carne, Queijo, Caveira
    Alface = Ingredientes(0, vel_alface)
    Tomate = Ingredientes(2, vel_tomate)
    Carne = Ingredientes(1, vel_carne)
    Queijo = Ingredientes(3, vel_queijo)
    Caveira = Ingredientes(4, vel_caveira)
    Sprites_Al.add(Alface)
    Sprites_To.add(Tomate)
    Sprites_Car.add(Carne)
    Sprites_Que.add(Queijo)
    Sprites_Morte.add(Caveira)
    
    global caveira_extra_adicionada
    caveira_extra_adicionada = False

class Ingredientes(pygame.sprite.Sprite):

    def __init__(self, Tipo, velocidade):
        self.Tipo = Tipo
        self.velocidade = velocidade

        pygame.sprite.Sprite.__init__(self)

        self.Sprites_Ingre = []

        for i in range(5):
            img = Ingre_trasform.subsurface((i * 16,0),(16,14))
            self.Sprites_Ingre.append(img)

        self.image = self.Sprites_Ingre[self.Tipo]
        self.image = pygame.transform.scale(self.image, (16*5, 14*5))
        self.rect = self.image.get_rect()
        self.rect.topleft = randint(80, 660), 40

    def update(self):
        global IngredientesRec
        self.image = self.Sprites_Ingre[int(self.Tipo)]
        self.image = pygame.transform.scale(self.image, (16*5, 14*5))
        self.rect.y = self.rect.y + self.velocidade

        if (self.rect.bottomleft[1] >= 560 ):
            self.rect.x = randint(80, 660)
            self.rect.y = 40
            IngredientesRec = IngredientesRec - 1

class TacoProta(pygame.sprite.Sprite):

    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.TacoSprite = []
        self.TacoSprite.append(Taco_transform)

        self.atual = 0
        self.image = self.TacoSprite[self.atual]
        self.image = pygame.transform.scale(self.image, (44*3.75, 29*3.75))
        visual_rect = self.image.get_rect()
        visual_center = visual_rect.center

        hitbox_width = int(visual_rect.width * 0.80)
        hitbox_height = int(visual_rect.height * 0.80)

        self.rect = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.rect.center = visual_center
        self.rect.topleft = 390, 480

    def update(self):        
        self.atual = self.atual + 0.20
        if self.atual >= len(self.TacoSprite):
            self.atual = 0
        self.image = self.TacoSprite[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (44*3.75, 29*3.75))


        if pygame.key.get_pressed()[K_a]:
            if (self.rect.x >= 90 ):
                self.rect.x = self.rect.x - 20
        if pygame.key.get_pressed()[K_d]:
            if (self.rect.x < 650):
                self.rect.x = self.rect.x + 20

class Coracao(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.Sprite_coracao = []

        for i in range(5):
            img = sprite_sheet_coracao.subsurface((i * 14,0),(14,13))
            self.Sprite_coracao.append(img)

        self.sprite_atual = 0
        self.image = self.Sprite_coracao[self.sprite_atual]
        self.image = pygame.transform.scale(self.image, (14*2.5, 13*2.5))
        self.rect = self.image.get_rect()
        self.rect.topleft = 700, 597

    def update(self):
        self.sprite_atual = self.sprite_atual + 0.20
        if self.sprite_atual >= len(self.Sprite_coracao):
            self.sprite_atual = 0

        self.image = self.Sprite_coracao[int(self.sprite_atual)]
        self.image = pygame.transform.scale(self.image, (14*2.5, 13*2.5))

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
Sprites_Que = pygame.sprite.Group()
Sprites_Morte = pygame.sprite.Group()
Sprite_coracao = pygame.sprite.Group()

Alface = Ingredientes(0, vel_alface)
Carne = Ingredientes(1, vel_carne)
Tomate = Ingredientes(2, vel_tomate)
Queijo = Ingredientes(3, vel_queijo)
Caveira = Ingredientes(4, vel_caveira)

TacoBalde = TacoProta()
MainPageTaco = MainPage()
corasao1 = Coracao()
corasao2 = Coracao()
corasao3 = Coracao()

corasao2.rect.topleft = 740, 597
corasao3.rect.topleft = 780, 597
Sprites_Al.add(Alface)
Sprites_To.add(Tomate)
Sprites_Car.add(Carne)
Sprites_Que.add(Queijo)
Sprites_Morte.add(Caveira)
Sprite_coracao.add(corasao1)
Sprite_coracao.add(corasao2)
Sprite_coracao.add(corasao3)

Sprites_Geral.add(TacoBalde)
Sprite_Tela.add(MainPageTaco)


while RodarJogo:
    if RodarMainPage:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(Rainig_taco)
        pygame.mixer.music.play(-1)

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

        if Vidas < 3:
            Sprite_coracao.remove(corasao3)
        if Vidas < 2:
            Sprite_coracao.remove(corasao2)
            
        Sprite_coracao.draw(janela)
        Sprite_coracao.update()

        Sprites_Al.draw(janela)
        Sprites_Al.update()

        if delay > 60:
            Sprites_To.draw(janela)
            Sprites_To.update()

        if delay > 120:
            Sprites_Car.draw(janela)
            Sprites_Car.update()

        if delay > 180:
            Sprites_Que.draw(janela)
            Sprites_Que.update()
        
        if delay > 240:
            Sprites_Morte.draw(janela)
            Sprites_Morte.update()
        if vel_tomate >= vel_maxima and not caveira_extra_adicionada:
            nova_caveira = Ingredientes(4, vel_caveira)
            Sprites_Morte.add(nova_caveira)
            caveira_extra_adicionada = True

        delay = delay + 1

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_inicial > intervalo_subida:
            incremento = 0.2

            if vel_alface < vel_maxima:
                vel_alface += incremento
                Alface.velocidade = vel_alface
            if vel_tomate < vel_maxima:
                vel_tomate += incremento
                Tomate.velocidade = vel_tomate
            if vel_carne < vel_maxima:
                vel_carne += incremento
                Carne.velocidade = vel_carne
            if vel_queijo < vel_maxima:
                vel_queijo += incremento
                Queijo.velocidade = vel_queijo
            if vel_caveira < vel_maxima + 2:
                vel_caveira += incremento
                Caveira.velocidade = vel_caveira
            tempo_inicial = tempo_atual

        print(f"Velocidade aumentada: {Alface.velocidade}")

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()


        ingredientes_info = [
            (Sprites_Al, 0),
            (Sprites_To, 2),
            (Sprites_Car, 1),
            (Sprites_Que, 3)
        ]

        for grupo, tipo in ingredientes_info:
            if pygame.sprite.spritecollide(TacoBalde, grupo, True):
                if tipo == 0:
                    grupo.add(Ingredientes(tipo, vel_alface))
                elif tipo == 1:
                    grupo.add(Ingredientes(tipo, vel_carne))
                elif tipo == 2:
                    grupo.add(Ingredientes(tipo, vel_tomate))
                elif tipo == 3:
                    grupo.add(Ingredientes(tipo, vel_queijo))
                IngredientesRec += 3

        if pygame.sprite.spritecollide(TacoBalde, Sprites_Morte, True):
            Sprites_Morte.add(Ingredientes(4, vel_caveira))
            Vidas -= 1

        if Vidas == 0:
            perdeu = True
            while perdeu:
                janela.blit(TelaFinal, (0,0))
                pontu_formatado = f'{IngredientesRec}'
                pontu_formatado_Novamente = fonte.render(pontu_formatado, False, (86, 8, 0))
                janela.blit(pontu_formatado_Novamente, (615, 97))

                pygame.mixer.music.stop()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            ReiniciarJogo()
                            perdeu = False
                        if event.key == K_ESCAPE:
                            VoltarMain()
                            perdeu = False

                pygame.display.update()

        pygame.display.flip()

