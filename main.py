import random
import pygame

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        sprite = pygame.image.load('sprite.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (90, 90))
        self.images.append(sprite)
        self.images.append(pygame.transform.flip(sprite, flip_x=True, flip_y=False))
        self.image = self.images[0]
        self.speed = 5  # Define the player's speed
        self.rect = self.image.get_rect()

    def update(self, keys):

        if keys[pygame.K_d]:
            if player.rect.x < screen.get_width() - player.rect.width:
                self.image = self.images[0]
                self.rect.x += self.speed

        if keys[pygame.K_a]:
            if player.rect.x > screen.get_width() - screen.get_width():
                self.image = self.images[1]
                self.rect.x -= self.speed

        if keys[pygame.K_w]:
            if player.rect.y > screen.get_height() - screen.get_height():
                self.rect.y -= self.speed

        if keys[pygame.K_s]:
            if player.rect.y < screen.get_height() - player.image.get_height():
                self.rect.y += self.speed

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        sprite = pygame.image.load('zombie.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (80, 80))
        self.images.append(sprite)
        self.images.append(pygame.transform.flip(sprite, flip_x=True, flip_y=False))
        self.image = self.images[0]
        self.speed = 2  # Define the player's speed
        self.rect = self.image.get_rect()

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, abs(dx) + abs(dy))
        self.rect.x += (dx / dist) * self.speed
        self.rect.y += (dy / dist) * self.speed


player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)

zombie_list = pygame.sprite.Group()

background = pygame.image.load("background.png")
floor_number_of_squares = (24, 24)
background_surface = pygame.Surface((background.get_width() * floor_number_of_squares[0],
                                     background.get_height() * floor_number_of_squares[1]))
for x in range(floor_number_of_squares[0]):
    for y in range(floor_number_of_squares[1]):
        background_surface.blit(background, (x * background.get_width(), y * background.get_height()))

pygame.init()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERUP or event.type == pygame.FINGERMOTION:
            for touch in event.touches:
                touch_x, touch_y = touch.position

                # Map touch coordinates to the screen coordinates
                touch_x = touch_x * screen.get_width()
                touch_y = touch_y * screen.get_height()

                # Check for touch controls
                if touch_x < screen.get_width() // 2:  # Left side of the screen
                    keys[pygame.K_a] = True
                    keys[pygame.K_d] = False
                else:  # Right side of the screen
                    keys[pygame.K_a] = False
                    keys[pygame.K_d] = True

                if touch_y < screen.get_height() // 2:  # Top half of the screen
                    keys[pygame.K_w] = True
                    keys[pygame.K_s] = False
                else:  # Bottom half of the screen
                    keys[pygame.K_w] = False
                    keys[pygame.K_s] = True

    keys = pygame.key.get_pressed()  # Check the state of all keys

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    screen.blit(background_surface, (0, 0))

    player_list.update(keys)  # Update the player's position with the current keys
    player_list.draw(screen)

    for zombie in zombie_list:
        zombie.update(player)

    zombie_list.draw(screen)

    if len(zombie_list) < 20:
        if random.random() < 0.01:  # Adjust the probability of spawning a new zombie
            zombie = Zombie()
            side = random.randint(1, 4)  # Determine the side from which the zombie will spawn

            if side == 1:  # Left side
                zombie.rect.x = random.randint(-100, -80)
                zombie.rect.y = random.randint(0, screen.get_height() - zombie.rect.height)
            elif side == 2:  # Right side
                zombie.rect.x = random.randint(screen.get_width() + 80, screen.get_width() + 100)
                zombie.rect.y = random.randint(0, screen.get_height() - zombie.rect.height)
            elif side == 3:  # Top side
                zombie.rect.x = random.randint(0, screen.get_width() - zombie.rect.width)
                zombie.rect.y = random.randint(-100, -80)
            elif side == 4:  # Bottom side
                zombie.rect.x = random.randint(0, screen.get_width() - zombie.rect.width)
                zombie.rect.y = random.randint(screen.get_height() + 80, screen.get_height() + 100)

            zombie_list.add(zombie)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()