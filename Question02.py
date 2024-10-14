###--------------------------####
###-------Quetion02----------####
###--------------------------####

# importing libraries
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# defining a timer for enemy spawning
ENEMY_SPAWN_TIME = 2000  # 2 seconds
pygame.time.set_timer(pygame.USEREVENT, ENEMY_SPAWN_TIME)

# Create screen window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D game window")

# Set the frame rate
clock = pygame.time.Clock()

###  creating player classes  ####

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

# Load the image of the player (replace 'hero_image.png' with your actual image file)
        self.image = pygame.image.load('hero_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image if needed

        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 100)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.health = 100
        self.lives = 3

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Stay on the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.speed_y = 0

    def jump(self):
        if self.rect.bottom >= HEIGHT - 50:  # Can only jump if on the ground
            self.speed_y = self.jump_strength

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

### creating projectile class ###

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > WIDTH:
            self.kill()  # Remove projectile if it leaves the screen

### creating enemy class ###
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])  # Enemies move either left or right
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])
        self.target = target

    def update(self):
        # Move enemy toward the player's current position
        if self.rect.x < self.target.rect.x:
            self.rect.x += 2  # Speed toward the right
        else:
            self.rect.x -= 2  # Speed toward the left

        if self.rect.y < self.target.rect.y:
            self.rect.y += 2  # Speed downward
        else:
            self.rect.y -= 2  # Speed upward

        # Wrap enemies around the screen if they go out of bounds (optional)
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT


### create collectable class ###
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type  # 'health' or 'life'
        self.image = pygame.Surface((30, 30))
        if self.type == 'health':
            self.image.fill(GREEN)
        elif self.type == 'life':
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        pass  # Update logic for collectible (e.g., moving, disappearing)

### levels and camera  ###
class Camera:
    def __init__(self):
        self.offset = 0

    def apply(self, rect):
        return rect.move(self.offset, 0)

    def update(self, target):
        self.offset = -target.rect.centerx + WIDTH // 2

camera = Camera()

### main loop ###

# Sprite groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Player object
player = Player()
all_sprites.add(player)

# Initialize score and other variables at the top
score = 0

# Game Loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:  # Check for the custom event to spawn enemies
            enemy = Enemy(WIDTH, random.randint(50, HEIGHT - 50), player)
            all_sprites.add(enemy)
            enemies.add(enemy)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop()

    if keys[pygame.K_SPACE]:
        player.jump()

    if keys[pygame.K_z]:  # Shoot projectile
        projectile = Projectile(player.rect.right, player.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

    # Update
    all_sprites.update()
    camera.update(player)

    # Drawing
    screen.fill(WHITE)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    # Check for collisions between projectiles and enemies
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for hit in hits:
        score += 10  # Increment score for each enemy hit

    # Check for collisions between player and enemies
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in enemy_hits:
        player.health -= 1  # Decrease player health when hit by an enemy
        if player.health <= 0:
            running = False  # End the game if health reaches 0

    # Display score and health on screen
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

    pygame.display.flip()

pygame.quit()

#scoring and health

# score = 0 

# Check for collisions
hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
for hit in hits:
    score += 10

# Collectibles
collect_hits = pygame.sprite.spritecollide(player, collectibles, True)
for collect in collect_hits:
    if collect.type == 'health':
        player.health += 20
    elif collect.type == 'life':
        player.lives += 1

# Display score and health on screen
font = pygame.font.Font(None, 36)
score_text = font.render(f"Score: {score}", True, (0, 0, 0))
health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
screen.blit(score_text, (10, 10))
screen.blit(health_text, (10, 40))

##### game over and restart ######

def game_over_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, RED)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds
    
    # Restart or quit logic
    main()

def main():
    # Restart the game loop
    pass  # (Put the entire game loop code here again)

# Check if player is dead
if player.lives == 0:
    game_over_screen()




