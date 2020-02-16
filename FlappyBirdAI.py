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

def draw_window(win, birds, pipes, base, score, gen, maxScore):
    win.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Max score: " + str(maxScore), 1, (255,255,255))
    win.blit(text, (10, WIN_HEIGHT - 10 - text.get_width()))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()



def main(genomes, config):
    global GEN
    global START_COUNTER_KEYS
    global FPS
    global MAX_SCORE

    last_score_level = 0
    distance_pipes = 600
    current_velocity = 5
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(distance_pipes)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
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
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds) :
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move(current_velocity)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(distance_pipes))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score > 1000:
            break

        base.move(current_velocity)
        draw_window(win, birds, pipes, base, score, GEN, MAX_SCORE)

        pressed = pygame.key.get_pressed()
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

        # increase difficulty
        if last_score_level < score:
            last_score_level = score
            if score % 10 == 0:
                distance_pipes += 25
                current_velocity += 2
                print("Velocity: " + str(current_velocity))

        if MAX_SCORE < score:
            MAX_SCORE = score
        



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main, 50)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configAI.txt")
    run(config_path)