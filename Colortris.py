from cProfile import run
from cgitb import text
import pygame
import random
pygame.init()
pygame.font.init()

# Rebecca Barros Alarça
# 22010373

# Designação de fonte e tamanho do ecrã
LOSER_FONT = pygame.font.SysFont("comicsans", 40)
SCORE_FONT = pygame.font.SysFont("comicsans", 25)
x = 420
y = 650

# Cores usadas e configuração do ecrã
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 225)
yellow = (255, 255, 0)
green = (0,128,0)
white = (255, 255, 255)
display_surface = pygame.display.set_mode((x, y))
pygame.display.set_caption("ColorTris")
display_surface.fill(black)

# Posição do jogador, matriz, níveis e pontos iniciais
current_player = (3,0)
score = 0
level = 1
map = [[0, 0, 0,0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]]
is_over = False


clock = pygame.time.Clock()

# Função para desenhar as elipses, 4 cores
def draw_ellipse(x,y,color):
    
    if color == 1:
        pygame.draw.ellipse(display_surface, red, (60 * x, 60 * y + 50, 60, 60), 8)
    if color == 2:
        pygame.draw.ellipse(display_surface, blue, (60 * x, 60 * y + 50, 60, 60), 8)
    if color == 3:
        pygame.draw.ellipse(display_surface, yellow, (60 * x, 60 * y + 50, 60, 60), 8)
    if color == 4:
        pygame.draw.ellipse(display_surface, green, (60 * x, 60 * y + 50, 60, 60), 8)
#Desenhar o mapa com a matriz correta
def draw_map():
    for y in range(0,10):
        for x in range(0,7):
            if map[y][x] != 0:
                draw_ellipse(x,y, map[y][x])
# Texto Game Over
def draw_loser(text):
    draw_text = LOSER_FONT.render(text, 1, white)
    display_surface.blit(draw_text, (x/2 - draw_text.get_width()/
                         2, y/2 - draw_text.get_height()/2))
    pygame.display.update()
    
# Reset para recomeçar do início caso perca o jogo. Reinicia em alguns segundos
def reset():
    global current_player
    global score
    global map
    global is_over
    global level
    is_over = False
    current_player = (3,0)
    score = 0
    level = 1
    map = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]
# Texto do score
def draw_score():
    global score
    draw_text = SCORE_FONT.render(str(score), 1, white)
    display_surface.blit(draw_text, (x - draw_text.get_width()*
                        4, y - draw_text.get_height()*18))
# Texto do Nível
def draw_level():
    global level
    draw_text = SCORE_FONT.render(str(level), 1, white)
    display_surface.blit(draw_text, (x/2 - draw_text.get_width()*
                        12, y - draw_text.get_height()*18))
# Função que faz a peça do jogador cair uma linha na matriz constantemente
def down():
    global current_player
    global is_over
    hasMoved = False
    for y in range(8, -1, -1):
        for x in range(0, 7):
            if map[y][x] != 0:
                if map[y + 1][x] == 0:
                    hasMoved = True
                    map[y + 1][x] = map[y][x]
                    map[y][x] = 0
                    if (x,y) == current_player:
                        current_player = (x, y + 1)
    if not(hasMoved):
        if map[0][3] != 0:
            is_over = True
          #sorteia o novo
        map[0][3] = random.choice(range(1,5))
        current_player = (3, 0)
    return
# Faz o jogador conseguir ir para a esquerda
def left():
    global current_player
    x,y = current_player
    if x > 0:
        if map[y][x - 1] == 0:
            map[y][x - 1] = map[y][x]
            map[y][x] = 0
            current_player = (x - 1, y)
    return
# Consegue mover para a direita
def right():
    global current_player
    x,y = current_player
    if x < 6:
        if map[y][x + 1] == 0:
            map[y][x + 1] = map[y][x]
            map[y][x] = 0
            current_player = (x + 1, y)
    return
    # Aqui acontece a pontuação do jogo, apaga as peças 
    # 3 peças ou mais da mesma cor, vertical e horizontal
def point_level():
    global current_player
    global score
    global level
    current_x, current_y = current_player
    # apagar linhas
    for y in range(9, -1, -1):
        for x in range(1, 6):
            right = x + 1
            left = x - 1
            if map[y][x] > 0 and not (current_x == x and current_y == y):
                if map[y][left] == map[y][x] and map[y][x] == map[y][right]:
                    if right < 6:
                        for i in range(right + 1, 7):
                            if map[y][x] == map[y][i]:
                              right = i
                    if left > 1:
                        for i in range(left, -1, -1):
                            if map[y][x] == map [y][i]:
                                left = i
                            else:
                                break
                    for i in range(left, right + 1):
                        map[y][i] = 0
                            # sistema de pontuação 
                        if map[y][i] == 0:
                            n = right - left + 1
                            if n == 3:
                                new_score = 10
                            if n == 4:
                                new_score = 30
                            if n >= 5:
                                new_score = 70
                            
                            score = score + new_score                       
    # apagar colunas 
    for x in range(0,7):
        for y in range(8, 0, -1):
            up = y - 1
            down = y + 1
            if map[y][x] > 0 and not (current_x == x and current_y == y):
                if map[up][x] == map[y][x] and map[y][x] == map[down][x]:
                    if up > 0:
                        for i in range(up, -1, -1):
                            if map[y][x] == map[i][x]:
                                up = i
                            else:
                                break
                    for i in range(down, up - 1, -1):
                        map[i][x] = 0
                    # sistema de pontuação
                        if map[i][x] == 0:
                            n = down - up + 1
                            if n == 3:
                                new_score = 10
                            if n == 4:
                                new_score = 30
                            if n >= 5:
                                new_score = 70
                            
                            score = score + new_score
    level = 1 + int(score//500)
    return                   

# Função principal                            
while run :
    # Velocidade progressiva que aumenta de acordo com o nível 
    fall_speed = 0.27
    clock.tick(level)
    
    if is_over:
        draw_loser("Game Over")
        pygame.time.delay(5000)
        reset()

    display_surface.fill(black)
    
    down()
    draw_map()
    draw_score()
    draw_level()
    point_level()

        
    pygame.display.update()
    

    #eventos de teclas
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left()
                display_surface.fill(black)
                draw_map()
                draw_score()
                draw_level()
            if event.key == pygame.K_RIGHT:
                right()
                display_surface.fill(black)
                draw_map()
                draw_score()
                draw_level()
                # down 2x para descer mais duas linhas
            if event.key == pygame.K_DOWN:
                down()
                down()
                display_surface.fill(black)
                draw_map()
                draw_score()
                draw_level()
        if event.type == pygame.QUIT:
            pygame.quit()
            # para sair do jogo
            quit()
        pygame.display.update()