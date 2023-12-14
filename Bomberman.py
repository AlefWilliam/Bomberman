import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

###

import pygame
from pygame.locals import *
from sys import exit
from Modularizando import (criar_terreno,sprites_dict,)

# Inicialização do Pygame
pygame.init()

# Som do titulo
pygame.mixer.music.load("Sons/titulo.mp3")
# Volume do Jogo
pygame.mixer.music.set_volume(0.09)
# Repetir a Música
pygame.mixer.music.play(-1)

# Som da Explosão
explo = pygame.mixer.Sound("Sons/Boom.mp3")
# Volume da Explosão
pygame.mixer.Sound.set_volume(explo,0.3)
#Mouse
mouse = pygame.image.load('Telas/mouse.png')
mouse = pygame.transform.scale(mouse, [44, 50])
# Configurações da tela
largura = 900
altura = 620
verde = (47, 79, 47)
branco = (255,255,255)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('BOMBERMAN')
fundo = pygame.image.load('Telas/inicial.jpg')
fundo = pygame.transform.scale(fundo,[900,620])

# Configuração do botão iniciar
iniciargroup = pygame.sprite.Group()
iniciar = pygame.sprite.Sprite(iniciargroup)
iniciar.image = pygame.image.load('Telas/iniciar.png')
iniciar.image = pygame.transform.scale(iniciar.image,[170,40])
iniciar.rect = pygame.Rect(700,25,170,40)

# Configuração do botão jogar
jogargroup = pygame.sprite.Group()
jogar = pygame.sprite.Sprite(jogargroup)
jogar.image = pygame.image.load('Telas/Jogar.png')
jogar.image = pygame.transform.scale(jogar.image,[230,40])
jogar.rect = pygame.Rect(660,570,230,40)

# Configuração do botão regras
regras = pygame.sprite.Sprite(jogargroup)
regras.image = pygame.image.load('Telas/regras.png')
regras.image = pygame.transform.scale(regras.image,[850,450])
regras.rect = pygame.Rect(30,50,850,450)

# Configuração da tela de vitoria
vitoriagroup = pygame.sprite.Group()
vitoria = False
venceu = pygame.sprite.Sprite(vitoriagroup)
venceu.image = pygame.image.load('Telas/venceu.png')
venceu.image = pygame.transform.scale(venceu.image,[300,60])
venceu.rect = pygame.Rect(300,100,230,40)

# Configuração da tela de GAME OVER
gameOgroup = pygame.sprite.Group()
gameover = False
gameO = pygame.sprite.Sprite(gameOgroup)
gameO.image = pygame.image.load('Telas/GameOver.png')
gameO.image = pygame.transform.scale(gameO.image,[300,60])
gameO.rect = pygame.Rect(290,100,230,40)

# Configuração do botão Sair
sair = pygame.sprite.Sprite(gameOgroup,vitoriagroup)
sair.image = pygame.image.load('Telas/sair.png')
sair.image = pygame.transform.scale(sair.image,[200,40])
sair.rect = pygame.Rect(350,300,230,40)

# Relógio
tempo_intervalo = 1000  # Tempo em milissegundos (1 segundo)

TEMPO_EVENTO = pygame.USEREVENT + 1
pygame.time.set_timer(TEMPO_EVENTO, tempo_intervalo)

tempo_decorrido = 0

# Definição da classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, sprites_dict, scale_factor, initial_position):
        pygame.sprite.Sprite.__init__(self)
        # Dicionário que mapeia direções para listas de sprites
        self.sprites_dict = {direcao: [pygame.image.load(path) for path in sprites] for direcao, sprites in sprites_dict.items()}
        # Direção inicial
        self.direcao_atual = 'baixo'
        # Índice atual da animação
        self.atual = 0
        # Carregando a imagem inicial e redimensionando conforme a escala
        self.image = pygame.transform.scale(self.sprites_dict[self.direcao_atual][self.atual], scale_factor)
        # Obtendo o retângulo da imagem
        self.rect = self.image.get_rect()
        # Posição inicial
        self.rect.topleft = initial_position
        # Flag para animação
        self.animar = False
        self.tempo_decorrido = 0
        self.vivo = True

    # Método para movimentar o jogador
    def andar(self, direcao, pedras_lisas, pedregulhos):
        if direcao != self.direcao_atual:
            # Se a direção mudou, reinicia a animação
            self.atual = 1
            self.tempo_decorrido = 0
        self.animar = True

        # Atualiza a posição conforme a direção, apenas se não houver colisão
        dx, dy = 0, 0
        if direcao == 'direita':
            dx = 4
        elif direcao == 'esquerda':
            dx = -4
        elif direcao == 'cima':
            dy = -4
        elif direcao == 'baixo':
            dy = 4

        next_rect = self.rect.move(dx, dy)

        # Verifica a colisão com pedras lisas
        for pedra in pedras_lisas:
            if next_rect.colliderect(pedra.rect):
                return

        # Verifica a colisão com pedregulhos
        for pedregulho in pedregulhos:
            if next_rect.colliderect(pedregulho.rect):
                return

        if pygame.sprite.spritecollide(self, explosoes, True):
            self.morrer()

        # Se não houver colisão, atualiza a posição do jogador
        self.rect.x += dx
        self.rect.y += dy
        self.direcao_atual = direcao

    # Método para parar a animação
    def parar(self):
        self.animar = False
        # Quando o jogador para, mostra o estado 0
        self.atual = 0
        self.tempo_decorrido = 0
        self.image = pygame.transform.scale(self.sprites_dict[self.direcao_atual][int(self.atual)], self.rect.size)

    def morrer(self):
        self.vivo = False
        global gameover
        global jogo
        jogo = False
        gameover = True

    # Método para atualizar a animação
    def update(self):
        if self.animar:
            # Atualiza o índice de animação
            self.tempo_decorrido += 1
            # Altere o valor 5 para ajustar a velocidade da animação
            if self.tempo_decorrido % 5 == 0:
                self.atual = (self.atual % 4) + 1
            # Atualiza a imagem redimensionada
            self.image = pygame.transform.scale(self.sprites_dict[self.direcao_atual][int(self.atual)], self.rect.size)
        else:
            # Se não estiver animando, mostra o estado 0
            self.image = pygame.transform.scale(self.sprites_dict[self.direcao_atual][0], self.rect.size)
        #Verifica se o player foi explodido
        if pygame.sprite.spritecollide(self, explosoes, False):
            self.morrer()

class Bomba(pygame.sprite.Sprite):
    def __init__(self, sprites, cell_position):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(path) for path in sprites]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = cell_position
        self.rect.center = cell_position
        self.explodir = False
        self.tempo_decorrido = 0
        self.tempo_explosao = 50  # Ajusta o tempo da explosão a 30 frames por segundo

    def explode(self, pedregulhos):

        tamanho_celula = 45
        explosao_meio = Explosao('meio', (self.rect.topleft[0] - 5, self.rect.topleft[1] - 10), tamanho_celula)

        explosoes.add(explosao_meio)
        todas_sprites.add(explosao_meio)

        # Explosão vertical para cima
        for i in range(1, 2):
            new_position = (self.rect.topleft[0], self.rect.topleft[1] - i * tamanho_celula)
            explosao_cima = Explosao('cima', (new_position[0]-6, new_position[1] - 7), tamanho_celula)
            if not pygame.sprite.spritecollide(explosao_cima, pedras_lisas, False):
                explosoes.add(explosao_cima)
                todas_sprites.add(explosao_cima)

        # Explosão vertical para baixo
        for i in range(1, 2):
            new_position = (self.rect.topleft[0], self.rect.topleft[1] + i * tamanho_celula)
            explosao_baixo = Explosao('baixo', (new_position[0]-7, new_position[1] - 10), tamanho_celula)
            if not pygame.sprite.spritecollide(explosao_baixo, pedras_lisas, False):
                explosoes.add(explosao_baixo)
                todas_sprites.add(explosao_baixo)

        # Explosão horizontal para direita
        for i in range(1, 2):
            new_position = (self.rect.topleft[0] + i * tamanho_celula - 5, self.rect.topleft[1] - 9)
            explosao_direita = Explosao('direita', new_position, tamanho_celula)
            if not pygame.sprite.spritecollide(explosao_direita, pedras_lisas, False):
                explosoes.add(explosao_direita)
                todas_sprites.add(explosao_direita)

        # Explosão horizontal para esquerda
        for i in range(1, 2):
            new_position = (self.rect.topleft[0] - i * tamanho_celula - 5, self.rect.topleft[1] - 10)
            explosao_esquerda = Explosao('esquerda', new_position, tamanho_celula)
            if not pygame.sprite.spritecollide(explosao_esquerda, pedras_lisas, False):
                explosoes.add(explosao_esquerda)
                todas_sprites.add(explosao_esquerda)

        for pedregulho in pedregulhos.copy():
            for explosao in explosoes:
                if pygame.sprite.collide_rect(explosao, pedregulho):
                    pedregulhos.remove(pedregulho)
                    todas_sprites.remove(pedregulho)

    def update(self):
        if not self.explodir:
            self.atual = (self.atual + 0.2) % len(self.sprites)
            self.image = self.sprites[int(self.atual)]
            # Atualiza o contador de tempo
            self.tempo_decorrido += 1
            # Verifica se o tempo de explosão foi atingido
            if self.tempo_decorrido >= self.tempo_explosao:
                # Som da Explosão
                explo.play()
                self.explodir = True
                self.explode(pedregulhos)
class Explosao(pygame.sprite.Sprite):
    def __init__(self, animation_type, position, tamanho_celula):
        pygame.sprite.Sprite.__init__(self)
        self.animation_type = animation_type
        self.sprites = self.load_sprites(animation_type)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.tempo_decorrido = 0
        self.tempo_explosao = 20  # Ajusta o tempo da explosão
        self.tamanho_celula = tamanho_celula

    def load_sprites(self, animation_type):
        # Lógica para carregar sprites com base no tipo de animação
        sprite_paths = []
        if animation_type == 'meio':
            sprite_paths = ['sprites/fogotodolado3.png', 'sprites/fogotodolado4.png', 'sprites/fogotodolado5.png']
        elif animation_type == 'cima':
            sprite_paths = ['sprites/fogocima3.png', 'sprites/fogocima4.png', 'sprites/fogocima5.png']
        elif animation_type == 'baixo':
            sprite_paths = ['sprites/fogobaixo3.png', 'sprites/fogobaixo4.png', 'sprites/fogobaixo5.png']
        elif animation_type == 'direita':
            sprite_paths = ['sprites/fogodireita3.png', 'sprites/fogodireita4.png', 'sprites/fogodireita5.png']
        elif animation_type == 'esquerda':
            sprite_paths = ['sprites/fogoesquerda3.png', 'sprites/fogoesquerda4.png', 'sprites/fogoesquerda5.png']
        elif animation_type == 'horizontal':
            sprite_paths = ['sprites/fogohorizontal3.png', 'sprites/fogohorizontal4.png', 'sprites/fogohorizontal5.png']
        elif animation_type == 'vertical':
            sprite_paths = ['sprites/fogovertical3.png', 'sprites/fogovertical4.png', 'sprites/fogovertical5.png']
        return [pygame.image.load(sprite_path) for sprite_path in sprite_paths]

    def update(self,tamanho_celula=45):
        self.tempo_decorrido += 1
        if self.tempo_decorrido >= self.tempo_explosao:
            todas_sprites.remove(self)
            explosoes.remove(self)
        else:
            self.atual = (self.atual + 0.5) % len(self.sprites)
            temp_surface = pygame.transform.scale(self.sprites[int(self.atual)],(self.tamanho_celula, self.tamanho_celula))
            # Converte para melhorar o desempenho
            self.image = temp_surface.convert()
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, sprite_path, initial_position, movimento):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (43, 43))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.movimento = movimento
        self.velocidade = 1
        self.esta_vivo = True
        self.tempo_desaparecer = 1

    def update(self):
        self.posicao_anterior = self.rect.topleft
        if self.esta_vivo:
            if self.movimento == 'vertical':
                self.rect.y += self.velocidade
                # Se atingir a borda inferior, muda a direção para cima
                if self.rect.bottom > altura or pygame.sprite.spritecollide(self, pedras_lisas, False) or pygame.sprite.spritecollide(self, pedregulhos, False):
                    self.velocidade = -self.velocidade
                # Se atingir a borda superior, muda a direção para baixo
                elif self.rect.top < 0 or pygame.sprite.spritecollide(self, pedras_lisas, False) or pygame.sprite.spritecollide(self, pedregulhos, False):
                    self.velocidade = -self.velocidade

            elif self.movimento == 'horizontal':
                self.rect.x += self.velocidade
                # Se atingir a borda direita, muda a direção para a esquerda
                if self.rect.right > largura or pygame.sprite.spritecollide(self, pedras_lisas,False) or pygame.sprite.spritecollide(self,pedregulhos,False):
                    self.velocidade = -self.velocidade
                # Se atingir a borda esquerda, muda a direção para a direita
                elif self.rect.left < 0 or pygame.sprite.spritecollide(self, pedras_lisas,False) or pygame.sprite.spritecollide(self,pedregulhos,False):
                    self.velocidade = -self.velocidade

            # Verifica colisões apenas na direção horizontal
            if pygame.sprite.spritecollide(self, pedras_lisas, False) or pygame.sprite.spritecollide(self, pedregulhos, False):
                self.rect.topleft = self.posicao_anterior
            # Reverte a posição anterior em caso de colisão
            if pygame.sprite.spritecollide(self, pedras_lisas, False) or pygame.sprite.spritecollide(self, pedregulhos, False):
                self.rect.topleft = self.posicao_anterior
            # Verifica se o inimigo foi explodido
            if pygame.sprite.spritecollide(self, explosoes, True):
                self.morrer()
    def morrer(self):
        global num_monstros_vivos
        self.esta_vivo = False
        self.tempo_desaparecer -= 1
        if self.tempo_desaparecer <= 0:
            self.kill()  # Remove o inimigo do grupo de sprites
            num_monstros_vivos -= 1

        # Mensagem de Vitória
        if num_monstros_vivos == 0:
            pygame.display.flip()
            global vitoria
            global jogo
            vitoria = True
            jogo = False


def mostrar_indicador_monstros():
    fonte = pygame.font.SysFont(None, 40)
    texto = fonte.render("Monstros: {}".format(num_monstros_vivos), True, (255, 255, 255))
    tela.blit(texto, (10, 10))

def mostrar_relogio():
    fonte = pygame.font.SysFont(None, 40)
    texto = fonte.render("Tempo: {}".format(tempo_decorrido), True, (255, 255, 255))
    tela.blit(texto, (720, 10))

# Instância do jogador
player = Player(sprites_dict, (30, 42), (170, 110))

# Posicionando o inimigo horizontal onde não há pedras
inimigo_horizontal = Inimigo('sprites/Inimigo.png', (695, 470), 'horizontal')
inimigo_horizontal2 = Inimigo('sprites/Inimigo.png', (650, 110), 'horizontal')
inimigo_vertical = Inimigo('sprites/Inimigo.png', (340, 335), 'vertical')
inimigo_vertical2 = Inimigo('sprites/Inimigo.png', (520, 245), 'vertical')

rect_iniciar = pygame.Rect(700, 25, 170, 40)
rect_jogar = pygame.Rect(660, 570, 230, 40)

# Grupo de Sprites
pedras_lisas = pygame.sprite.Group()
pedregulhos = pygame.sprite.Group()
bombas = pygame.sprite.Group()
explosoes = pygame.sprite.Group()
todas_sprites = pygame.sprite.Group()
num_monstros_vivos = 4

# Criando Terreno
criar_terreno(pedras_lisas,pedregulhos)

# Adiciona os sprites ao grupo todas_sprites
todas_sprites.add(player,pedras_lisas,pedregulhos,inimigo_horizontal,inimigo_horizontal2,
                  inimigo_vertical,inimigo_vertical2,bombas,explosoes)

# Verificar Bombas colocadas
bombas_colocadas = set()

# Configuração do relógio
relogio = pygame.time.Clock()

# Tela inicial
comeco = True
while comeco == True:
    tela.fill((0,0,0))
    tela.blit(fundo, (0, 0))
    iniciargroup.draw(tela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0] and iniciar.rect.collidepoint(pygame.mouse.get_pos()):
            ini = True
            comeco = False
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Verifica se o mouse está sobre o botão "Iniciar" e "Jogar"
    if rect_iniciar.collidepoint(mouse_x, mouse_y) or rect_jogar.collidepoint(mouse_x, mouse_y):
        # Desenha a imagem do cursor personalizado
        tela.blit(mouse, (mouse_x-16, mouse_y-25))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)

    pygame.display.flip()

# Regras e jogabilidade
while ini == True:
    tela.fill((0,0,0))
    jogargroup.draw(tela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0] and jogar.rect.collidepoint(pygame.mouse.get_pos()):
            ini = False
            jogo = True
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Verifica se o mouse está sobre o botão iniciar e jogar
    if rect_iniciar.collidepoint(mouse_x, mouse_y) or rect_jogar.collidepoint(mouse_x, mouse_y):
        # Desenha a imagem do cursor personalizado
        tela.blit(mouse, (mouse_x - 16, mouse_y - 25))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
    pygame.display.flip()

# Som do Jogo
pygame.mixer.music.load("Sons/musica.mp3")
pygame.mixer.music.play(-1)

#loop principal
while jogo == True:
    relogio.tick(30)
    tela.fill(verde)
    bombas_a_remover = set()

    #A linha isinstance(bomba, Bomba) verifica se bomba é uma instância da classe Bomba.Se for o caso, e
    # bomba.explodir também for verdadeiro, a bomba é adicionada ao conjunto bombas_a_remover
    # e sua posição (bomba.rect.x, bomba.rect.y) é removida de bombas_colocadas.
    # Essa verificação é útil para garantir que você está lidando apenas com instâncias da
    # classe Bomba em seu código, evitando possíveis erros se outros tipos de objetos estiverem
    # presentes no conjunto bombas.

    for bomba in bombas.copy():
        if isinstance(bomba, Bomba) and bomba.explodir:
            bombas_a_remover.add(bomba)
            bombas_colocadas.remove((bomba.rect.x, bomba.rect.y))
    todas_sprites.remove(bombas_a_remover)
    bombas.remove(bombas_a_remover)

    # Desenhando e atualizando os sprites
    todas_sprites.draw(tela)
    todas_sprites.update()
    mostrar_indicador_monstros()
    mostrar_relogio()

    # Atualizando a tela
    pygame.display.flip()

    # Verificação de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == TEMPO_EVENTO:
            # Ação a ser executada a cada intervalo de tempo
            tempo_decorrido += 1
            if tempo_decorrido == 300000:
                jogo = False
                gameover = True

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                player_center = player.rect.center
                # Encontrando a posição da célula em que o jogador está
                cell_x = (player_center[0] + 22) // 45 * 45  # Adicionando 22 para centralizar
                cell_y = (player_center[1] + 22) // 45 * 45  # Adicionando 22 para centralizar

                # Verificando se a posição já tem uma bomba
                if not any(bomba.rect.collidepoint(cell_x, cell_y) for bomba in bombas):
                    # Criando uma nova bomba na posição acima do jogador
                    bomba_sprites = ['sprites/bomb1.png', 'sprites/bomb2.png', 'sprites/bomb3.png', 'sprites/bomb4.png']
                    bomba = Bomba(bomba_sprites, (cell_x, cell_y))
                    bombas.add(bomba)
                    todas_sprites.add(bomba)

    # Obtendo teclas pressionadas
    comandos = pygame.key.get_pressed()

    # Movendo o jogador com base nas teclas pressionadas
    if comandos[K_RIGHT]:
        player.andar('direita', pedras_lisas, pedregulhos)
    elif comandos[K_LEFT]:
        player.andar('esquerda', pedras_lisas, pedregulhos)
    elif comandos[K_UP]:
        player.andar('cima', pedras_lisas, pedregulhos)
    elif comandos[K_DOWN]:
        player.andar('baixo', pedras_lisas, pedregulhos)
    else:
        player.parar()

    # Remove as bombas que explodiram
    for bomba in bombas.copy():
        if bomba.explodir:
            bombas.remove(bomba)
            todas_sprites.remove(bomba)

    # Atualizando a tela
    pygame.display.flip()

    # Taxa de Atualização
    pygame.time.Clock().tick(60)

while vitoria == True:
    tela.fill((0, 0, 0))
    vitoriagroup.draw(tela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0] and sair.rect.collidepoint(pygame.mouse.get_pos()):
            exit()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Verifica se o mouse está sobre o botão iniciar e jogar
    if sair.rect.collidepoint(mouse_x, mouse_y):
        # Desenha a imagem do cursor personalizado
        tela.blit(mouse, (mouse_x - 16, mouse_y - 25))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
    pygame.display.flip()

# GAME OVER
pygame.mixer.music.load("Sons/gameover.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(1)

while gameover == True:
    tela.fill((0,0,0))
    gameOgroup.draw(tela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0] and sair.rect.collidepoint(pygame.mouse.get_pos()):
            exit()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Verifica se o mouse está sobre o botão iniciar e jogar
    if sair.rect.collidepoint(mouse_x, mouse_y):
        # Desenha a imagem do cursor personalizado
        tela.blit(mouse, (mouse_x - 16, mouse_y - 25))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
    pygame.display.flip()