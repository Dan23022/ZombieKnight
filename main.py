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

        self.max_health = 100
        self.health = self.max_health

        self.health_bar_height = 40
        self.health_bar_colour = (255, 0, 0)

        self.attack_cooldown = 10
        self.last_attack_time = 0

    def update(self, keys, dt):

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

    def attack(self):
        current_time = pygame.time.get_ticks() / 1000

        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time

            zombies_to_kill = []
            for zombie in zombie_list:
                if abs(self.rect.centerx - zombie.rect.centerx) <= 20 and abs(
                        self.rect.centery - zombie.rect.centery) <= 20:
                    zombies_to_kill.append(zombie)

            for zombie in zombies_to_kill:
                zombie_list.remove(zombie)

    def draw_health_bar(self):
        health_bar_width = int((self.health / self.max_health) * screen.get_width())
        health_bar_rect = pygame.Rect(0, 0, health_bar_width, self.health_bar_height)
        pygame.draw.rect(screen, self.health_bar_colour, health_bar_rect)

    def handle_collision(self, collided_zombies):
        self.health -= len(collided_zombies)
        if self.health <= 0:
            pass

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

        self.alive = True

    def update(self, player):
        if self.alive:
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed


player = Player()
player.rect.x = screen.get_width() // 2
player.rect.y = screen.get_height() // 2
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()

    keys = pygame.key.get_pressed()  # Check the state of all keys

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    screen.blit(background_surface, (0, 0))

    player_list.update(keys, dt)  # Update the player's position with the current keys
    player_list.draw(screen)

    for zombie in zombie_list:
        zombie.update(player)

    zombie_list.draw(screen)

    player.draw_health_bar()

    if len(zombie_list) < 75:
        if random.random() < 0.1:  # Adjust the probability of spawning a new zombie
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

    zombie_hit = pygame.sprite.spritecollide(player, zombie_list, False)

    if zombie_hit:
        player.handle_collision(zombie_hit)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()