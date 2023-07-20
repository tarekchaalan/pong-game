import pygame
import sys
import random
import time

# Basic settings
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
BALL_SPEED = 2
PADDLE_SPEED = {'Easy': 1.5, 'Medium': 2, 'Hard': 2.5}
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)

#Load audio files
clicksound = pygame.mixer.Sound('data\sounds\click_sound.mp3')
paddlehit = pygame.mixer.Sound('data\sounds\paddle_collision.mp3')
wallhit = pygame.mixer.Sound('data\sounds\wall_collision.mp3')
lifelost = pygame.mixer.Sound('data\sounds\life_lost.mp3')

# Load the player icon images and scale them down
one_player_img = pygame.image.load('data\images\player1.png')
one_player_img = pygame.transform.scale(one_player_img, (200, 200))  # change 50, 50 to the size you want

two_players_img = pygame.image.load('data\images\players2.png')
two_players_img = pygame.transform.scale(two_players_img, (200, 200))  # change 50, 50 to the size you want

LIFE_RADIUS = 10  # adjust this to change the size of the "lives" circles
LIVES_Y = HEIGHT - LIFE_RADIUS - 10  # y position of the "lives" circles

def draw_menu():
    # Fill the screen with a solid color to "erase" previous frames
    win.fill((0, 0, 0))  # Fill with black, or whatever your background color is

    # Blit the scaled images. You may need to adjust the position as well.
    win.blit(one_player_img, (WIDTH // 2 - 250, HEIGHT // 2 - 100))
    win.blit(two_players_img, (WIDTH // 2 + 25, HEIGHT // 2 - 100))
    pygame.display.update()

def draw_difficulty():
    # Fill the screen with a solid color to "erase" previous frames
    win.fill((0, 0, 0))  # Fill with black, or whatever your background color is

    easy_text = font.render('Easy', True, WHITE)
    medium_text = font.render('Medium', True, WHITE)
    hard_text = font.render('Hard', True, WHITE)

    win.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 3 - easy_text.get_height() // 2))
    win.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 - medium_text.get_height() // 2))
    win.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 3 * 2 - hard_text.get_height() // 2))

    pygame.display.update()

def select_difficulty():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                clicksound.play()

                if HEIGHT // 3 - 18 < y < HEIGHT // 3 + 18:
                    return 'Easy'
                elif HEIGHT // 2 - 18 < y < HEIGHT // 2 + 18:
                    return 'Medium'
                elif HEIGHT // 3 * 2 - 18 < y < HEIGHT // 3 * 2 + 18:
                    return 'Hard'

def select_players():
    draw_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                clicksound.play()
                # Check if the 1-player or 2-player image was clicked
                if WIDTH // 2 - 150 < x < WIDTH // 2 - 50 + 100 and HEIGHT // 2 - 50 < y < HEIGHT // 2 + 50:
                    # 1 player game
                    draw_difficulty()
                    difficulty = select_difficulty()
                    return 1, difficulty
                elif WIDTH // 2 + 50 < x < WIDTH // 2 + 150 + 100 and HEIGHT // 2 - 50 < y < HEIGHT // 2 + 50:
                    # 2 player game
                    pygame.time.delay(200)  # delay before entering the main game loop
                    return 2, 'Medium'

def draw_lives(lives1, lives2):
    for i in range(lives1):
        pygame.draw.circle(win, WHITE, (30 + i*30, LIVES_Y), LIFE_RADIUS)
    for i in range(lives2):
        pygame.draw.circle(win, WHITE, (WIDTH - 30 - i*30, LIVES_Y), LIFE_RADIUS)

def update_lives(ball, ball_dx, ball_dy, lives1, lives2, start_time):
    # Ball goes out of bounds
    if ball[0] - BALL_RADIUS < 0:
        lifelost.play()
        lives1 -= 1
        ball[0] = WIDTH // 2
        ball[1] = HEIGHT // 2
        ball_dx = 0  # Make the ball stationary
        ball_dy = 0  # Make the ball stationary
        start_time = pygame.time.get_ticks()  # Start the timer
    elif ball[0] + BALL_RADIUS > WIDTH:
        lifelost.play()
        lives2 -= 1
        ball[0] = WIDTH // 2
        ball[1] = HEIGHT // 2
        ball_dx = 0  # Make the ball stationary
        ball_dy = 0  # Make the ball stationary
        start_time = pygame.time.get_ticks()  # Start the timer
    return lives1, lives2, ball_dx, ball_dy, start_time

def display_winner(winner):
    win.fill((0, 0, 0))  # Fill with black
    winner_text = font.render(f'Player {winner} Wins!', True, WHITE)
    win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)  # delay 3 seconds

def main():
    players, difficulty = select_players()
    paddle_speed1 = 2  # constant speed for player 1
    paddle_speed2 = PADDLE_SPEED[difficulty]  # speed for player 2 or AI

    # Initialize game objects
    ball = [WIDTH // 2, HEIGHT // 2]
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = BALL_SPEED * random.choice([-1, 1])
    paddle1 = pygame.Rect(30, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH - PADDLE_WIDTH - 30, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    lives1 = lives2 = 5

    # Initialize a variable to hold the start time of the delay
    delay_start = 0
    start_time = 0
    is_delaying = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ball movement
        if not start_time or pygame.time.get_ticks() - start_time > 1000:
            ball[0] += ball_dx
            ball[1] += ball_dy

        # Delay ball movement if necessary
        if is_delaying and time.time() - delay_start > 2:
            is_delaying = False

        # Collision with top and bottom
        if ball[1] - BALL_RADIUS < 0 or ball[1] + BALL_RADIUS > HEIGHT - 40:
            ball_dy *= -1
            wallhit.play()

        # Collision with paddles
        if ball_dx < 0 and paddle1.right > ball[0] > paddle1.left and paddle1.top < ball[1] < paddle1.bottom or \
           ball_dx > 0 and paddle2.left < ball[0] < paddle2.right and paddle2.top < ball[1] < paddle2.bottom:
            ball_dx *= -1
            paddlehit.play()

        # Move the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.move_ip(0, -paddle_speed1)
        if keys[pygame.K_s]:
            paddle1.move_ip(0, paddle_speed1)

        # Player 2 or AI Movement
        if players == 2:
            if keys[pygame.K_UP]:
                paddle2.move_ip(0, -paddle_speed2)
            if keys[pygame.K_DOWN]:
                paddle2.move_ip(0, paddle_speed2)
        else:
            # AI Movement
            if ball[0] > WIDTH // 2:  # if ball is on the right side of the screen
                if paddle2.centery < ball[1]:
                    paddle2.move_ip(0, paddle_speed2)
                else:
                    paddle2.move_ip(0, -paddle_speed2)

        # Ensure paddles aren't out of screen
        if paddle1.top < 0: paddle1.top = 0
        if paddle1.bottom > HEIGHT - 40: paddle1.bottom = HEIGHT - 40
        if paddle2.top < 0: paddle2.top = 0
        if paddle2.bottom > HEIGHT - 40: paddle2.bottom = HEIGHT - 40

        if start_time != 0 and pygame.time.get_ticks() - start_time > 1000:
            ball_dx = BALL_SPEED if ball[0] < WIDTH // 2 else -BALL_SPEED  # Start the ball moving again
            ball_dy = BALL_SPEED * random.choice([-1, 1])  # Set the y-direction of the ball
            start_time = 0  # Reset the start time

        lives1, lives2, ball_dx, ball_dy, start_time = update_lives(ball, ball_dx, ball_dy, lives1, lives2, start_time)

        if lives1 == 0:
            display_winner(2)
            break
        elif lives2 == 0:
            display_winner(1)
            break

        # Drawing everything
        win.fill((0, 0, 0))
        pygame.draw.rect(win, WHITE, paddle1)
        pygame.draw.rect(win, WHITE, paddle2)
        pygame.draw.circle(win, WHITE, ball, BALL_RADIUS)
        pygame.draw.line(win, WHITE, (0, 560), (800, 560), 1)
        draw_lives(lives1, lives2)
        pygame.display.update()

        # Frame rate
        pygame.time.delay(10)

if __name__ == '__main__':
    main()
