import pygame, sys, math, random


# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap


def player_delay(clock, time, counter, player):
    counter += clock.tick()
    if counter >= time:
        print('thing')
        player.animate()
        counter = 0


# A basic Sprite class that can draw itself, move, and test collisions
class Sprite:
    def __init__(self, image):
        self.image = image
        self.display_image = self.image[0]
        self.rectangle = image[0].get_rect()
        self.mask = pygame.mask.from_surface(image[0])
        self.left_foot = False
        self.anim_counter = 0

        # xp accumulator variable
        self.xp_counter = 0

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.display_image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

    def animate(self):
        if self.anim_counter == len(self.image):
            self.anim_counter = 0
        self.display_image = self.image[self.anim_counter]
        self.anim_counter += 1

    # level will make it easier to have specific affects (astetic or not) take place in a trackable and adjustable situation
    def Level(self):
        self.xp_counter += self.xp_counter + 1
        if self.xp_counter < 10:
            self.speed = (self.speed[0] - 1, self.speed[1] - 1)
        else:
            self.LevelUp

    def LevelUp(self):
        self.speed = (self.speed[0] + 10, self.speed[1] + 10)


class Enemy:
    def __init__(self, image, width, height, vx, vy):
        # starter Code
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        # places the enemy in a random location on the world space
        self.rectangle.center = (random.randint(50, width - 50), random.randint(50, height - 50))

        # sets a starting velocity
        self.speed = (vx, vy)
        # Add code to
        # 1. Set the rectangle center to a random x and y based
        #    on the screen width and height
        # 2. Set a speed instance variable that holds a tuple (vx, vy)
        #    which specifies how much the rectangle moves each time.
        #    vx means "velocity in x".

    def move(self):
        self.rectangle.move_ip(self.speed[0], self.speed[1])

        # Add code to move the rectangle instance variable in x by
        # the speed vx and in y by speed vy. The vx and vy are the
        # components of the speed instance variable tuple.
        # A useful method of rectangle is pygame's move_ip method.
        # Research how to use it for this task.

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
        # This method makes the enemy bounce off of the top/left/right/bottom
        # of the screen. For example, if you want to check if the object is
        # hitting the left side, you can test
        # if self.rectangle.left < 0:
        # The rectangle.left tests the left side of the rectangle. You will
        # want to use .right .top .bottom for the other sides.
        # The height and width parameters gives the screen boundaries.
        # If a hit of the edge of the screen is detected on the top or bottom
        # you want to negate (multiply by -1) the vy component of the speed instance
        # variable. If a hit is detected on the left or right of the screen, you
        # want to negate the vx component of the speed.
        # Make sure the speed instance variable is updated as needed.

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)


class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(50, width - 50), random.randint(50, height - 50))

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
    enemy = pygame.image.load("Pixeled bomb v1.png").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []

    for i in range(15):
        if random.randint(0, 1):
            enemy_sprites.append(Enemy(enemy_image, 600, 600, random.randint(1, 3), random.randint(1, 3)))
        else:
            enemy_sprites.append(Enemy(enemy_image, 600, 600, random.randint(-3, -1), random.randint(-3, -1)))

    # This is the character you control. Choose your image.
    player_image1 = pygame.image.load("LF1.png").convert_alpha()
    player_image2 = pygame.image.load("RF-1.png").convert_alpha()
    player_sprite = Sprite([player_image1, player_image2])
    life = 3

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("Burger.png").convert_alpha()
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []
    powerups.append(PowerUp(powerup_image, 600, 600))

    clock = pygame.time.Clock()
    anim_counter = 0

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing and life > 0:  # while is_playing is True, repeat
        # Modify the loop to stop when life is <= to 0.

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        if anim_counter > 1000:
            player_sprite.animate()
            anim_counter = 0
        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.

        for i in enemy_sprites:
            if pixel_collision(player_sprite.mask, player_sprite.rectangle, i.mask, i.rectangle):
                life -= 0.5
                enemy_sprites.remove(i)
                del i
                enemy_sprites.append(Enemy(enemy_image, 600, 600, random.randint(-3, 3), random.randint(-3, 3)))

            # Loop over the powerups. If the player sprite is colliding, add
            # 1 to the life.

            for i in powerups:
                if pixel_collision(player_sprite.mask, player_sprite.rectangle, i.mask, i.rectangle):
                    life += 1

                    # player_sprite.Level()
                    # print(player_sprite.xp_counter)

            # Make a list comprehension that removes powerups that are colliding with
            # the player sprite.
            for i in powerups:
                if pixel_collision(player_sprite.mask, player_sprite.rectangle, i.mask, i.rectangle):
                    powerups.remove(i)

        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for i in enemy_sprites:
            i.bounce(width, height)
            i.move()

        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        if len(powerups) < 2:
            for i in range(1):
                x = random.randint(1, 300)
                if x == random.randint(1, 100):
                    for i in range(1):
                        powerups.append(PowerUp(powerup_image, 600, 600))

        # Erase the screen with a background color
        screen.fill((0, 100, 50))  # fill the window with a color

        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Money: " + str('%.1f' % life)
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))

        level = "Level: " + str('%.1f' % life)
        label = myfont.render(level, True, (255, 255, 0))
        screen.blit(label, (400, 20))
        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        anim_counter += 20
        pygame.time.wait(20)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(20)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
