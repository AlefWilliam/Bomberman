import pygame
from pygame.locals import *
from sys import exit

# Inicialização do Pygame
pygame.init()

#funções
def pedra_lisa(x,y):
    lisa.rect = pygame.Rect(x,y,30,30)
    lisaGroup.draw(tela)

def pedregulho(x,y):
    pedra.rect = pygame.Rect(x,y,30,30)
    pedraGroup.draw(tela)

#Pedra lisa
lisaGroup = pygame.sprite.Group()
lisa = pygame.sprite.Sprite(lisaGroup)
lisa.image = pygame.image.load("sprites/PedraLisa.png")
lisa.image = pygame.transform.scale(lisa.image, [45,45])

#Pedregulho
pedraGroup = pygame.sprite.Group()
pedra = pygame.sprite.Sprite(pedraGroup)
pedra.image = pygame.image. load("sprites/Predregulho.png")
pedra.image = pygame.transform.scale(pedra.image,[45,45])

# Configurações da tela
largura = 900
altura = 620
verde = (47, 79, 47)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('BOMBERMAN')

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
        self.tempo_decorrido = 0  # Contador de tempo em frames
        self.tempo_explosao = 130  # 10 segundos a 30 frames por segundo

    def explode(self, pedregulhos):
        explosao_sprites = ['sprites/fogotodolado4.png', 'sprites/fogohorizontal4.png', 'sprites/fogovertical4.png',
                            'sprites/fogocima4.png', 'sprites/fogodireita4.png', 'sprites/fogobaixo4.png',
                            'sprites/fogoesquerda4.png']

        tamanho_celula = 45
        explosao_meio = Explosao(explosao_sprites[0], (self.rect.topleft[0] - 5, self.rect.topleft[1] - 10), tamanho_celula)

        explosoes.add(explosao_meio)
        todas_sprites.add(explosao_meio)

        # Explosão vertical para cima
        for i in range(1, 3):
            new_position = (self.rect.topleft[0], self.rect.topleft[1] - i * tamanho_celula)
            if i == 1:
                if i == 1:
                    # Ajuste aqui: Subtrai uma pequena quantidade para cima (por exemplo, 5 pixels)
                    explosao = Explosao(explosao_sprites[2], (new_position[0]-6, new_position[1] - 7), tamanho_celula)
            else:
                explosao = Explosao(explosao_sprites[3], (new_position[0]-6, new_position[1] - 7), tamanho_celula)
            explosoes.add(explosao)
            todas_sprites.add(explosao)

        # Explosão vertical para baixo
        for i in range(1, 3):
            new_position = (self.rect.topleft[0], self.rect.topleft[1] + i * tamanho_celula)
            if i == 1:
                # Ajuste aqui: Adiciona uma pequena quantidade para baixo (por exemplo, 5 pixels)
                explosao = Explosao(explosao_sprites[2], (new_position[0]-7, new_position[1] - 10), tamanho_celula)
            else:
                explosao = Explosao(explosao_sprites[5], (new_position[0]-6,new_position[1]-10), tamanho_celula)
            explosoes.add(explosao)
            todas_sprites.add(explosao)

        # Explosão horizontal para direita
        for i in range(1, 3):
            new_position = (self.rect.topleft[0] + i * tamanho_celula - 5, self.rect.topleft[1] - 9)
            if i == 1:
                explosao = Explosao(explosao_sprites[1], new_position, tamanho_celula)
            else:
                explosao = Explosao(explosao_sprites[4], new_position, tamanho_celula)
            explosoes.add(explosao)
            todas_sprites.add(explosao)

        # Explosão horizontal para esquerda
        for i in range(1, 3):
            new_position = (self.rect.topleft[0] - i * tamanho_celula - 5, self.rect.topleft[1] - 10)
            if i == 1:
                explosao = Explosao(explosao_sprites[1], new_position, tamanho_celula)
            else:
                explosao = Explosao(explosao_sprites[6], new_position, tamanho_celula)
            explosoes.add(explosao)
            todas_sprites.add(explosao)

        # Verifica colisões com pedregulhos e remove-os
        for pedregulho in pedregulhos.copy():
            for explosao in explosoes:
                if pygame.sprite.collide_rect(explosao, pedregulho):
                    pedregulhos.remove(pedregulho)
                    todas_sprites.remove(pedregulho)

    def update(self):
        if not self.explodir:
            self.atual = (self.atual + 0.1) % len(self.sprites)
            self.image = self.sprites[int(self.atual)]
            # Atualiza o contador de tempo
            self.tempo_decorrido += 1
            # Verifica se o tempo de explosão foi atingido
            if self.tempo_decorrido >= self.tempo_explosao:
                self.explodir = True
                self.explode(pedregulhos)
        else:
            # Lógica para a explosão da bomba (se necessário)
            pass
class Explosao(pygame.sprite.Sprite):
    def __init__(self, sprite_path, position,tamanho_celula):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(sprite_path)]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.center = position  # Use center em vez de topleft para centralizar
        self.tempo_decorrido = 0
        self.tempo_decorrido = 0
        self.tempo_explosao = 10  # Ajuste conforme necessário
        self.tamanho_celula = tamanho_celula

    def update(self):
        self.atual = (self.atual + 0.1) % len(self.sprites)
        self.image = pygame.transform.scale(self.sprites[int(self.atual)], (self.tamanho_celula, self.tamanho_celula))
        self.tempo_decorrido += 1
        if self.tempo_decorrido >= self.tempo_explosao:
            todas_sprites.remove(self)
            explosoes.remove(self)
# Dicionário de sprites para cada direção
sprites_dict = {
    'direita': ['sprites/Direita_0.png', 'sprites/Direita_1.png', 'sprites/Direita_3.png', 'sprites/Direita_2.png',
                'sprites/Direita_4.png'],
    'esquerda': ['sprites/Esquerda_0.png', 'sprites/Esquerda_1.png', 'sprites/Esquerda_3.png', 'sprites/Esquerda_2.png',
                 'sprites/Esquerda_4.png'],
    'cima': ['sprites/Cima_0.png', 'sprites/Cima_1.png', 'sprites/Cima_2.png', 'sprites/Cima_3.png',
             'sprites/Cima_4.png'],
    'baixo': ['sprites/Baixo_0.png', 'sprites/Baixo_1.png', 'sprites/Baixo_2.png', 'sprites/Baixo_3.png',
              'sprites/Baixo_4.png']
}

# Criando uma instância do jogador
player = Player(sprites_dict, (32, 42), (170, 110))
pedras_lisas = pygame.sprite.Group()
pedregulhos = pygame.sprite.Group()
bombas = pygame.sprite.Group()
explosoes = pygame.sprite.Group()
a = 113
b = 63

# Esquerda
for i in range(11):
    pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
    pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
    pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
    pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
    b += 45

    # Pedras Lisas no Terreno
    if i == 1 or i == 3 or i == 5 or i == 7:
        for i in range(15):
            if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 11:
                a += 90
                pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
                pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
                pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
                pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
        a = 113

# Emcima
a = 113
b = 63
for i in range(15):
    pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
    pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
    pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
    pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
    a += 45

# Embaixo
a = 743
b = 63
for i in range(11):
    pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
    pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
    pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
    pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
    b += 45

# Direita
a = 113
b = 513
for i in range(13):
    a += 45
    pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
    pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
    pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
    pedra_lisa.rect = pygame.Rect(a, b, 30, 30)

# Posição da Pedra
a = 158
b = 63
for i in range(11):
    if i == 1:
        a += 90
        for i in range(11):
            pedregulho = pygame.sprite.Sprite(pedregulhos)
            pedregulho.image = pygame.image.load("sprites/Predregulho.png")
            pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
            pedregulho.rect = pygame.Rect(a, b, 30, 30)
            a += 45
        a = 158

    if i == 3 or i == 5 or i == 7:
        for i in range(13):
            pedregulho = pygame.sprite.Sprite(pedregulhos)
            pedregulho.image = pygame.image.load("sprites/Predregulho.png")
            pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
            pedregulho.rect = pygame.Rect(a, b, 30, 30)
            a += 45
        a = 158

    elif i == 9:
        for i in range(11):
            pedregulho = pygame.sprite.Sprite(pedregulhos)
            pedregulho.image = pygame.image.load("sprites/Predregulho.png")
            pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
            pedregulho.rect = pygame.Rect(a, b, 30, 30)
            a += 45
        a = 158
    b += 45
# Criando um grupo de sprites
todas_sprites = pygame.sprite.Group()
todas_sprites.add(player,pedras_lisas,pedregulhos)
bombas_colocadas = set()
# Configuração do relógio
relogio = pygame.time.Clock()

# Loop principal
while True:
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

    # Atualizando a tela
    pygame.display.flip()

    # Verificação de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
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

    # Atualiza as bombas
    for bomba in bombas:
        bomba.update()
        tela.blit(bomba.image, bomba.rect)

    # Remove as bombas que explodiram
    for bomba in bombas.copy():
        if bomba.explodir:
            bombas.remove(bomba)
            todas_sprites.remove(bomba)

    # Atualizando a tela
    pygame.display.flip()