import pygame
from pygame.locals import *
from sys import exit 
from random import randint

pygame.init()

largura = 800
altura = 600
janela = pygame.display.set_mode([largura,altura])
fonte = pygame.font.SysFont('Times New Roman', 40, True, True)
pygame.display.set_caption('Jogo da Cobrinha')

relogio = pygame.time.Clock()

comprimento = 3
Pontuacao = 0
loop = True
x = randint(50 , 750)
y = randint(50, 550)
px = largura/2
py = altura/2
Lista_azul_corrente = []
x_controle = 20
y_controle = 0
morreu = False

def Alonga_corrente(Lista_azul_corrente):
    for XisEYpisulon in Lista_azul_corrente:
        pygame.draw.rect(janela, (0,0,255), (XisEYpisulon[0], XisEYpisulon[1], 50, 50))

def ReiniciarJogo():
    global Pontuacao, comprimento, py, px, Lista_azul_cabes, Lista_azul_corrente, morreu, x, y
    Pontuacao = 0
    comprimento = 3
    px = largura/2
    py = altura/2
    Lista_azul_corrente = []
    Lista_azul_cabes = []
    morreu = False
    x = randint(50 , 750)
    y = randint(50, 550)

while True:
    relogio.tick(30)
    janela.fill([0,0,0])
    
    texto_formatado = f'Pontos: {Pontuacao}'
    texto_formatado_Novamente = fonte.render(texto_formatado, False, (123,53,98))
    texto_game_over = fonte.render('Aperte R para reiniciar', False, (123,53,98))


    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()

        
        if events.type == pygame.KEYDOWN:
            if events.key == K_a:
                if (x_controle == 20):
                    pass
                else:
                    x_controle = -20
                    y_controle = 0
            if events.key == K_d:
                if (x_controle >= 0):
                    x_controle = 20
                    y_controle = 0
            if events.key == K_w:
                if (y_controle <= 0):
                    y_controle = -20
                    x_controle = 0
            if events.key == K_s:
                if (y_controle >= 0):
                    y_controle = 20
                    x_controle = 0

    if (px > largura):
        px = 0
    
    if (px < 0):
        px = largura

    px = px + x_controle

    if (py < 0):
        py = altura

    if (py > altura):
        py = 0

    py = py + y_controle

    '''
    if pygame.key.get_pressed()[K_a]:
        px = px - 15
    if pygame.key.get_pressed()[K_d]:
        px = px + 15
    if pygame.key.get_pressed()[K_w]:
        py = py - 15
    if pygame.key.get_pressed()[K_s]:
        py = py + 15
    '''
        
    Ret_Azul = pygame.draw.rect(janela, (0,0,255), (px, py, 50, 50))
    
    Ret_Vermelho = pygame.draw.rect(janela, (255,0,0), (x, y, 50, 50))

    if Ret_Azul.colliderect(Ret_Vermelho):
        print('Colidiu')
        x = randint(20 , (largura - 50))
        y = randint(20, (altura - 50))
        Pontuacao = Pontuacao + 1
        comprimento = comprimento + 1
    
    Lista_azul_cabes = []
    Lista_azul_cabes.append(px)
    Lista_azul_cabes.append(py)

    Lista_azul_corrente.append(Lista_azul_cabes)

    if Lista_azul_corrente.count(Lista_azul_cabes) > 1:
        morreu = True
        while morreu:
            janela.fill((255,255,255))
            janela.blit(texto_game_over, (300, 350))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        ReiniciarJogo()

            pygame.display.update()

    
    Alonga_corrente(Lista_azul_corrente)

    if len(Lista_azul_corrente) > comprimento:
        del Lista_azul_corrente[0]

    janela.blit(texto_formatado_Novamente, (600, 50))
    '''
    if ( y >= altura): 
        y = 0
    
    y = y + 1

    if ( x >= largura): 
        x = 0
    
    x = x + 1

    pygame.draw.circle(janela, (0,234,0), (50, 50), 50)
    pygame.draw.line(janela, (34,86,65), (0, 0), (800,600), 10)
    '''

    pygame.display.update()