import pygame
import neat
import time
import os
import random
import time
from Bird import Bird
from Base import Base
from Pipe import Pipe

pygame.font.init()

GEN = 0
WIN_WIDTH = 500
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 50)
FPS = 30
TIME_BETWEEN_KEYS = 0.2
START_COUNTER_KEYS = 0.0
MAX_SCORE = 0

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

def draw_window(win, bird, pipes, base, score, best_score):
    win.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Best Score: " + str(best_score), 1, (255,255,255))
    win.blit(text, (10, 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def main():
    global START_COUNTER_KEYS
    global FPS
    global MAX_SCORE

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    best_score = 0

    while True:

        last_score_level = 0
        distance_pipes = 600
        current_velocity = 5

        bird = Bird(230, 350)
        base = Base(730)
        pipes = [Pipe(distance_pipes)]
        
        clock = pygame.time.Clock()

        score = 0
        run = True

        

        while run:

            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            pipe_ind = 0
            add_pipe = False

            for pipe in pipes:
                if pipe.collide(bird):
                    run = False
                    
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                #if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                #    rem.append(pipe)

                pipe.move(current_velocity)

            if add_pipe:
                score += 1
                pipes.append(Pipe(distance_pipes))

            if score > 1000:
                break

            base.move(current_velocity)
            draw_window(win, bird, pipes, base, score, best_score)

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_SPACE]:
                bird.jump()

            if time.time() - START_COUNTER_KEYS > TIME_BETWEEN_KEYS:
                START_COUNTER_KEYS = time.time()
                if pressed[pygame.K_RIGHT]:
                    if FPS < 60:
                        FPS = FPS * 2
                        print("Current fps: " + str(FPS))
                    else:
                        print("Max velocity reached")
                if pressed[pygame.K_LEFT]:
                    if FPS > 1:
                        FPS = FPS / 2
                        print("Current fps: " + str(FPS))
                    else:
                        print("Min velocity reached")

            if bird.y >= WIN_HEIGHT:
                run = False

            bird.move()

            # increase difficulty
            if last_score_level < score:
                last_score_level = score
                if score % 10 == 0:
                    distance_pipes += 10
                    current_velocity += 2
                    print("Velocity: " + str(current_velocity))

            if score > best_score:
                best_score = score

    

if __name__ == "__main__":
    main()




      