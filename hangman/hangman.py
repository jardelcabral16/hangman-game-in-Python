import os
import random
import time
import csv
import drawed_hangman


MAXIMUM_NUMBER_OF_WRONG_GUESSES = 5
HIDDEN_SYMBOL = "_"

def get_secret_word() :
    lines = []

    with open("wordlist.csv", "r") as file :
        reader = csv.DictReader(file)

        for row in reader :
            lines.append(row)
        
        return random.choice(lines)

CHOSEN_WORD_AND_HINTS = get_secret_word()
SECRET_WORD = CHOSEN_WORD_AND_HINTS['country']
HINTS = [CHOSEN_WORD_AND_HINTS['hint 1'], 
        CHOSEN_WORD_AND_HINTS['hint 2'], 
        CHOSEN_WORD_AND_HINTS['hint 3']]

WRONG_GUESS_COUNTER = 0
HINTS_ASKED_COUNTER = 0
HIDDEN_SECRET_WORD = HIDDEN_SYMBOL * len(SECRET_WORD)


def main() :
    print_introduction()
    play_game_logic()
    clear_terminal()


def clear_terminal(delay=2) :
    time.sleep(delay)  
    return os.system("cls")  


def play_game_logic() :
    scenario = "" 
    
    while WRONG_GUESS_COUNTER < MAXIMUM_NUMBER_OF_WRONG_GUESSES and HIDDEN_SECRET_WORD.lower() != SECRET_WORD.lower() :
        draw_hangman_and_hidden_word()

        print_remaining_guesses_and_hints()

        user_guess = input("Enter a letter: ").strip(" ")
        
        scenario = check_guess(user_guess)
        
        act_based_on_scenario(scenario, user_guess)
           
        clear_terminal(1)

    if WRONG_GUESS_COUNTER == MAXIMUM_NUMBER_OF_WRONG_GUESSES :
        print()
        print(drawed_hangman.five_errors_hangman)
        print("\nYou lost!\n\nThe word was '" + SECRET_WORD + "'")
        
    else :
        print("The word was '" + SECRET_WORD + "'. Good job. You win!")


def check_guess(user_guess) :
    if user_guess.lower() == "hint" :
        return "hint"
    elif user_guess.lower() == "guess" :
        return "guess"
    elif user_guess[:1].lower() not in SECRET_WORD.lower() :
        if WRONG_GUESS_COUNTER < MAXIMUM_NUMBER_OF_WRONG_GUESSES - 2:
            print("\nThere's no '" + user_guess + "' in the word. You still have",  MAXIMUM_NUMBER_OF_WRONG_GUESSES - (WRONG_GUESS_COUNTER + 1), "guesses.\n")
            return "wrong guess"
        elif WRONG_GUESS_COUNTER == MAXIMUM_NUMBER_OF_WRONG_GUESSES - 2 :
            print("\nThere's no '" + user_guess + "' in the word. You have one more guess.\n")
            return "wrong guess"
        else :
            print("\nYou used up all your guesses.")
            return "wrong guess"

    elif user_guess[:1].lower() in HIDDEN_SECRET_WORD.lower() :
        print("Try entering another letter. You already know that the letter '" + user_guess + "' is in the word.\n")
        return "already made guess"
    else :
        print("There's a letter '" + user_guess + "' in the word. Good job!\n")
        return "correct guess"        


def act_based_on_scenario(scenario, user_guess) :
    global WRONG_GUESS_COUNTER, HINTS_ASKED_COUNTER
    
    match scenario :
        case "wrong guess" :
            WRONG_GUESS_COUNTER = WRONG_GUESS_COUNTER + 1
        case "already made guess" :
            WRONG_GUESS_COUNTER
        case "correct guess" :
            uncover_hidden_word(user_guess)
        case "hint" :
            HINTS_ASKED_COUNTER = HINTS_ASKED_COUNTER + 1
            print_hint()
        case "guess" :
            get_and_check_whole_word_guess()


def uncover_hidden_word(user_guess) :
    global SECRET_WORD, HIDDEN_SECRET_WORD
    after_guess_hidden_word = ""

    for i in range(len(SECRET_WORD)) :
        if SECRET_WORD[i].lower() == user_guess[:1].lower() :
            after_guess_hidden_word = after_guess_hidden_word + SECRET_WORD[i]
        elif HIDDEN_SECRET_WORD[i] != HIDDEN_SYMBOL :
            after_guess_hidden_word = after_guess_hidden_word + HIDDEN_SECRET_WORD[i] 
        else :
            after_guess_hidden_word = after_guess_hidden_word + HIDDEN_SYMBOL
    
    HIDDEN_SECRET_WORD = after_guess_hidden_word
            

def get_and_check_whole_word_guess() :
    global HIDDEN_SECRET_WORD, WRONG_GUESS_COUNTER

    user_guess = input("Enter the word you think it is: ").strip(" ")
        
    if user_guess.lower() == SECRET_WORD.lower() :
        HIDDEN_SECRET_WORD = SECRET_WORD 
    else :
        WRONG_GUESS_COUNTER = MAXIMUM_NUMBER_OF_WRONG_GUESSES
        

def print_introduction() :
    clear_terminal(0.1)
    print("--- Hangman: contries edition ---")
    print("\nEach time you guess it right, you can continue to play.")
    print("\nYou can ask for hints up to three times by typing 'hint'.")
    print("\nYou can try your luck and guess the whole word at any point by typing 'guess'.")
    print("Be aware that if you do that and guess it wrong, you lose the game!") 
    print("Otherwise will only be guessing letters")
    print("\nYou can only guess it wrong at most", MAXIMUM_NUMBER_OF_WRONG_GUESSES, "times. \n\nBegin!", end="\n\n")


def draw_hangman_and_hidden_word() :
    match WRONG_GUESS_COUNTER :
        case 0 :
            print(drawed_hangman.no_errors_hangman)
        case 1 :
            print(drawed_hangman.one_error_hangman)
        case 2 :
            print(drawed_hangman.two_errors_hangman)
        case 3 :
            print(drawed_hangman.three_errors_hangman)
        case 4 :
            print(drawed_hangman.four_errors_hangman)
        case 5 :
            print(drawed_hangman.five_errors_hangman)
    
    print()
    print(HIDDEN_SECRET_WORD, end="\n\n")


def print_remaining_guesses_and_hints() :
    print("Remaining number of guesses:", MAXIMUM_NUMBER_OF_WRONG_GUESSES - WRONG_GUESS_COUNTER)
    print("Remaining number of hints:", 3 - HINTS_ASKED_COUNTER)
    print()


def print_hint() :
    global HINTS_ASKED_COUNTER

    match HINTS_ASKED_COUNTER :
        case 1 :
            print(HINTS[HINTS_ASKED_COUNTER - 1])
        case 2 :
            print(HINTS[HINTS_ASKED_COUNTER - 1])
        case 3 :
            print(HINTS[HINTS_ASKED_COUNTER - 1])
        case _ :
            print("All hints used. You cannot ask for more")
            HINTS_ASKED_COUNTER = 3

    time.sleep(2)


if __name__ == "__main__" :
    main()
