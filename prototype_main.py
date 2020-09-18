from prototype_classes import *

# Display the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


# Display the title in the window
pygame.display.set_caption("Prototype")

# Instantiate the player object
player = Player()

# Instantiate the level object and append them to a list
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))

# Set the current level to the first level
current_level_no = 0
current_level = level_list[current_level_no]
player.level = current_level

# Add the player to an active sprite list
active_sprite_list = pygame.sprite.Group()
active_sprite_list.add(player)

# Set starting position for the player
player.rect.x = 10
player.rect.y = 0

# Create a clock for game timing
clock = pygame.time.Clock()

done = False

# ----- Main Program Loop -----
while not done:

    # ----- Input Stage -----
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:       # User clicked close
            done = True                     # Breaks out of main program loop
            
        # User presses a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                player.go_left()
            if event.key == pygame.K_RIGHT: 
                player.go_right()           
            if event.key == pygame.K_UP:
                player.jump()

        # User lets go of key      
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0 or event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()
            if event.key == pygame.K_UP:
                player.canWalljump = False

    # ---- Logic Stage -----
    # Update the player
    active_sprite_list.update()

    # Update platforms in the level
    current_level.update()

    # If player crosses the left side of the screen (not on the first level), go back a level
    if player.rect.x < 0:
        if current_level_no != 0:
            current_level_no -= 1
            player.rect.x = 950
        else:
            player.rect.x = 0

    # If player crosses the right side of the screen (not on the last level), go to next level
    if player.rect.x > 950:
        if current_level_no != len(level_list) - 1:
            current_level_no += 1
            player.rect.x = 0
        else:
            player.rect.x = 950

    # Stop player from going above the screen
    if player.rect.y < 0:
        player.rect.y = 0

    # Set the player in the current level
    current_level = level_list[current_level_no]
    player.level = current_level

    # ----- Draw Stage -----
    # Draw the current level
    current_level.draw(screen)

    # Draw the active sprites
    active_sprite_list.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Wipe the screen for the next iteration
    pygame.display.flip()

# Quits after main program loop
pygame.quit()
