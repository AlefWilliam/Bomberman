import pygame
def criar_terreno(pedras_lisas, pedregulhos):
    a, b = 113, 63

    # Esquerda
    for i in range(11):
        pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
        pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
        pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
        pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
        b += 45

        # Pedras Lisas no Terreno
        if i == 1 or i == 3 or i == 5 or i == 7:
            for j in range(15):
                if j == 1 or j == 3 or j == 5 or j == 7 or j == 9 or j == 11:
                    a += 90
                    pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
                    pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
                    pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
                    pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
            a = 113

    # Emcima
    a, b = 113, 63
    for i in range(15):
        pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
        pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
        pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
        pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
        a += 45

    # Embaixo
    a, b = 743, 63
    for i in range(11):
        pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
        pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
        pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
        pedra_lisa.rect = pygame.Rect(a, b, 30, 30)
        b += 45

    # Direita
    a, b = 113, 513
    for i in range(13):
        a += 45
        pedra_lisa = pygame.sprite.Sprite(pedras_lisas)
        pedra_lisa.image = pygame.image.load("sprites/PedraLisa.png")
        pedra_lisa.image = pygame.transform.scale(pedra_lisa.image, [45, 45])
        pedra_lisa.rect = pygame.Rect(a, b, 30, 30)

    # Posição da Pedregulho
    a, b = 158, 63
    for i in range(11):
        if i == 1:
            a += 90
            for j in range(11):
                if j == 9 or j == 10:
                    continue
                else:
                    pedregulho = pygame.sprite.Sprite(pedregulhos)
                    pedregulho.image = pygame.image.load("sprites/Pedregulho.png")
                    pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
                    pedregulho.rect = pygame.Rect(a, b, 30, 30)
                a += 45
            a = 158

        if i == 3 or i == 5 or i == 7:
            for j in range(13):
                pedregulho = pygame.sprite.Sprite(pedregulhos)
                pedregulho.image = pygame.image.load("sprites/Pedregulho.png")
                pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
                pedregulho.rect = pygame.Rect(a, b, 30, 30)
                a += 45
            a = 158

        elif i == 9:
            for j in range(11):
                pedregulho = pygame.sprite.Sprite(pedregulhos)
                pedregulho.image = pygame.image.load("sprites/Pedregulho.png")
                pedregulho.image = pygame.transform.scale(pedregulho.image, [45, 45])
                pedregulho.rect = pygame.Rect(a, b, 30, 30)
                a += 45
            a = 158
        b += 45

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