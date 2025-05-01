import random
import time
import sys

"""

Author: Harjap Uppal
Student ID: 501316128

Problem Description: 
This program is based on Hangman. Players have to guess what the hidden word is
by guessing one letter at a time. Every correct letter will reveal that part of
the word and every inccorect guess will progess the drawing of the stick
figure. If the drawing is complete, the player loses the game. If the player
fills in the word before that happens, then they win. The program contains
difficulties levels that can be choosen by the user, allowing the player more
flexibility of the game. Program also contains a hint system, which allows the
players to get a letter for free if they are stuck. The program also tracks the
statistics of the player throughout all of their games played, which saves data
such as total games played, games won, games lost, etc into a text file within
the folder.

"""

dangle_states = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

def game_loop(difficulty, word, state_skip):
    
    """
    Where the main game operates. Players will make their guesses here. 
    Once the game ends and they win or lose, their statistics will
    be saved to the file "savedata.txt". This function can only be entered 
    after selecting the difficulty. This function can only be exited once 
    the game ends and their statistics save.
    """

    answer = ["_"] * (len(word))
    wrong_letters = []
    guessed_letters = []    
    current_state = 0
    hints_used = 0
    win = False # this only changes if the player wins

    # Loop until the player wins or reaches the final danglestate
    while current_state <= len(dangle_states)-2:
        # set guess equal to a value that is not valid, to force the program
        # into the while loop
        guess = "NOT AN ANSWER123"
        
        # check to make sure the player only guessed one letter and is
        # alphabetical. Also to avoid repeating the same guess
        while (len(guess) != 1) or (guess in guessed_letters) or not (guess.isalpha()):
            print(f"-------------------------------------------------------\n{dangle_states[current_state]}\n\nWord: {answer}\nLetters Guessed: {guessed_letters}\nWrong Letters:{wrong_letters}\nHints Used: {hints_used}\n\n")
            
            guess = input("Enter a letter to guess (Type \"hint\" for a hint):\n")
            
            # if a hint is requested, then choose a random letter in the answer,
            # and make that letter the player's guess, which will give them part of
            # the answer
            if guess == "hint":
                guess = random.choice(word)
                
                # if that letter has already been revealed to the player, then
                # choose a different one
                while guess in guessed_letters:   
                    guess = random.choice(word)
                    
                print("\n\nHint Used\n\n")
                hints_used += 1
                time.sleep(0.5)
                
            # display the appropriate message based on the situation and
            # prompt for another guess
            if guess in guessed_letters:
                print("\nYou already guessed that\n\n")
            elif len(guess) != 1:
                print("\nYou must guess only one letter\n\n")
            elif not guess.isalpha():
                print("\nYou can only guess letters\n\n")
                
            time.sleep(0.5)
            

        # Call guess_check method and check if the guess is correct and update 
        # the current answer
        answer, check = guess_check(word, guess, answer)

        # If there are no more blanks, then the player wins. If they made a
        # wrong guess, then enter the next danglestate
        if check:
            if "_" not in answer:
                win = True
                break
        else:
            current_state += state_skip
            wrong_letters.append(guess)
        

        guessed_letters.append(guess)

    # once outside the while loop, display the appropriate message based on
    # the result of the game
    if win:
        print(f"\n\n-------------------------------------------\nYOU WIN\n-------------------------------------------\n\nThe word was: {word}")
    else:
        print(f"-------------------------------------------------------\n{dangle_states[-1]}")
        print(f"\n\n-------------------------------------------\nYOU LOSE\n-------------------------------------------\n\nThe word was: {word}")
        
    # Attempt to read existing statistics from "savedata.txt" and update it 
    # with the current game's results.
    try: 
       total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used = read_file()
          
       # Update relevant statistics based on the game's result
       if win:
           games_won += 1
           current_win_streak += 1

           if current_win_streak > longest_win_streak:
               longest_win_streak = current_win_streak
                
           if len(word) > longest_word_guessed:
               longest_word_guessed = len(word)
               
       else:
            games_lost += 1
            current_win_streak = 0

        # Update non-dependant statistics
       total_games_played += 1
       win_percentage = round(((games_won/total_games_played) * 100), 2)
       total_hints_used += hints_used

       print(f"\nStatistics:\nTotal Games Played: {total_games_played}\nGames Won: {games_won}\nGames Lost: {games_lost}\nWin Percentage: {win_percentage}%\nCurrent Win Streak: {current_win_streak}\nLongest Win Streak: {longest_win_streak}\nLongest Word Guessed: {longest_word_guessed}\nTotal Hints Used: {total_hints_used}")
        
       # call the save_file function to save the updated data into a file
       save_file(total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used)
        
        
    # if file is not found or is emoty, then add the statistics of current game
    # as the first entry in the file
    except (FileNotFoundError, ValueError):
        total_games_played = 1

        if win:
            games_won = 1
            games_lost = 0
            current_win_streak = 1
            longest_win_streak = 1
            longest_word_guessed = len(word)
        else:
            games_won = 0
            games_lost = 1
            current_win_streak = 0
            longest_win_streak = 0
            
        win_percentage = (games_won/total_games_played) * 100
        total_hints_used = hints_used      
        
        print(f"\nStatistics:\nTotal Games Played: {total_games_played}\nGames Won: {games_won}\nGames Lost: {games_lost}\nWin Percentage: {win_percentage}%\nCurrent Win Streak: {current_win_streak}\nLongest Win Streak: {longest_win_streak}\nLongest Word Guessed: {longest_word_guessed}\nTotal Hints Used: {total_hints_used}")
        
        # call the save_file function to save the updated data into a file
        save_file(total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used)
            

def guess_check(word, guess, answer):
    
    """
    Logic to determine if the player guessed the correct letter. Check returns
    True if letter is correct, otherwise it returns false. This also updates
    the blanks in the answer
    """
    check = False
    
    if guess in word:
        for index, letter in enumerate(word, start=0):
            # if letter loctation is found, replace the blank with the actual
            # letter
            if guess == letter:
                answer[index] = letter
                check = True

    return answer, check

def setup(difficulty):
    
    """
    Set up the game by selecting a word and determining state progression based on difficulty
    (harder difficulty uses longer words and faster failure progression).
    """

    # based on difficulty, determine the range of the length of the word, and
    # determine of fast the game should progess
    if difficulty == 1:
        letter_min = 3
        letter_max = 11
        state_skip = 1
    elif difficulty == 2:
        letter_min = 12
        letter_max = 22
        state_skip = 2


    word = ""

    # attempts to opens "wordbank.txt" containing random words that are listed 
    # line by line.
    try:
        with open("wordbank.txt", "r") as words_file:
            file = words_file.readlines()
            
        # randomly select the word, if the word doesn't meet length
        # requirements, then choose a new word. continue until condition is
        # satisfied
        while not (letter_min <= len(word) <= letter_max):
            word = random.choice(file).strip() 
            
    # If wordbank.txt is not found or is empty, then force the game to close 
    # as it cannot be played in the current state
    except (FileNotFoundError, ValueError, IndexError):
        print("\nProgram is corrupted! \"wordbank.txt\" is missing or empty\n\n" +
              "Game Closing...")
        sys.exit(0) 

    return word, state_skip

def save_file(total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used):
    
    """
    Saves the data passed in into the savedata.txt file
    """

    with open("savedata.txt","w") as savedata_file:
        savedata_file.write(f"{total_games_played}\n{games_won}\n{games_lost}\n{win_percentage}\n{current_win_streak}\n{longest_win_streak}\n{longest_word_guessed}\n{total_hints_used}\n")
        
        print("\nSaved to \"savedata.txt\"")


def read_file():
    
    """
    Returns the data read from the savedata.txt file
    """
        
    with open("savedata.txt","r") as savedata_file:
        total_games_played = int(savedata_file.readline().strip())
        games_won = int(savedata_file.readline().strip())
        games_lost = int(savedata_file.readline().strip())
        win_percentage = float(savedata_file.readline().strip())
        current_win_streak = int(savedata_file.readline().strip())
        longest_win_streak = int(savedata_file.readline().strip())
        longest_word_guessed = int(savedata_file.readline().strip())
        total_hints_used = int(savedata_file.readline().strip())
        
    return total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used







# Start of the main program
print("\nWelcome to DangleMan!")

# infinite loop which can only be exited by leaving the program
while True:
    print("------------------------------\n- Play (1)\n- View Highscore" + 
          " (2)\n- Help (3)\n- Any other number to exit the program\n" + 
          "\nType the number associated with the option\n")
    
    # attempt to prompt the user for a number
    try:
        
        intro = int(input("What would you like to do?:\n"))
    
    # if the user does not type a number, raise an error to the user and 
    # restart the loop
    except ValueError:
        print("\nYou must enter a number\n")
        time.sleep(0.5)
        continue
        
    # if the user chooses to play, then prompt for difficulties
    if intro == 1:
            
        # infinite loop to force the user to type a valid input
        while True:
            print("\nDifficulties:\n------------------\n- Rope Rookie (1)\n-" + 
                  " DangleMan Apprentice (2)\n\nType the number associated with" + 
                  " the option\n")
            
            # attempt to prompt for a difficulty
            try:
                difficulty = int(input("\nSelect your difficulty:\n"))
                if 1 <= difficulty <= 2:
                    break  # Exit the loop if the input is valid
                
                print("\nPlease type either 1 or 2.\n")
            # if user doesn't input an integer, warn user
            except ValueError:
                print("\nPlease type either 1 or 2.\n")


    
        # Call the setup function to get the decided word and game progression
        # also calls game_loop function to start the game. Reprompt for action
        # after
        word, state_skip = setup(difficulty)
        game_loop(difficulty, word, state_skip)
        
        intro = 0
        continue
    
    elif intro == 2:
        
        # attempt to call the read_file function to get existing player data 
        # and display to the user
        try:
            total_games_played, games_won, games_lost, win_percentage, current_win_streak, longest_win_streak, longest_word_guessed, total_hints_used = read_file()    
            
            print(f"\nStatistics:\nTotal Games Played: {total_games_played}\nGames Won: {games_won}\nGames Lost: {games_lost}\nWin Percentage: {win_percentage}%\nCurrent Win Streak: {current_win_streak}\nLongest Win Streak: {longest_win_streak}\nLongest Word Guessed: {longest_word_guessed}\nTotal Hints Used: {total_hints_used}")
        
        # If the file was not found, then tell user and reprompt for action
        except (FileNotFoundError, ValueError):
            print("\nNo save data was found\n")
            time.sleep(0.5)
            
        intro = 0
        continue
    
    # if the player chooses the help option, display the rules of the game
    elif intro == 3:
        print("\n\nHow to play\n----------------\n- Your goal is to guess" + 
              " what the hidden word is\n- You have to guess one letter at" + 
              " a time until you guessed the complete word\n- If you guess" + 
              " the letter correctly, the blanks in the word will start" + 
              " to fill with that letter\n- If you guess the letter" + 
              " incorrectly, then the dangleman becomes more complete\n-" +
              " If the dangleman is completed, then you lose the game\n-" +
              " If you choose to play on the harder difficulty, you will" +
              " have less forgiveness for your mistakes\n- At the end" +
              " of the game you can see your statistics and will be" +
              " saved in the \"savedata.txt\" file\n")
        
        intro = 0
        continue
    
    # if the user enters any other number, display goodbye message and exit
    # the program
    else:
        print("\nThanks for playing!")
        break
