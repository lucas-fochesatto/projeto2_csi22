# Código para refatoração - Viagem Espacial

import pygame
import random
import time

class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """
    image = None
    margin_left = None
    margin_right = None

    def __init__(self):

        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 600))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 600))
        self.margin_right = margin_right_fig
    # __init__()

    def update(self, dt):
        pass
    # update()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        screen.blit(self.margin_left, (0, 0))
        screen.blit(self.margin_right, (740, 0))
    # draw()

    # Define posições do Plano de Fundo para criar o movimento
    def move (self, screen, movL_x, movL_y, movR_x, movR_y):

        # deslocamento contínuo via aritmética modular (2 ladrilhos por camada)
        altura_fundo = self.image.get_height()
        desloc_fundo = movL_y % altura_fundo
        screen.blit(self.image, (movL_x, desloc_fundo))
        screen.blit(self.image, (movL_x, desloc_fundo - altura_fundo))

        altura_margem_esq = self.margin_left.get_height()
        desloc_margem_esq = movL_y % altura_margem_esq
        screen.blit(self.margin_left, (movL_x, desloc_margem_esq))
        screen.blit(self.margin_left, (movL_x, desloc_margem_esq - altura_margem_esq))

        altura_margem_dir = self.margin_right.get_height()
        desloc_margem_dir = movR_y % altura_margem_dir
        screen.blit(self.margin_right, (movR_x, desloc_margem_dir))
        screen.blit(self.margin_right, (movR_x, desloc_margem_dir - altura_margem_dir))
    # move()
# Background:

class Player:
    """
    Classe Jogador
    """
    image = None
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y
    # __init__()

    def mover(self, mudar_x):
        self.x = self.x + mudar_x
    # mover()

    def bateu_lateral(self):
        return self.x > 760 - 92 or self.x < 40 + 5
    # bateu_lateral()

    # Desenhar Player
    def draw (self, screen):
        screen.blit(self.image, (self.x, self.y))
    #draw()
# Player:

class Hazard:

    image = None
    x = None
    y = None
    largura = None
    altura = None

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y
        self.largura = 130
        self.altura = 130
    # __init__()

    def mover(self, mudar_y):
        self.y = self.y + mudar_y
    # mover()

    def reposicionar(self):
        self.y = 0 - self.altura
        self.x = random.randrange(125, 650 - self.altura)
    # reposicionar()

    def colidiu_com(self, player):
        if player.y < self.y + self.altura:
            if player.x > self.x or player.x > self.x - 56:
                if player.x < self.x + self.largura or player.x < self.x - 56:
                    return True
        return False
    # colidiu_com()

    # Desenhar Hazard
    def draw (self, screen):
        screen.blit(self.image, (self.x, self.y))
    #draw()
# Hazard:

class Game:
    screen = None
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None
    player = None
    hazard_1 = hazard_2 = hazard_3 = hazard_4 = hazard_5 = None
    render_text_bateulateral = None
    render_text_perdeu = None

    # movimento do Player
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    mudar_x = 0.0


    def __init__(self, size, fullscreen):

        """
        Função que inicializa o pygame, define a resolução da tela,
        caption, e desabilita o mouse.
        """

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))  # tamanho da tela
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Viagem Espacial')

        # fontes
        my_font = pygame.font.Font("Fonts/Fonte4.ttf", 100)

        # Mensagens para o jogador
        self.render_text_bateulateral = my_font.render("COLISÃO!", 0,(255, 255, 255))  # ("texto", opaco/transparente 0/1, cor do texto)
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0))  # ("texto, opaco/transparente 0/1, cor do texto)

    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            # se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:
                # se clicar na seta da esquerda, anda 3 para a esquerda no eixo x
                if event.key == self.ESQUERDA:
                    self.mudar_x = -3
                # se clicar na seta da direita, anda 3 para a direita no eixo x
                if event.key == self.DIREITA:
                    self.mudar_x = 3

            # se soltar qualquer tecla, não faz nada
            if event.type == pygame.KEYUP:
                if event.key == self.ESQUERDA or event.key == self.DIREITA:
                    self.mudar_x = 0

    # handle_events()

    def elements_update(self, dt):
        self.background.update(dt)
    # elements_update()

    def elements_draw(self):
        self.background.draw(self.screen)
    # elements_draw()

    # Desenha o Player
    def draw_player (self):
        self.player.draw (self.screen)
    # draw_player()

    def hazard_atual (self, hzrd):
        if hzrd == 0:
            return self.hazard_1
        elif hzrd == 1:
            return self.hazard_2
        elif hzrd == 2:
            return self.hazard_3
        elif hzrd == 3:
            return self.hazard_4
        elif hzrd == 4:
            return self.hazard_5
    # hazard_atual()

    # Desenha Hazard
    def draw_hazard (self, hzrd):
        self.hazard_atual(hzrd).draw(self.screen)
    # draw_hazard()

    # Define as posições dos objetos para criar o movimento
    def move_background (self, obj_movL_x, obj_movL_y, obj_movR_x, obj_movR_y):
        self.background.move (self.screen, obj_movL_x, obj_movL_y, obj_movR_x,obj_movR_y)
    # move_background()

    # Informa a quantidade de hazard que passaram e a Pontuação
    def score_card(self, screen, h_passou, score):
        font = pygame.font.SysFont(None, 35)
        passou = font.render("Passou: " + str(h_passou), True, (255, 255, 128))
        score = font.render("Score: " + str(score), True, (253, 231, 32))
        screen.blit(passou, (0, 50))
        screen.blit(score, (0, 100))
    #score_card()

    def loop(self):
        """
        Laço principal
        """
        score = 0
        h_passou = 0

        # variáveis para movimento de Plano de Fundo/Background
        velocidade_background = 5
        velocidade_hazard = 7

        faixaA_x = 375
        faixaA_y = 0
        hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o Plano de fundo
        self.background = Background()

        # Posicao do Player
        x = (self.width - 56) / 2
        y = self.height - 125

        # Criar o Player
        self.player = Player(x, y)

        # Criar Harzard_1
        self.hazard_1 = Hazard("Images/nave.png", h_x, h_y)

        # Criar Harzard_2
        self.hazard_2 = Hazard("Images/satelite.png", h_x, h_y)

        # Criar Harzard_3
        self.hazard_3 = Hazard("Images/cometa.png", h_x, h_y)

        # Criar Harzard_4
        self.hazard_4 = Hazard("Images/planeta.png", h_x, h_y)

        # Criar Harzard_5
        self.hazard_5 = Hazard("Images/ameaca.png", h_x, h_y)

        # Inicializamos o relogio e o dt que vai limitar o valor de FPS
        # frames por segundo do jogo
        clock = pygame.time.Clock()
        dt = 16

        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.elements_update(dt)

            # Desenha o background buffer
            self.elements_draw()

            # adiciona movimento ao background

            self.move_background (movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            self.player.mover(self.mudar_x)

            # Mostrar Player
            self.draw_player()

            # Mostrar score
            self.score_card(self.screen, h_passou, score)

            # Restrições do movimento do Player
            # Se o Player bate na lateral não é Game Over
            if self.player.bateu_lateral():
                self.screen.blit(self.render_text_bateulateral, (80, 200))
                pygame.display.update()  # atualizar a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # adicionando movimento ao hazard
            hazard = self.hazard_atual(hzrd)
            hazard.mover(velocidade_hazard / 4)
            self.draw_hazard(hzrd)
            hazard.mover(velocidade_hazard)

            # definindo onde hazard vai aparecer, recomeçando a posição do obstaculo e da faixa
            if hazard.y > self.height:
                hzrd = random.randint(0, 4)
                hazard = self.hazard_atual(hzrd)
                hazard.reposicionar()
                # determinando quantos hazard passaram e a pontuação
                h_passou = h_passou + 1
                score = h_passou * 10

            # restrições para o game over
            if hazard.colidiu_com(self.player):
                self.screen.blit(self.render_text_perdeu, (80, 200))
                pygame.display.update()
                time.sleep(3)
                self.run = False

            # atualizando a tela
            pygame.display.update()
            clock.tick(2000)

        # while self.run
    # loop()
# Game:

def main():
    # Cria o objeto game e chama o loop básico
    game = Game("resolution", "fullscreen")
    game.loop()
# main()

# Chama a função main
if __name__ == '__main__':
    main()