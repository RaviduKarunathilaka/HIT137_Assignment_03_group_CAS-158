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

### creating player classes ####
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the image of the player (replace 'hero_image.png' with your actual image file)
        self.image = pygame.image.load('hero_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image if needed

        # Set the initial position of the player at middle left of the screen
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT // 2)  # Middle-left position of the screen
        self.speed_x = 0  # Horizontal speed initialized to 0
        self.speed_y = 0  # Vertical speed initialized to 0
        self.speed = 5  # Movement speed
        self.health = 100  # health
        self.lives = 3  # lives

    def update(self):
        # Update the player's position based on current speed (speed_x and speed_y)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ensure the player stays within screen boundaries (left, right, top, bottom)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH  # Prevent moving past the right edge
        if self.rect.left < 0:
            self.rect.left = 0  # Prevent moving past the left edge
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT  # Prevent moving past the bottom edge
        if self.rect.top < 0:
            self.rect.top = 0  # Prevent moving past the top edge

    # Move the player left by setting the horizontal speed
    def move_left(self):
        self.speed_x = -self.speed

    # Move the player right by setting the horizontal speed
    def move_right(self):
        self.speed_x = self.speed

    # Move the player up by setting the vertical speed
    def move_up(self):
        self.speed_y = -self.speed

    # Move the player down by setting the vertical speed
    def move_down(self):
        self.speed_y = self.speed

    # Stop horizontal movement (reset horizontal speed to 0)
    def stop_horizontal(self):
        self.speed_x = 0

    # Stop vertical movement (reset vertical speed to 0)
    def stop_vertical(self):
        self.speed_y = 0

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

### Main game loop ###
# Constants for enemy spawning
ENEMY_SPAWN_TIME = 2000  # 2 seconds for enemy spawn timer
pygame.time.set_timer(pygame.USEREVENT, ENEMY_SPAWN_TIME)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()  # Group for enemies
projectiles = pygame.sprite.Group()  # Group for projectiles
collectibles = pygame.sprite.Group()  # Group for collectibles

player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Spawn an enemy every time the timer event occurs
        if event.type == pygame.USEREVENT:
            # Spawn an enemy at a random position on the right side
            enemy_x = WIDTH - 40
            enemy_y = random.randint(0, HEIGHT - 40)
            enemy = Enemy(enemy_x, enemy_y, player)
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Handle movement
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop_horizontal()

    if keys[pygame.K_UP]:
        player.move_up()
    elif keys[pygame.K_DOWN]:
        player.move_down()
    else:
        player.stop_vertical()

    # Fire projectile when pressing 'Z'
    if keys[pygame.K_z]:
        projectile = Projectile(player.rect.centerx, player.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

    # Update game logic
    all_sprites.update()

    # Check for projectile-enemy collisions
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)

    # Drawing
    screen.fill(WHITE)  # Fill the screen with a white background
    all_sprites.draw(screen)  # Draw all sprites

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




