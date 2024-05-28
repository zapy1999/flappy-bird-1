import pygame
import random


pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


BIRD_WIDTH = 40
BIRD_HEIGHT = 35
BIRD_X = SCREEN_WIDTH // 4
BIRD_Y = SCREEN_HEIGHT // 2
GRAVITY = 0.6
FLAP_STRENGTH = -10


PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200
PIPE_VELOCITY = -3 


bird_image = pygame.transform.scale(pygame.image.load("bird.png"), (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.transform.scale(pygame.image.load("pipe(1).png"), (PIPE_WIDTH, PIPE_HEIGHT))
ground_image = pygame.image.load("ground (1).png")
background_image = pygame.transform.scale(pygame.image.load("background (2).png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_image = pygame.image.load("gameover.png")
hit_sound = pygame.mixer.Sound("hit.wav")
point_sound = pygame.mixer.Sound("point.wav")
wing_sound = pygame.mixer.Sound("wing.wav")
background_music = "music_bird.mp3"


pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  



class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(PIPE_GAP, SCREEN_HEIGHT - PIPE_GAP)
        self.passed = False

    def update(self):
        self.x += PIPE_VELOCITY

    def draw(self, screen):
        
        screen.blit(pipe_image, (self.x, self.height))
       
        screen.blit(pygame.transform.flip(pipe_image, False, True), (self.x, self.height - PIPE_GAP - PIPE_HEIGHT))

    def get_rects(self):
        return [pygame.Rect(self.x, self.height, PIPE_WIDTH, PIPE_HEIGHT),
                pygame.Rect(self.x, self.height - PIPE_GAP - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)]

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    game_started = False
    game_over = False

    running = True
    while running:
        screen.blit(background_image, (0,0))

        if not game_started:
            draw_text(screen, "Press SPACE to start", 50, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_started = True
                    game_over = False
                    bird = Bird()
                    pipes = [Pipe(SCREEN_WIDTH + 100)]
                    score = 0
        elif game_over:
            screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_image.get_height() // 2 - 50))
            draw_text(screen, "Press SPACE to restart", 50, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_started = True
                    game_over = False
                    bird = Bird()
                    pipes = [Pipe(SCREEN_WIDTH + 100)]
                    score = 0
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
                    wing_sound.play()  

            bird.update()
            bird.draw(screen)

            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe(SCREEN_WIDTH + 100))

            for pipe in pipes:
                pipe.update()
                pipe.draw(screen)
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)

                if pipe.x < bird.x and not pipe.passed:
                    pipe.passed = True
                    score += 1
                    point_sound.play() 

                if bird.get_rect().collidelist(pipe.get_rects()) != -1 or bird.y > SCREEN_HEIGHT or bird.y < 0:
                    hit_sound.play()  
                    game_over = True
                    

            ground_rect = pygame.Rect(0, SCREEN_HEIGHT - ground_image.get_height(), SCREEN_WIDTH, ground_image.get_height())
            if bird.get_rect().colliderect(ground_rect):
                hit_sound.play()  
                game_over = True

            screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_image.get_height()))

            
                    

            font = pygame.font.SysFont(None, 55)
            score_text = font.render(str(score), True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2, 50))

            screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_image.get_height()))

            pygame.display.flip()
            clock.tick(50)

    pygame.quit()

if __name__ == "__main__":
    main()
    