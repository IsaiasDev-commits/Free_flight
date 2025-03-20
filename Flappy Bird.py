import pygame
import random
import os

# Inicializar pygame
pygame.init()

# Configuración de pantalla adaptable
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Preguntar si el usuario quiere pantalla completa
fullscreen = input("¿Quieres jugar en pantalla completa? (s/n): ").strip().lower() == "s"

# Configuración de la ventana
flags = pygame.FULLSCREEN | pygame.NOFRAME if fullscreen else 0
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("Flappy Bird")

# Colores y fuentes
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 48)

# Función para verificar archivos
def check_file(filename):
    if not os.path.exists(filename):
        print(f"Error: No se encontró {filename}")
        return False
    return True

# Cargar imágenes
if check_file("bird.png") and check_file("tree.png") and check_file("background.png"):
    bird_img = pygame.image.load("bird.png")
    tree_img = pygame.image.load("tree.png")
    background_img = pygame.image.load("background.png")

    # Ajustar tamaños automáticamente según la pantalla
    bird_size = (WIDTH // 10, HEIGHT // 15)  
    tree_size = (WIDTH // 6, HEIGHT // 2)  
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    
    bird_img = pygame.transform.scale(bird_img, bird_size)
    tree_img = pygame.transform.scale(tree_img, tree_size)
else:
    print("Error: Archivos de imagen faltantes.")
    exit()

# Cargar sonidos
pygame.mixer.init()
if check_file("background_music.mp3") and check_file("hit_sound.mp3"):
    pygame.mixer.music.load("background_music.mp3")
    game_over_sound = pygame.mixer.Sound("hit_sound.mp3")
else:
    print("Error: Archivos de sonido faltantes.")
    exit()

# Clase del pájaro
class Bird:
    def __init__(self):
        self.x = WIDTH // 8
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = HEIGHT * 0.0015
        self.alive = True  

    def flap(self):
        if self.alive:
            self.velocity = -HEIGHT * 0.02  

    def move(self):
        if self.alive:
            self.velocity += self.gravity
            self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, bird_img.get_width(), bird_img.get_height())

# Clase de los árboles
class Tree:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(HEIGHT // 4, HEIGHT // 2)
        self.gap = HEIGHT // 4  
        self.speed = WIDTH * 0.005  

    def move(self):
        self.x -= self.speed  
        if self.x < -tree_img.get_width():
            self.x = WIDTH
            self.height = random.randint(HEIGHT // 4, HEIGHT // 2)
            return True  
        return False  

    def draw(self):
        tree_top = pygame.transform.flip(tree_img, False, True)  
        screen.blit(tree_top, (self.x, self.height - tree_img.get_height()))  
        screen.blit(tree_img, (self.x, self.height + self.gap))  

    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.height - tree_img.get_height(), tree_img.get_width(), tree_img.get_height())
        bottom_rect = pygame.Rect(self.x, self.height + self.gap, tree_img.get_width(), tree_img.get_height())
        return top_rect, bottom_rect

# Función para reiniciar el juego
def restart_game():
    global bird, trees, game_over, score, speed
    bird = Bird()
    trees = [Tree(WIDTH // 1.5), Tree(WIDTH * 1.2)]
    game_over = False
    score = 0
    speed = WIDTH * 0.005  
    pygame.mixer.music.play(-1)

# Inicializar objetos
bird = Bird()
trees = [Tree(WIDTH // 1.5), Tree(WIDTH * 1.2)]
game_over = False
score = 0
speed = WIDTH * 0.005  

pygame.mixer.music.play(-1)  

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_img, (0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            if not game_over:
                bird.flap()
            else:
                restart_game()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            pygame.image.save(screen, "captura.png")
            print("Captura guardada como 'captura.png'.")

    if not game_over:
        bird.move()
        bird.draw()

        for tree in trees:
            if tree.move():
                score += 1
                if score % 5 == 0:  
                    speed += WIDTH * 0.0005  
                    for t in trees:
                        t.speed = speed  

            tree.draw()

            # Detección de colisión con los árboles
            bird_rect = bird.get_rect()
            top_rect, bottom_rect = tree.get_rects()

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect) or bird.y >= HEIGHT or bird.y <= 0:
                game_over = True
                pygame.mixer.music.stop()
                game_over_sound.play()

    else:
        text = font.render("Game Over - Toca para reiniciar", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    # Mostrar puntuación
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


