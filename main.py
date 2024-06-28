import pygame
import random
import math
import time
pygame.init()

WIDTH, HEIGHT = 600, 400

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Improver")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (84, 69, 23)
LIVES = 5
TOP_BAR_HEIGHT = 60

LABEL_FONT = pygame.font.SysFont("comicsans", 30, False, True)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "yellow"
    SECOND_COLOR = "blue"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    
    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size #if distance if less then size


def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)
    

def format_time(secs):
    milliseconds = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}" #02d means 2 digits if it doesnt have 2 digits start with 0

def draw_top_bar(win, elpased_time, targets_pressed, misses):
    pygame.draw.rect(win, "pink", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elpased_time)}", 1, "black")

    win.blit(time_label, (5, 5)) #to display another surface. so it means you can put text on top of another surface

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    elapsed_time = time.time() - start_time

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            #to see if mouse position is colided with the target
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                click += 1

    
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
            
            if click and target.collide(*mouse_pos): #breaks tuple into individual variables
                targets.remove(target)
                targets_pressed += 1

            if misses >= LIVES:
                pass #finish the game

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
