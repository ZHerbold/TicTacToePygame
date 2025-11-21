'''
Zander Herbold - First created on 4/19/2025
Last updated on 4/28/2025

This is the pygame version of my previous text based tic-tac-toe

Planned Updates:
- None for now

Updates:
V1.5.0 - Update 5
- Added button to go back to title screen.
- Added protection for repeated names
- Changed the location of the reset button
- Moved the title screen code into a function

V1.4.0 - Update 4
- UI UPDATE
- Remade the UI for both the title/userinput screen and the main game screen
- Remade the UI into dark theme to make it easy on the eyes and remade the x and o shapes and the lines.
- Made the reset font red to tell players to avoid clicking it for fun

V1.3.0 - Update 3
- Added planned updates information in the docstring. The information in there has not been added in the game yet.
- Changed how saving works
- Now tracks who plays against who and their scores
    - EX: Zander plays against John, saved as a dictionary value inside of a dictionary
    - New naming scheme, will need to proof it against two of the same name because John vs John will not work
    - The Johns will need to agree on something to differenate themselves for now
    - Currently goes {name1Vname2:{name1:0,ties:0,name2:0}}
- Saves are alphabetical so while the first name goes first in the game, it will not create a new entry in the save file if it was the second name before
    - EX Zander goes first last time, replays and goes second this time, will use the same save file while maintaining the order of play
    - This gives players more freedom to choose who to go first without worrying about losing scores
- Ties are no longer universal
- Blocked tab from being registered as a key press because of my habit of tabbing into the next entry field (maybe as a later feature)

V1.2.0 - Update 2
- Added player names entry field
- Added comfirmation button (green button)
- Changed save file from save.txt to save.json
- Added the ability to track each player's total win based on name

V1.1.0 - Update 1
- Added information about updates in the docstring
- Added save file
- New variables to track total wins per player and ties
- New text to let players know current score (wins and ties)
- Added button to reset the score

V1.0.1 - Revision 1
- Reformatted code for easier readability
- Added comments

V1.0.0 - Release version
- Added Tic Tac Toe gameplay
- Added Tic Tac Toe logic
- Added Replay and quit buttons
- Added text informing player whose turn it is and who wins or ties
- Added images and font
'''

# imports the pygame module
import pygame
import json

# starts all the pygame modules
pygame.init()

# INPUT FUNCTION
def playerInput():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            global mouseclick
            mouseclick = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Enter Key Pressed")
            elif event.key == pygame.K_BACKSPACE:
                return "BACKSPACE"
            elif event.key == pygame.K_TAB:
                pass # do nothing
                # this is here because I kept pressing tab while trying to go to the next text box
            else:
                return event.unicode
    return ""

#FONTS
# loads a font
game_font = pygame.font.Font('BrownieStencil.ttf', 50)
win_font = pygame.font.Font('BrownieStencil.ttf', 20)

# loads all images used for tic tac toes (the lines and the x and o) and the title menu
menu_image = pygame.image.load("TicTacToeMenu.png")
tic_tac_toe_lines = pygame.image.load("Tic-tac-toe.png")
letter_x = pygame.image.load("X_letter.png")
letter_o = pygame.image.load("O_letter.png")

# various variable for game to use
# variable to make the game loop run
playing = 'y'
clock = pygame.time.Clock()

player1_name = ""
player2_name = ""
total_ties = "TIES"
player1_wins = 0
player2_wins = 0
ties = 0
wins = []
player_game = ""
player1 = ""
player2 = ""

# DISPLAY
# Screen height and width setting (Don't change until I figure out a good way to scale the tic tac toe images)
SCREEN_HEIGHT = 750
SCREEN_WIDTH = 600

# sets the size of the tic tac toe rectangles. It's currently -150 to screen height because I'm leaving space for text and buttons at the bottom
rect_size = (SCREEN_WIDTH/3,(SCREEN_HEIGHT-150)/3)

# creates a Surface to display everything on and sets it to a preset size
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Creates the input fields
input_field_rect1 = pygame.Rect((110,250),(300,30))
input_field_rect2 = pygame.Rect((180,400),(300,30))
ok_field = pygame.Rect((330,620),(235,96))

# START OF MENU FUNCTION
def menu():
    screen.blit(menu_image,(0,0))
    # SAVE INFO
    # access the save info variables
    global player1_name
    global player2_name
    global total_ties
    global mouseclick
    global wins
    global player_game
    global player1
    global player2
    
    screen.fill("white",input_field_rect1)
    screen.fill("white",input_field_rect2)
    screen.fill("green",ok_field)
    mouseclick = (0,0)
    
    # Text box typing
    saveloaded = False

    # INPUT LOOP
    while not saveloaded:
        # calls the player input function to find out which key was pressed
        key = playerInput()

        # makes the play button green
        screen.fill("green",ok_field)

        # checks if the first text box was clicked and make it so that you can type in names and updated accordingly
        if input_field_rect1.collidepoint(mouseclick):
            # Highlights the box that was clicked while dehighlighting the other
            screen.fill("yellow",input_field_rect1)
            screen.fill("white",input_field_rect2)
            # Delete the letters
            if key == "BACKSPACE":
                player1_name = player1_name[:-1]
            # makes it so that while key isnt empty, add the key and then reset it to nothing. This prevents accidental double input
            elif key != "":
                player1_name += key
            key = ""

        # SAME AS ABOVE IF FUNCTION FOR THE SECOND INPUT BOX
        elif input_field_rect2.collidepoint(mouseclick):
            screen.fill("yellow",input_field_rect2)
            screen.fill("white",input_field_rect1)
            if key == "BACKSPACE":
                player2_name = player2_name[:-1]
            elif key != "":
                player2_name += key
            key = ""
        
        # if you click out of the input field, changes ui to inform user
        elif not input_field_rect2.collidepoint(mouseclick) and not input_field_rect1.collidepoint(mouseclick) and not ok_field.collidepoint(mouseclick):
            screen.fill("white",input_field_rect1)
            screen.fill("white",input_field_rect2)

        # Checks if the player presses the play button
        elif ok_field.collidepoint(mouseclick):
            # checks to make sure both fields have a name entered (or at least a character)
            if player1_name != "" and player2_name != "":
                saveloaded = True
                
                #loads the save file
                savefile = open("save.json", "r")
                wins = json.load(savefile)
                savefile.close()
                
                # Ignores capitalization
                player1 = player1_name.upper()
                player2 = player2_name.upper()
                player_game = ''

                # makes sure if 2 players with the same name will not make a error
                # adds a 2 to the 2nd player
                # the second player can be first if they type their name + 2
                if player1 == player2:
                    player2 = player2 + "2"
                    player2_name = player2_name + "2"
                # sorts the game alphabetically to find the key for the matches so we can save scores properly
                # Example: John played against Adam and won 5 - 2. This would be saved as a key named ADAMVJOHN
                # The value would be another dictionary that saves the scores and ties
                if player1 < player2:
                    player_game = player1 + "V" + player2
                else:
                    player_game = player2 + "V" + player1

                # first check if the current players have played against eachother before
                # if not, make a new save
                if player_game not in wins:
                    wins[player_game] = {player1:0, "TIES":0, player2:0}

                # loads all saved scores into game variables to be modified
                if player_game in wins:
                    global player1_wins
                    player1_wins = wins[player_game][player1]
                    global player2_wins
                    player2_wins = wins[player_game][player2]
                    global ties
                    ties = wins[player_game][total_ties]
            else:
                screen.fill("red",ok_field)
            
        # prints the user's name as it is being typed
        p1_text = win_font.render(player1_name, True, (0,0,0))
        screen.blit(p1_text,(input_field_rect1.x+5,input_field_rect1.y+5))
        p2_text = win_font.render(player2_name, True, (0,0,0))
        screen.blit(p2_text,(input_field_rect2.x+5,input_field_rect2.y+5))
        pygame.display.flip()

# END OF MENU FUNCTION

# Creates the game board rectangles in a 3 by 3 squares
board_rects = []
for i in range(0,3):
    for x in range(0,3):
        board_rects += [pygame.Rect((x*200,i*200),rect_size)]

# a rectangle to clean up the text at the bottom of the screen so different texts dont overlay. They get erased instead
blackout_rect = pygame.Rect((0,600),(600,200))

# Function to print current player scores
def wintext(p1name = player1_name, p2name = player2_name):
    global player1_wins
    global player2_wins
    global ties
    # Creates text to show total wins
    p1_win_text = win_font.render(f"{player1_name}'s total wins: {player1_wins}", True, (255,255,255))
    p2_win_text = win_font.render(f"{player2_name}'s total wins: {player2_wins}", True, (255,255,255))
    tie_text = win_font.render(f"Ties: {ties}",True,(255,255,255))
    screen.blit(p1_win_text, (5,710))
    screen.blit(tie_text,(260,710))
    screen.blit(p2_win_text, (360,710))


# game logic to be called per player
# requires the player number(feature to be added to be names instead), shape(X or O), and letter("X" or "O"). The letter is used to update a seperate list board[]
def  game(player_name,player_shape, player_letter):
    # erases the bottom of the screen
    screen.fill("black",blackout_rect)

    #print current score
    wintext()
    
    # Creates text to let know which player's turn it is
    text_surface = game_font.render(f"{player_name}'s Turn '{player_letter}'", True, (255,255,255))
    screen.blit(text_surface, (100,600))

    # checks if a player clicks a square. This loop also makes sure a player cannot update a previously clicked square
    for i in board_rects:
        current_index = board_rects.index(i) # matches the index to the board[] list to be updated
        if i.collidepoint(mouseclick) and board[current_index] != "X" and board[current_index] != "O": # checks where the board is clicked
            board[current_index] = player_letter # updates the internal board
            screen.blit(player_shape,i) # updates the game board on screen
            global turn # accesses the variable turn to update from inside the function
            turn += 1 # next turn
            

    # all possible 3 in rows
    horizontal_win_conditions = (board[0] == board[1] and board[1] == board[2]) or (board[3] == board[4] and board[4] == board [5]) or (board[6] == board[7] and board[7] == board[8])
    vertical_win_conditions = (board[0] == board[3] and board [3] == board[6]) or (board[1] == board[4] and board [4] == board[7]) or (board[2] == board[5] and board [5] == board[8])
    diagonal_win_conditions = (board[0] == board[4] and board[4] == board[8]) or (board[2] == board[4] and board[4] == board[6])

    # checks if any three in rows are met
    if horizontal_win_conditions or vertical_win_conditions or diagonal_win_conditions:
        # lets the player know they have a 3 in row
        # sends true and player string to the win condition variable
        return [True, player_name] 
    else:
        # sends false and empty string to the win condition variable
        return [False, ""]

gamemode = 0
# GAME LOOP
while playing ==  'y':
    # Menu screen
    if gamemode == 0:
        menu()
        gamemode = 1
    # game screen
    if gamemode == 1:
        mouseclick = (-100,-100) # Default so a square isnt preclicked
        turn = 0 # sets the turn to the first one(0 so player 1 is even)
        board = [1,2,3,4,5,6,7,8,9] #this is the internal game board where logic is checked for win conditions. This is also reset every replay

        # Black background, this is called every replay to erase the previous game
        screen.fill("black")
        # creates tic tac toe lines on top of the black background
        screen.blit(tic_tac_toe_lines,(0,0))

        # Lets the first player know its their turn and what letter they are using
        text = game_font.render(f"{player1_name}'s turn 'X'", True, (255,255,255))
        screen.blit(text, (100,600))

        # sets the win condition to false so the game runs until true and empty string because I think it looks cool
        win_condition_met = [False, ""]

        # TIC TAC TOE LOOP
        while win_condition_met[0] != True:
            # Process player inputs
            playerInput()

            # changes player based on which turn it is
            if turn % 2 == 0:
                win_condition_met = game(player1_name, letter_x, "X")
            elif turn % 2 == 1:
                win_condition_met = game(player2_name, letter_o, "O")

            # Checks if win condition is met and lets the players know who won
            if win_condition_met[0] == True:
                screen.fill("black", blackout_rect) # erase the bottom of the game
                # Winner text
                win_text = game_font.render(f"{win_condition_met[1]} wins!", True, (255,255,255),(0,0,0))
                screen.blit(win_text, (150,300))
                if win_condition_met[1] == player1_name:
                    player1_wins += 1
                elif win_condition_met[1] == player2_name:
                    player2_wins += 1

            # If there is no winner by turn 9, declare a tie
            elif turn == 9:
                ties += 1
                text = game_font.render("It's a tie!",True,(255,255,255),(0,0,0))
                screen.fill("black", blackout_rect)
                screen.blit(text, (200,300))
                break # exits the loop

            wintext()
            pygame.display.flip()  # Refresh on-screen display

        # REPLAY LOOP
        decision_made = False
        while decision_made != True:
            
            # Draws the "Play Again" and "Quit" and "Reset" buttons
            screen.fill("black", blackout_rect) # erase the bottom of the game

            # builds all the rectangles
            reset_rect = pygame.Rect((500,675),(100,25))
            yes_rect = pygame.Rect((0,600),(300,100))
            no_rect = pygame.Rect((300,600),(300,100))
            menu_rect = pygame.Rect((250,675),(100,25))

            # draws the rectangles onscreen
            screen.fill("green",yes_rect)
            screen.fill("red", no_rect)
            screen.fill("yellow",reset_rect)
            screen.fill("white",menu_rect)

            # creates and writes the text in the rectangles
            reset_text = win_font.render("RESET",True,(255,0,0))
            yes_text = game_font.render("PLAY AGAIN",True,(0,0,0))
            no_text = game_font.render("QUIT",True,(0,0,0))
            menu_text = win_font.render("MENU",True,(0,0,0))
            screen.blit(menu_text,(275,675)) # menu
            screen.blit(yes_text,(30,610)) #Replay
            screen.blit(no_text,(400,610)) #Quit
            screen.blit(reset_text,(520,675)) #Reset
            wintext()
            
            # checks if player clicks on the screen 
            playerInput()

            # Checks if the player clicked either buttons to replay or quit or to reset the scores
            if reset_rect.collidepoint(mouseclick): # RESET
                player1_wins = 0
                player2_wins = 0
                ties = 0
            elif menu_rect.collidepoint(mouseclick):
                gamemode = 0
                decision_made = True
                
                # loads all current scores back into the dictionary
                wins[player_game][player1] = player1_wins
                wins[player_game][player2] = player2_wins
                wins[player_game][total_ties] = ties
                #saves total wins to file before going back to the menu
                savefile = open("save.json", "w")
                json.dump(wins, savefile)
                savefile.close()
            elif yes_rect.collidepoint(mouseclick): # PLAY AGAIN
                playing = 'y'
                decision_made = True
            elif no_rect.collidepoint(mouseclick): # QUIT
                playing = 'n'
                decison_made = True

                # loads all current scores back into the dictionary
                wins[player_game][player1] = player1_wins
                wins[player_game][player2] = player2_wins
                wins[player_game][total_ties] = ties
                #saves total wins to file before closing the game
                savefile = open("save.json", "w")
                json.dump(wins, savefile)
                savefile.close()
                
                pygame.quit() # quits the game
            pygame.display.flip()  # Refresh on-screen display

# END OF CODE
