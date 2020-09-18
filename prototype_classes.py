from prototype_presets import *

# ----- Player class -----
""" Create the player class as a subclass of the pygame class pygame.sprite.Sprite """
class Player(pygame.sprite.Sprite):

    isGrounded = False
    jumpBoost = False
    slideBoost = False

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
        
        # If player is at the bottom of the screen they die
        # Player is placed back to the start of the level
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.x = 10
            self.rect.y = 0
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

        # When player falls they can no longer walljump
        if self.change_y > 0:
            self.canWalljumpRight = False
            self.canWalljumpLeft = False

        # Halts horizontal movement from walljump when player hits the ground
        if self.isGrounded and self.change_x == 2 or self.isGrounded and self.change_x == -2:
            self.stop()

        # Check for slide boost
        if self.slideBoost:
            if self.change_x == 5:
                self.change_x += 5
            elif self.change_x == -5:
                self.change_x -= 5
        
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
                self.slideBoost = False
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_y = 1
                self.canWalljumpLeft = True
                self.slideBoost = False
            
        # Checks for jump boost
        if self.jumpBoost:
            self.change_y = -15
            self.jumpBoost = False
            
        # Player moves vertically
        self.rect.y += self.change_y

        # Checks for vertical collison
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                # If the player jumps on a slime block they get a jump boost
                if block.type == "jump":
                    self.jumpBoost = True
                else:
                    self.isGrounded = True
                if block.type == "slide":
                    self.slideBoost = True
                else:
                    self.slideBoost = False
            elif self.change_y < 0:
                if block.type == "acid":
                    self.rect.x = 10
                    self.rect.y = 20
                else:
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
            self.change_x = -2
            self.canWalljumpRight = False
            self.haltWalljump = True
        elif self.canWalljumpLeft:
            self.change_y = -10
            self.change_x = 2
            self.canWalljumpLeft = False
            self.haltWalljump = True

# ----- Platform class -----
""" Create the platform class as a subclass of pygame.sprite.Srpite """
class Platform(pygame.sprite.Sprite):

    """ Calls the constructor method when an object is instantiated """
    def __init__ (self, width, height):

        """ Calls the super method to override the parent's constructor method """
        super().__init__()

        # Create the platform block
        self.image = pygame.Surface([width, height])
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
            block.type = platform[4]
            if block.type == "normal":
                block.image.fill(BLACK)
            elif block.type == "jump":
                block.image.fill(PURPLE)
            elif block.type == "acid":
                block.image.fill(GREEN)
            else:
                block.image.fill(ORANGE)
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

    """ The constructor method is called when the object is instantiated """
    def __init__(self, player):

        """ Call the parent constructor method """
        Level.__init__(self, player)

        # Give the level a name
        self.name = "Level 1"

        # Create a list of platforms in the level
        platforms = [[  0, 490, 1000, 10,   "jump"],
                     [100, 202,  100, 20,   "acid"],
                     [  0, 200, 1000, 20, "normal"]]
        
        # Pass the list of platfroms to the build method
        self.build(platforms)

class Level_02(Level):

    """ The constructor method is called when the object is instantiated """
    def __init__(self, player):

        """ Call the parent constructor method """
        Level.__init__(self, player)

        # Give the level a name
        self.name = "Level 2"

        # Create a list of platforms in the level
        platforms = [[  0, 490, 900,  10,  "slide"],
                     [300,  90, 200, 300, "normal"],
                     [ -1, 200,   1,  20, "normal"]]

        # Pass the list of platfroms to the build method
        self.build(platforms) 
