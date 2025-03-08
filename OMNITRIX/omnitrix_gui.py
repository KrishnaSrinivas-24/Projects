import pygame

# Initialize Pygame
pygame.init()

# Screen Settings
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OMNITRIX AI")

# Load Omnitrix Image
omnitrix_img = pygame.image.load('omnitrix.png')
omnitrix_img = pygame.transform.scale(omnitrix_img, (200, 200))  

# Omnitrix Position (Centered)
x, y = WIDTH // 2 - 100, HEIGHT // 2 - 100

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Pulse Animation State
pulse = False

# Function to Update Pulse State
def update_pulse(state):
    global pulse
    pulse = state

# Main Loop
running = True
while running:
    pygame.time.delay(30)
    screen.fill(BLACK)

    # Draw Pulsing Circles When Speaking
    if pulse:
        for i in range(3):  
            pygame.draw.circle(screen, GREEN, (WIDTH // 2, HEIGHT // 2), 100 + (i * 10), 2)

    # Draw Omnitrix Symbol
    screen.blit(omnitrix_img, (x, y))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
