from prototype_presets import *

# ----- Player class -----
""" Create the player class as a subclass of the pygame class pygame.sprite.Sprite """
class Player(pygame.sprite.Sprite):

    canWalljumpLeft = False
    canWalljumpRight = False
    leftWalljump = False
    rightWalljump = False

    """ Calls the constructor when the object is instantiated """
    def __init__(self):

        """ Calls the super method to override the parent's constructor method """
        super().__init__()

        # Create the player block
        width = 50
        height = 80
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Set values for player's change in distance attributes
        self.change_x = 0
        self.change_y = 0

    """ Create the gravity method to calculate gravity on player """
    def calc_grav(self):
        
        # Check if the player is at the bottom of the screen
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0 # Gravity keeps player on the ground
            self.isGrounded = True

        # Player is not grounded
        # Checks if player is falling from after max height
        elif self.change_y == 0:
            self.change_y = 1 # Player's fall speed
        else:
            self.change_y += .35 # Gravity effect on player in air
            self.isGrounded = False
    
    """ Create method to update the player """
    def update(self):

        """ Moves the player """
        # Gravity method is called
        self.calc_grav()

        # Walljump logic
        if self.change_y < 0:
            if self.leftWalljump:
                self.rect.x += 2
            elif self.rightWalljump:
                self.rect.x -= 2
        else:
            self.leftWalljump = False
            self.rightWalljump = False

        # Player moves horizontally
        self.rect.x += self.change_x
        
        # Check for collison detection
        # The side that collides with the block matches the blocks collided side

        # Check horizontal collison
        # Player will slide down a wall and can walljump off of it
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_y = 1
                self.canWalljumpRight = True
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_y = 1
                self.canWalljumpLeft = True

        # Player moves vertically
        self.rect.y += self.change_y

        # Checks for vertical collison
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.isGrounded = True
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            
            # Stop the player's vertical movement if there's a collison
            self.change_y = 0

    """ Calls method when user presses the right arrow key"""
    def go_right(self):
        self.change_x = 5

    """ Calls method when user presses the left arrow key"""
    def go_left(self):
        self.change_x = -5

    """ Calls method when user lets go of left or right arrow key"""
    def stop(self):
        self.change_x = 0

    """ Calls method when user presses the up arrow key"""
    def jump(self):

        # If user is grounded player can jump
        if self.isGrounded:
            self.change_y = -10
        elif self.canWalljumpRight:
            self.change_y = -10
            self.rightWalljump = True
            self.canWalljumpRight = False
        elif self.canWalljumpLeft:
            self.change_y = -10
            self.leftWalljump = True
            self.canWalljumpLeft = False

# ----- Platform class -----
""" Create the platform class as a subclass of pygame.sprite.Srpite """
class Platform(pygame.sprite.Sprite):

    """ Calls the constructor method when an object is instantiated """
    def __init__ (self, width, height):

        """ Calls the super method to override the parent's constructor method """
        super().__init__()

        # Create the platform block
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()


# ----- Level class -----
""" Create the level class """
class Level(object):

    """ Calls the constructor method when an object is instatinated """
    def __init__(self, player):

        # Keep track of objects and platforms in the level
        self.platform_list = pygame.sprite.Group()
        self.player = player

        # Create background surface
        self.background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT]) 

    """ Create a method to update the level """
    def update(self):
        self.platform_list.update()

    """ Create a method to build the level """
    def build(self, level):

        # Create platforms by calling the Platform class and add them to the platform list
        for platform in level:
            block = Platform(platform[2], platform[3])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.platform_list.add(block)

    """ Draw all sprites on the level """
    def draw(self, screen):
        
        # Draw the background and sprites on the level
        screen.fill(WHITE)
        self.platform_list.draw(screen)

# ----- Level subclasses -----
""" Create the levels as subclasses of Level """
class Level_01(Level):

    """ The constructor method is called whne the object is instantiated """
    def __init__(self, player):

        """ Call the parent constructor method """
        Level.__init__(self, player)

        # Give the level a name
        self.name = "Level 1"

        # Create a list of platforms in the level
        platforms = [[0, 200, 1000, 20]]
        
        # Pass the list of platfroms to the build method
        self.build(platforms) 

class Level_02(Level):

    """ The constructor method is called whne the object is instantiated """
    def __init__(self, player):

        """ Call the parent constructor method """
        Level.__init__(self, player)

        # Give the level a name
        self.name = "Level 2"

        # Create a list of platforms in the level
        platforms = [[300, 100, 200, 300]]

        # Pass the list of platfroms to the build method
        self.build(platforms) 
