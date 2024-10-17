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
BLACK = (0, 0, 0)

# Defining a timer for enemy spawning
ENEMY_SPAWN_TIME = 2000  # 2 seconds
pygame.time.set_timer(pygame.USEREVENT, ENEMY_SPAWN_TIME)

# Create screen window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D game window")

# Set the frame rate
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 74)

### Function to Draw Health Bars ###
def draw_health_bar(surf, x, y, current_health, max_health, bar_length, bar_height):
    # Calculate the health bar 
    health_ratio = current_health / max_health
    fill_width = int(bar_length * health_ratio)
    
    # Draw the background of the health bar (black)
    pygame.draw.rect(surf, BLACK, (x, y, bar_length, bar_height))
    
    # Draw the filled portion of the health bar
    if health_ratio > 0.5:
        pygame.draw.rect(surf, GREEN, (x, y, fill_width, bar_height))
    else:
        pygame.draw.rect(surf, RED, (x, y, fill_width, bar_height))

### Player Class ###
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the image of the player 
        self.image = pygame.image.load('hero_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image

        # Set the initial position of the player at middle left of the screen
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT // 2) 
        self.speed_x = 0  # Horizontal speed initialized to 0
        self.speed_y = 0  # Vertical speed initialized to 0
        self.speed = 5  # Movement speed
        self.health = 100  # Player's health
        self.max_health = 100  # Max health of player
        self.lives = 3  # Player's lives

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

    def move_left(self):
        self.speed_x = -self.speed

    def move_right(self):
        self.speed_x = self.speed

    def move_up(self):
        self.speed_y = -self.speed

    def move_down(self):
        self.speed_y = self.speed

    def stop_horizontal(self):
        self.speed_x = 0

    def stop_vertical(self):
        self.speed_y = 0

    def draw_health(self, surf):
        # Draw health bar below the player sprite
        draw_health_bar(surf, self.rect.x, self.rect.y + 55, self.health, self.max_health, 50, 5)

### Projectile Class ###
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

### Enemy Class ###
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target, level):
        super().__init__()

        self.image = pygame.image.load('dragon_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))  # Resize the image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])  # Enemies move either left or right
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])
        self.target = target

        # Adjust enemy health based on level
        self.level = level
        if self.level == 1:
            self.health = 1  # 1 shot to kill
            self.max_health = 1
        elif self.level == 2:
            self.health = 5  # 5 shots to kill
            self.max_health = 5
        elif self.level == 3:
            self.health = 10  # 10 shots to kill
            self.max_health = 10

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

        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove enemy when health is 0

    def draw_health(self, surf):
        # Draw health bar above the enemy sprite
        draw_health_bar(surf, self.rect.x, self.rect.y - 10, self.health, self.max_health, 50, 5)

### Camera Class ###
class Camera:
    def __init__(self):
        self.offset = 0

    def apply(self, rect):
        return rect.move(self.offset, 0)

    def update(self, target):
        self.offset = -target.rect.centerx + WIDTH // 2

camera = Camera()

### Game Over Screen ###
def game_over_screen(won):
    screen.fill(WHITE)
    if won:
        text = large_font.render("Congratulations, you won!", True, GREEN)
    else:
        text = large_font.render("GAME OVER", True, RED)
    
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds

    pygame.quit()  # Quit after showing the game over screen

### Main game loop ###
score = 0  # Initialize the score variable
level = 1  # Initialize the level variable

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()  # Group for enemies
projectiles = pygame.sprite.Group()  # Group for projectiles

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
            # Spawn enemies at random positions on the right side based on level
            enemy_x = WIDTH - 40
            enemy_y = random.randint(0, HEIGHT - 40)
            enemy = Enemy(enemy_x, enemy_y, player, level)  # Pass level to enemy
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
    hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)  # Enemy and projectile collision

    for enemy, projectiles_hit in hits.items():
        for projectile in projectiles_hit:
            enemy.take_damage()  # Enemy takes damage on hit
            if enemy.health <= 0:
                score += 10  # Increase score when enemy dies

    # Check for player-enemy collisions
    player_hits = pygame.sprite.spritecollide(player, enemies, False)  # Check if player collides with any enemies
    if player_hits:
        player.health -= 10  # Reduce player health upon collision
        for enemy in player_hits:
            enemy.kill()  # Remove enemy on collision

    # Check if player won (reached 400 points)
    if score >= 400:
        game_over_screen(True)  
        running = False  # End the game after winning

    # Clear the screen by filling it with white color
    screen.fill(WHITE)

    # Draw everything
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    # Display score, health, and lives
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Render score
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))  # Render health
    lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))  # Render lives

    screen.blit(score_text, (10, 10))  # Position score at top-left corner
    screen.blit(health_text, (10, 40))  # Position health below score
    screen.blit(lives_text, (10, 70))  # Position lives below health

    # Draw health bars for player and enemies
    player.draw_health(screen)
    for enemy in enemies:
        enemy.draw_health(screen)

    # Level progression logic
    if score >= 50:  # Example: level 2 at 50 points
        level = 2
    if score >= 100:  # Example: level 3 at 100 points
        level = 3

    pygame.display.flip()

    # Check if player is out of lives or health
    if player.health <= 0:
        game_over_screen(False)  # Call game over screen with 'won' as False
        running = False  # End the game loop

pygame.quit()