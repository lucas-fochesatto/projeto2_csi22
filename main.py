# Código para refatoração - Viagem Espacial

import pygame
import random
from abc import ABC, abstractmethod

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

class GameObject(ABC):
    def __init__(self, image, x, y, velocidade):
        self.image = image
        self.x = x
        self.y = y
        self.velocidade = velocidade
    # __init__()

    @abstractmethod
    def update(self):
        pass
    # update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    # draw()
# GameObject:

class Player(GameObject):
    """
    Classe Jogador
    """
    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        super().__init__(player_fig, x, y, 0)
    # __init__()

    def update(self):
        self.x = self.x + self.velocidade
    # update()

    def bateu_lateral(self):
        return self.x > 760 - 92 or self.x < 40 + 5
    # bateu_lateral()
# Player:

class Hazard(GameObject):

    def __init__(self, img, x, y, velocidade):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.largura = 130
        self.altura = 130
        super().__init__(hazard_fig, x, y, velocidade)
    # __init__()

    def update(self):
        self.y = self.y + self.velocidade
    # update()

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
# Hazard:

class GameState(ABC):
    """
    Classe base (abstrata) do padrão State.
    """
    def __init__(self, game):
        self.game = game
    # __init__()

    @abstractmethod
    def handle_events(self, events):
        pass
    # handle_events()

    @abstractmethod
    def update(self, dt):
        pass
    # update()

    @abstractmethod
    def draw(self, screen):
        pass
    # draw()
# GameState:

class MenuState(GameState):
    """
    Tela inicial: aguarda o jogador iniciar a partida.
    """
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.mudar_estado(PlayingState(self.game))
    # handle_events()

    def update(self, dt):
        pass
    # update()

    def draw(self, screen):
        self.game.background.draw(screen)
        self._blit_centralizado(screen, self.game.texto_titulo, 180)
        self._blit_centralizado(screen, self.game.texto_menu, 350)
    # draw()

    def _blit_centralizado(self, screen, texto, y):
        x = (self.game.width - texto.get_width()) / 2
        screen.blit(texto, (x, y))
    # _blit_centralizado()
# MenuState:

class PlayingState(GameState):
    """
    Estado de jogo: concentra toda a lógica da partida.
    """
    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.h_passou = 0

        # velocidades
        self.velocidade_background = 5
        self.velocidade_hazard = 7
        self.velocidade_descida = self.velocidade_hazard / 4 + self.velocidade_hazard

        # controle dos obstáculos
        self.hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500

        # movimento das margens/fundo
        self.movL_x = 0
        self.movL_y = 0
        self.movR_x = 740
        self.movR_y = 0

        # velocidade horizontal atual do Player (definida pelo input)
        self.mudar_x = 0

        # Criar o Player
        x = (game.width - 56) / 2
        y = game.height - 125
        self.player = Player(x, y)

        # Criar os obstáculos (Hazard) em uma coleção dinâmica
        imagens_hazard = [
            "Images/nave.png",
            "Images/satelite.png",
            "Images/cometa.png",
            "Images/planeta.png",
            "Images/ameaca.png",
        ]
        self.hazards = [Hazard(img, h_x, h_y, self.velocidade_descida) for img in imagens_hazard]
    # __init__()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.mudar_x = -3
                if event.key == pygame.K_RIGHT:
                    self.mudar_x = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.mudar_x = 0
    # handle_events()

    def update(self, dt):
        # movimento do fundo
        self.movL_y = self.movL_y + self.velocidade_background
        self.movR_y = self.movR_y + self.velocidade_background

        # movimento do Player
        self.player.velocidade = self.mudar_x
        self.player.update()

        # bater na lateral encerra a partida
        if self.player.bateu_lateral():
            self.game.mudar_estado(GameOverState(self.game, self.score))
            return

        # movimento do hazard ativo
        hazard = self.hazards[self.hzrd]
        hazard.update()

        # reposiciona o hazard e atualiza o placar
        if hazard.y > self.game.height:
            self.hzrd = random.randint(0, 4)
            hazard = self.hazards[self.hzrd]
            hazard.reposicionar()
            self.h_passou = self.h_passou + 1
            self.score = self.h_passou * 10

        # colisão com o hazard encerra a partida
        if hazard.colidiu_com(self.player):
            self.game.mudar_estado(GameOverState(self.game, self.score))
            return
    # update()

    def draw(self, screen):
        self.game.background.move(screen, self.movL_x, self.movL_y, self.movR_x, self.movR_y)
        self.player.draw(screen)
        self.hazards[self.hzrd].draw(screen)
        self._desenhar_placar(screen)
    # draw()

    def _desenhar_placar(self, screen):
        passou = self.game.fonte_placar.render("Passou: " + str(self.h_passou), True, (255, 255, 128))
        score = self.game.fonte_placar.render("Score: " + str(self.score), True, (253, 231, 32))
        screen.blit(passou, (0, 50))
        screen.blit(score, (0, 100))
    # _desenhar_placar()
# PlayingState:

class GameOverState(GameState):
    """
    Tela de fim de jogo: mostra o placar e aguarda voltar ao menu.
    """
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.texto_score = game.fonte_media.render("Score: " + str(score), True, (253, 231, 32))
    # __init__()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game.mudar_estado(MenuState(self.game))
    # handle_events()

    def update(self, dt):
        pass
    # update()

    def draw(self, screen):
        self.game.background.draw(screen)
        self._blit_centralizado(screen, self.game.texto_perdeu, 180)
        self._blit_centralizado(screen, self.texto_score, 320)
        self._blit_centralizado(screen, self.game.texto_continuar, 420)
    # draw()

    def _blit_centralizado(self, screen, texto, y):
        x = (self.game.width - texto.get_width()) / 2
        screen.blit(texto, (x, y))
    # _blit_centralizado()
# GameOverState:

class Game:
    """
    Contexto do padrão State: mantém o estado atual e roda o laço principal.
    """
    width = 800
    height = 600

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
        self.fonte_grande = pygame.font.Font("Fonts/Fonte4.ttf", 100)
        self.fonte_media = pygame.font.Font("Fonts/Fonte4.ttf", 40)
        self.fonte_placar = pygame.font.SysFont(None, 35)

        # textos pré-renderizados compartilhados entre os estados
        self.texto_titulo = self.fonte_media.render("VIAGEM ESPACIAL", True, (255, 255, 255))
        self.texto_menu = self.fonte_media.render("APERTE ESPACO PARA JOGAR", True, (255, 255, 255))
        self.texto_perdeu = self.fonte_grande.render("GAME OVER!", True, (255, 0, 0))
        self.texto_continuar = self.fonte_media.render("APERTE ESPACO PARA O MENU", True, (255, 255, 255))

        # plano de fundo compartilhado
        self.background = Background()

        # estado inicial
        self.run = True
        self.estado = MenuState(self)

    # init()

    def mudar_estado(self, estado):
        self.estado = estado
    # mudar_estado()

    def loop(self):
        """
        Laço principal: delega tudo ao estado atual (sem recursão, sem sleep).
        """
        clock = pygame.time.Clock()
        dt = 16

        while self.run:
            clock.tick(1000 / dt)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.run = False

            self.estado.handle_events(events)
            self.estado.update(dt)
            self.estado.draw(self.screen)

            pygame.display.update()

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