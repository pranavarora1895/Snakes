import pygame
import random
import os

# Setting up the music
pygame.mixer.init()
# Setting the game window
screen_width = 900
screen_height = 600
pygame.init()  # Initializes the pygame engine
gameWindow = pygame.display.set_mode((screen_width, screen_height))  # Opens the Game Window
# Setting up bg image
welcome_bg_image = pygame.image.load('welcome_bg.jpg')
welcome_bg_image = pygame.transform.scale(welcome_bg_image, (screen_width, screen_height)).convert_alpha()
gameover_bg_image = pygame.image.load('game_over_bg.jpg')
gameover_bg_image = pygame.transform.scale(gameover_bg_image, (screen_width, screen_height)).convert_alpha()
# Setting colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
pygame.display.set_caption("Python Snakes")  # Setting Game Heading
pygame.display.update()

# Creating the Clock
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('chiller', 50)


# Defining the Functions

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))


# Snake Plot
def plot_snake(gameWindow, color, snake_list, size1, size2):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, size1, size2])


# Creating a Welcome Screen
def welcome_screen():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcome_bg_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('bg_song.mp3')
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('bg_song.mp3'))
                    gameloop()
        pygame.display.update()
        clock.tick(fps)


# Creating a Game Loop
def gameloop():
    # Snake
    snake_x = 45
    snake_y = 55
    snake_size = 20
    velocity_x, velocity_y = 0, 0
    init_velocity = 5
    snake_list = []
    snake_length = 1
    exit_game = False
    game_over = False
    # Food
    food_x = random.randint(20, screen_width / 1.5)
    food_y = random.randint(20, screen_height / 1.5)
    score = 0
    # Getting High Score
    # Check if HighScore file exists
    if (not os.path.exists('highscore.txt')):
        with open('highscore.txt', 'w') as f:
            f.write('0')
    with open('highscore.txt', 'r') as f:
        hiscore = f.read()

    while not exit_game:  # it doesnt lets the game to close
        if game_over:
            gameWindow.fill(white)
            gameWindow.blit(gameover_bg_image, (0, 0))
            with open('highscore.txt', 'w') as f:
                f.write(str(hiscore))
            for event in pygame.event.get():  # logs the events
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handling Quit Event
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    # CheatCodes
                    if event.key == pygame.K_SPACE:
                        velocity_x = 0
                        velocity_y = 0
                    if event.key == pygame.K_q:
                        score += 10
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # When Snake eats the food
            if abs(food_x - snake_x) < 12 and abs(food_y - snake_y) < 12:
                pygame.mixer.music.load('beep.mp3')
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('beep.mp3'))
                score += 10
                food_x = random.randint(40, screen_width / 2)
                food_y = random.randint(40, screen_height / 2)
                snake_length += 5
                if score > int(hiscore):
                    hiscore = str(score)
            gameWindow.fill(black)
            text_screen("Score: " + str(score) + "High Score: " + hiscore, yellow, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
                game_over = True
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
                game_over = True
            plot_snake(gameWindow, green, snake_list, snake_size, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


if __name__ == '__main__':
    welcome_screen()
