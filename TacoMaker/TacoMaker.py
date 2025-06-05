import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###

import pygame
import pygame_gui
import json
from pygame.locals import *
from sys import exit 
from random import randint
import os

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')
diretorio_fonts = os.path.join(diretorio_principal,'fonts')

ponto2_caminho = os.path.join(diretorio_sons,'ponto1.mp3')
ponto_caminho = os.path.join(diretorio_sons,'ponto2.mp3')
Rainig_taco_caminho  = os.path.join(diretorio_sons,'Chovendo_Taco.mp3')
Start_caminho  = os.path.join(diretorio_sons,'game-start-317318_[cut_1sec].mp3')
Morte_caminho  = os.path.join(diretorio_sons,'wrong-buzzer-6268.mp3')

TelaInicial_transform = pygame.image.load(os.path.join(diretorio_imagens,'TacoMainPage.png'))

esc_nome_trasform = pygame.image.load(os.path.join(diretorio_imagens,'EscNome.png'))
esc_nome = pygame.transform.scale(esc_nome_trasform,(180*5, 140*5))

TelaGame_transform = pygame.image.load(os.path.join(diretorio_imagens,'TelaGame.png'))
TelaGame = pygame.transform.scale(TelaGame_transform,(180*5, 140*5))

TelaFinal_transform = pygame.image.load(os.path.join(diretorio_imagens,'TelaFinal.png'))
TelaFinal = pygame.transform.scale(TelaFinal_transform,(180*5, 140*5))

Taco_transform = pygame.image.load(os.path.join(diretorio_imagens,'Taco.png'))
Taco_true = pygame.transform.scale(Taco_transform, (44*3.75, 29*3.75))

Tutorial_transform = pygame.image.load(os.path.join(diretorio_imagens,'Tutorial.png'))
TutorialFund = pygame.transform.scale(Tutorial_transform,(180*5, 140*5))

Ingre_trasform = pygame.image.load(os.path.join(diretorio_imagens,'Ingredientes.png'))

fontePixel = os.path.join(diretorio_fonts,'PressStart2P.ttf')

arquivo_ranking = os.path.join(diretorio_principal, 'ranking.txt')

pygame.init()

ponto2 = pygame.mixer.Sound(ponto2_caminho)
ponto = pygame.mixer.Sound(ponto_caminho)
Rainig_taco = pygame.mixer.Sound(Rainig_taco_caminho)
Start = pygame.mixer.Sound(Start_caminho)
Morte = pygame.mixer.Sound(Morte_caminho)

canal1 = pygame.mixer.Channel(0)
canal2 = pygame.mixer.Channel(1)
canal3 = pygame.mixer.Channel(2)

tempo_inicial = pygame.time.get_ticks()
intervalo_subida = 1000
caveira_extra_adicionada = False
largura = 900
altura = 700
janela = pygame.display.set_mode([largura,altura])
sprite_sheet_coracao = pygame.image.load(os.path.join(diretorio_imagens,'CoracaoBril.png')).convert_alpha()
delay = 0
IngredientesRec = 10
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
Tutorial = False
loop = True
fonte = pygame.font.Font(fontePixel, 50)
fonte2 = pygame.font.Font(fontePixel, 25)
fonte4 = pygame.font.Font(fontePixel, 20)
fonte3 = pygame.font.Font(fontePixel, 38)

Se_move_f = f'Se movimente com      ou'
Se_ingre_f = f'Ingredientes         = +3 pontos'
Se_cair_f = f'Deixar cair = -1 ponto'
Se_cav_f = f'Caveira     = -1 Vida'
Se_rank_f = f'Se conseguir pontos o suficiente'
Se_rank2_f =f'entrará no Ranking'

Se_move = fonte4.render(Se_move_f, False,  (86, 8, 0))
Se_ingre = fonte4.render(Se_ingre_f, False,  (86, 8, 0))
Se_cair = fonte4.render(Se_cair_f, False,  (86, 8, 0))
Se_cav = fonte4.render(Se_cav_f, False,  (86, 8, 0))
Se_rank = fonte4.render(Se_rank_f, False,  (86, 8, 0))
Se_rank2 = fonte4.render(Se_rank2_f, False,  (86, 8, 0))


velocidade = 1

def carregar_ranking():
    if os.path.exists(arquivo_ranking):
        with open(arquivo_ranking, 'r') as f:
            return json.load(f)
    return []

def salvar_ranking(ranking):
    with open(arquivo_ranking, 'w') as f:
        json.dump(ranking, f)

def atualizar_ranking(nome, pontuacao):
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "pontuacao": pontuacao})
    ranking = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)[:5]
    salvar_ranking(ranking)

def TutorialEntrar():
    global RodarMainPage, RodarFase, Tutorial
    RodarFase = False
    RodarMainPage = False
    Tutorial = True

def VoltarMain():
    global RodarMainPage, RodarFase, Tutorial
    RodarFase = False
    RodarMainPage = True
    Tutorial = False


def ReiniciarJogo():
    global RodarMainPage, protax, protay, RodarFase, IngredientesRec, Vidas, delay, vel_alface, vel_tomate, vel_carne, vel_queijo, vel_caveira, Tutorial
    RodarMainPage = False
    Tutorial = False
    RodarFase = True
    protax = 70
    protay = 450
    Vidas = 3
    IngredientesRec = 10
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
            aumentada = pygame.transform.scale(img, (16*5, 14*5))
            self.Sprites_Ingre.append(aumentada)

        self.image = self.Sprites_Ingre[self.Tipo]
        self.rect = self.image.get_rect()
        self.rect.topleft = randint(80, 660), 40

    def update(self):
        global IngredientesRec
        self.image = self.Sprites_Ingre[int(self.Tipo)]
        self.rect.y = self.rect.y + self.velocidade

        if (self.rect.bottomleft[1] >= 560 ):
            self.rect.x = randint(80, 660)
            self.rect.y = 40
            if self.Tipo != 4:
                IngredientesRec = max(0, IngredientesRec - 1)


class TacoProta(pygame.sprite.Sprite):

    def __init__(self): 
        super().__init__()
        self.TacoSprite = [Taco_true]
        self.atual = 0
        self.image = self.TacoSprite[self.atual]
        
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (390, 480)

        hitbox_width = int(self.image_rect.width * 0.8)
        hitbox_height = int(self.image_rect.height * 0.8)
        self.rect = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.rect.center = self.image_rect.center

    def update(self):
        self.atual += 0.20
        if self.atual >= len(self.TacoSprite):
            self.atual = 0
        self.image = self.TacoSprite[int(self.atual)]

        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            if self.rect.left >= 90:
                self.rect.x -= 20
                self.image_rect.x -= 20
        if keys[K_d] or keys[K_RIGHT]:
            if self.rect.right <= 750:
                self.rect.x += 20
                self.image_rect.x += 20
    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)

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

Sprite_Tela.add(MainPageTaco)

canal1.play(Rainig_taco, loops=-1)
canal1.set_volume(0.2)

while RodarJogo:

    while Tutorial:
        janela.blit(TutorialFund, (0,0))
        janela.blit(Se_move, (145, 200))
        janela.blit(Se_ingre, (145, 280))
        janela.blit(Se_cair, (145, 330))
        janela.blit(Se_cav, (145, 400))
        janela.blit(Se_rank, (145, 450))
        janela.blit(Se_rank2, (145, 475))


        for events in pygame.event.get():
                if events.type == QUIT:
                    pygame.quit()
                    exit()
                if events.type == KEYDOWN:
                    if events.key == K_ESCAPE:
                        VoltarMain()

        pygame.display.flip()

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
                    canal2.play(ponto, loops=0)
                if events.key == K_t:
                    TutorialEntrar()

        pygame.display.flip()

    while RodarFase:

        relogio.tick(30)        
        janela.blit(TelaGame, (0,0))
        TacoBalde.draw(janela)
        TacoBalde.update()
        pontu_formatado_tela = f'{IngredientesRec}'
        texto_pontu_tela = fonte3.render(pontu_formatado_tela, False,  (86, 8, 0))
        janela.blit(texto_pontu_tela, (676, 72))

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
                canal2.play(Start, loops=0)


        if pygame.sprite.spritecollide(TacoBalde, Sprites_Morte, True):
            Sprites_Morte.add(Ingredientes(4, vel_caveira))
            Vidas -= 1
            canal3.play(Morte, loops=0)
            canal3.set_volume(0.2)

        
        manager = pygame_gui.UIManager((largura, altura))
        input_nome = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 300), (300, 50)), manager=manager)
        input_nome.hide()
        enviar_nome = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 360), (100, 40)), text='confirmar', manager=manager)
        enviar_nome.hide()
        nome_inserido = False
        inserindo_nome = False

        if Vidas == 0:
            perdeu = True
            nome_jogador = ""
            ranking = carregar_ranking()

            if len(ranking) < 5 or IngredientesRec > ranking[-1]["pontuacao"]:
                inserindo_nome = True
                input_nome.show()
                enviar_nome.show()

            while perdeu:
                tempo_tick_inputs = relogio.tick(30) / 1000.0
                janela.blit(TelaFinal, (0, 0))

                if not inserindo_nome:
                    pontu_formatado = f'{IngredientesRec}'
                    texto_pontu = fonte.render(pontu_formatado, False, (86, 8, 0))
                    janela.blit(texto_pontu, (615, 128))

                for i, jogador in enumerate(carregar_ranking()):
                    nome_text = fonte2.render(f"{jogador['nome']} - {jogador['pontuacao']}", False, (86, 8, 0))
                    janela.blit(nome_text, (150, 260 + i * 46))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()

                    if inserindo_nome:
                        manager.process_events(event)

                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == enviar_nome:
                                nome_jogador = input_nome.get_text()
                                atualizar_ranking(nome_jogador, IngredientesRec)
                                input_nome.hide()
                                enviar_nome.hide()
                                inserindo_nome = False
                    else:
                        if event.type == KEYDOWN:
                            if event.key == K_r:
                                ReiniciarJogo()
                                perdeu = False
                            if event.key == K_ESCAPE:
                                VoltarMain()
                                perdeu = False

                if inserindo_nome:
                    janela.blit(esc_nome, (0, 0))
                    manager.update(tempo_tick_inputs)
                    manager.draw_ui(janela)

                pygame.display.update()


        pygame.display.flip()

