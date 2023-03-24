#By Charlie Sinclair and Connor Patterson

# You are a nobody trying to make it in the crime world, can you avoid the cops and become the Godfather?



# How to Play:
#   Use mouse to move the character
#   Collect Money Bags and rise through the crime world
#   Avoid the Cops
#   If you touch a cop, you need to pay money, if you don't have enough money then you get arrested and you lose














import pygame, sys, math, random

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap


# A basic Sprite class that can draw itself, move, and test collisions
class Sprite:
    def __init__(self, image, other_image):
        self.image = image
        self.other_image = other_image
        self.display_image = self.image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        self.left_foot = False
        self.current_level = 0
        self.speed = (15, 15)


        # xp accumulator variable
        self.xp_counter = 0

    def set_position(self, new_position): # set position of player
        self.rectangle.center = new_position

    def draw(self, screen): # draw on screen
        screen.blit(self.display_image, self.rectangle)

    def is_colliding(self, other_sprite): # check if colliding
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

    def animate(self): # Change animation sprite
        if self.left_foot:
           self.left_foot = False
           self.display_image = self.other_image

        else:
            self.left_foot = True
            self.display_image = self.image



    # level will make it easier to have specific affects (astetic or not) take place in a trackable and adjustable situation
    def Level(self):
        self.xp_counter += random.randint(1, 4)
        if self.xp_counter < 10:
            self.speed = (self.speed[0] - 1, self.speed[1] - 1)
        else:
            self.LevelUp()
            self.xp_counter = 0

    def LevelUp(self):
        self.speed = (self.speed[0] + 10, self.speed[1] + 10)
        self.current_level += 1


class Enemy:
    def __init__(self, image1, image2, width, height, vx, vy):
        # starter Code
        self.image1 = image1
        self.image2 = image2
        self.mask = pygame.mask.from_surface(image1)
        self.rectangle = image1.get_rect()
        self.display_image = image1
        self.left_foot = False

        # places the enemy in a random location on the world space
        self.rectangle.center = (random.randint(50, width - 50), random.randint(50, height - 50))

        # sets a starting velocity
        self.speed = (vx, vy)


    # Move
    def move(self):
        self.rectangle.move_ip(self.speed[0], self.speed[1])

    # Bounce on the edge of the screen
    def bounce(self, width, height):
        if self.rectangle.left < 0:
            self.speed = (self.speed[0] * -1, self.speed[1])
            counter = 0
            current_x = self.rectangle.left
            while current_x < 0:
                current_x += 1
                counter += 1
                if current_x == 0:
                    break
            self.rectangle.move_ip(counter, 0)
        elif self.rectangle.right > width:
            self.speed = (self.speed[0] * -1, self.speed[1])
            counter = 0
            current_x = self.rectangle.right
            while current_x > width:
                current_x -= 1
                counter -= 1
            self.rectangle.move_ip(counter, 0)

        if self.rectangle.top < 0:
            self.speed = (self.speed[0], self.speed[1] * -1)
            counter = 0
            current_y = self.rectangle.top
            while current_y < 0:
                current_y += 1
                counter += 1
            self.rectangle.move_ip(0, counter)
        elif self.rectangle.bottom > height:
            self.speed = (self.speed[0], self.speed[1] * -1)
            counter = 0
            current_y = self.rectangle.bottom
            while current_y > height:
                current_y -= 1
                counter -= 1
            self.rectangle.move_ip(0, counter)

    def draw(self, screen):
        screen.blit(self.display_image, self.rectangle)

    def animate(self):
        if self.left_foot:
            self.left_foot = False
            self.display_image = self.image2
        else:
            self.left_foot = True
            self.display_image = self.image1


class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        # Default code
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        self.rectangle.center = (random.randint(50, width - 80), random.randint(50, height - 80)) # place the money bag in a random location

        self.money = random.randint(1, 30) # set a money amount

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)

def main():
    # Setup pygame
    pygame.init()

    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode((width, height))

    # Load image assets
    # Choose your own image
    enemy1 = pygame.image.load("cop_left_Foot.png").convert_alpha()
    enemy2 = pygame.image.load("cop_right_foot.png").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image1 = pygame.transform.smoothscale(enemy1, (50, 50))
    enemy_image2 = pygame.transform.smoothscale(enemy2, (50, 50))

    enemy_sprites = []

    # Create police
    for i in range(20):
        if random.randint(0, 1):
            enemy_sprites.append(Enemy(enemy_image1, enemy_image2, 600, 600, random.randint(1, 3), random.randint(1, 3)))
        else:
            enemy_sprites.append(Enemy(enemy_image2, enemy_image1, 600, 600, random.randint(-3, -1), random.randint(-3, -1)))

    # This is the character you control. Choose your image.

    # Load animation images
    player_image1 = pygame.image.load("LF_BG1.png").convert_alpha()
    player_image2 = pygame.image.load("RF_BG-1.png").convert_alpha()

    # Resize images
    player_image1 = pygame.transform.smoothscale(player_image1, (40, 40))
    player_image2 = pygame.transform.smoothscale(player_image2, (40, 40))
    player_sprite = Sprite(player_image1, player_image2) # create an object
    life = 20 # money in game

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("Money_Bag.png").convert_alpha()
    powerup_image1 = pygame.transform.smoothscale(powerup_image, (80, 80))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    # Load music
    pygame.mixer.music.load("Gangsta Music.ogg", 'ogg') # Credit to: Michael Hunter

    # Set the animation timer
    anim_counter = 0

    # Main part of the game
    is_playing = True

    # Play music
    pygame.mixer.music.play(-1)
    while is_playing and life > 0:

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Check to see if the animation timer is up
        if anim_counter > 500:
            player_sprite.animate()
            for i in enemy_sprites:
                i.animate()
            anim_counter = 0
        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.


        # Check if Police have collided with player
        for i in enemy_sprites:
            if pixel_collision(player_sprite.mask, player_sprite.rectangle, i.mask, i.rectangle):
                life -= random.randint(1, 4) # Pay bribe


        # Check to see if Player is next to a money bag
        for i in powerups:
            if pixel_collision(player_sprite.mask, player_sprite.rectangle, i.mask, i.rectangle):
                life += i.money
                player_sprite.Level() # Add xp to the player
                powerups.remove(i)


        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for i in enemy_sprites:
            i.bounce(width, height)
            i.move()



        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        if len(powerups) < 4:
            if random.randint(1, 100) == random.randint(1, 100):
                powerups.append(PowerUp(powerup_image, 600, 600))

        # Erase the screen with a background color
        screen.fill((0,100,50)) # fill the window with a color

        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the money to the screen.
        text = "Money: $" + str(life)
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))

        # Write the player's level to the screen
        level = "Level " + str(player_sprite.current_level)
        if player_sprite.current_level == 0:
            level += ' nobody'

        elif player_sprite.current_level > 0 and player_sprite.current_level < 5:
            level += ' Crook'

        elif player_sprite.current_level >= 5 and player_sprite.current_level < 20:
            level += ' Theif'

        elif player_sprite.current_level >= 20 and player_sprite.current_level < 50:
            level += ' Cook'

        elif player_sprite.current_level >= 50 and player_sprite.current_level < 75:
            level += ' Enforcer'

        elif player_sprite.current_level >= 75 and player_sprite.current_level < 100:
            level += ' Fixer'

        elif player_sprite.current_level >= 100 and player_sprite.current_level < 500:
            level += ' Boss'

        elif player_sprite.current_level >= 500 and player_sprite.current_level < 1000:
            level += ' Big Boss'

        else:
            level += ' Godfather'
        label = myfont.render(level, True, (255, 255, 0))
        screen.blit(label, (300, 20))

        # Write the player's XP to the screen
        xp_txt = "XP: " + str(player_sprite.xp_counter) + '/10'
        label = myfont.render(xp_txt, True, (255, 255, 0))
        screen.blit(label, (20, 50))


        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        anim_counter += 20
        pygame.time.wait(20)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
