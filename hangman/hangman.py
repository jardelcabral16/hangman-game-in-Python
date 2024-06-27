import os
import random
import time
import csv
import drawed_hangman


MAXIMUM_NUMBER_OF_WRONG_GUESSES = 5
MAXIMUM_NUMBER_OF_HINTS = 3
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


wrong_guess_counter = 0
hints_asked_counter = 0
hidden_secret_word = "_" * len(SECRET_WORD)


def main() :
    print_introduction()
    play_game_logic()
    clear_terminal()


def clear_terminal(delay=2) :
    time.sleep(delay)  
    return os.system("cls")  


def play_game_logic() : 
    loss_condition = False
    win_condition = False

    while (not loss_condition) and (not win_condition) :
        draw_hangman_and_hidden_word()
        print_remaining_number_of_guesses_and_hints()

        user_guess = input("Enter a letter: ").strip(" ")
        scenario = check_guess(user_guess)
        
        act_based_on_scenario(user_guess, scenario)  
        
        loss_condition = (wrong_guess_counter >= MAXIMUM_NUMBER_OF_WRONG_GUESSES)
        win_condition = (hidden_secret_word.lower() == SECRET_WORD.lower())
           
        clear_terminal(1)

    if loss_condition :
        print()
        print(drawed_hangman.five_errors_hangman)
        print("\nYou lost!\n\nThe word was '" + SECRET_WORD + "'")
        
    else :
        print("The word was '" + SECRET_WORD + "'. Good job. You win!")


def check_guess(user_guess) :
    global wrong_guess_counter
    if user_guess.lower() == "hint" :
        return "hint"
    elif user_guess.lower() == "guess" :
        return "guess"
    elif user_guess[:1].lower() not in SECRET_WORD.lower() :
        if wrong_guess_counter < MAXIMUM_NUMBER_OF_WRONG_GUESSES - 2:
            print("\nThere's no '" + user_guess + "' in the word. You still have",  MAXIMUM_NUMBER_OF_WRONG_GUESSES - (wrong_guess_counter + 1), "guesses.\n")
            return "wrong guess"
        elif wrong_guess_counter == MAXIMUM_NUMBER_OF_WRONG_GUESSES - 2 :
            print("\nThere's no '" + user_guess + "' in the word. You have one more guess.\n")
            return "wrong guess"
        else :
            wrong_guess_counter = MAXIMUM_NUMBER_OF_WRONG_GUESSES
            print("\nYou used up all your guesses.")
            return "wrong guess"

    elif user_guess[:1].lower() in hidden_secret_word.lower() :
        print("Try entering another letter. The letter '" + user_guess + "' is already in the word.\n")
        return "already made guess"
    else :
        print("There's a letter '" + user_guess + "' in the word. Good job!\n")
        return "correct guess"        


def act_based_on_scenario(user_guess, scenario) :
    global wrong_guess_counter, hints_asked_counter
    
    match scenario :
        case "wrong guess" :
            wrong_guess_counter = wrong_guess_counter + 1
        case "already made guess" :
            pass
        case "correct guess" :
            uncover_hidden_word(user_guess)
        case "hint" :
            hints_asked_counter = hints_asked_counter + 1
            print_hint()
        case "guess" :
            get_and_check_whole_word_guess()


def uncover_hidden_word(user_guess) :
    global hidden_secret_word
    
    after_guess_hidden_word = ""

    for i in range(len(SECRET_WORD)) :
        if SECRET_WORD[i].lower() == user_guess[:1].lower() :
            after_guess_hidden_word = after_guess_hidden_word + SECRET_WORD[i]
        elif hidden_secret_word[i] != HIDDEN_SYMBOL :
            after_guess_hidden_word = after_guess_hidden_word + hidden_secret_word[i] 
        else :
            after_guess_hidden_word = after_guess_hidden_word + HIDDEN_SYMBOL
    
    hidden_secret_word = after_guess_hidden_word
            

def get_and_check_whole_word_guess() :
    global hidden_secret_word, wrong_guess_counter

    user_guess = input("Enter the word you think it is the answer: ").strip(" ")
        
    if user_guess.lower() == SECRET_WORD.lower() :
        hidden_secret_word = SECRET_WORD 
    else :
        wrong_guess_counter = MAXIMUM_NUMBER_OF_WRONG_GUESSES
        

def print_introduction() :
    clear_terminal(0.25)
    print("\n--- Hangman: contries edition ---")
    print("\nEach time you guess it right, you can continue to play.")
    print("\nYou can ask for hints up to", MAXIMUM_NUMBER_OF_HINTS, "times by typing 'hint'.")
    print("\nYou can try your luck and guess the whole word at any point by typing 'guess'.")
    print("Be aware that if you do that and guess it wrong, you lose the game!") 
    print("Otherwise will only be guessing letters")
    print("\nYou can only guess it wrong at most", MAXIMUM_NUMBER_OF_WRONG_GUESSES, "times.")
    print("\nBegin!", end="\n\n")


def draw_hangman_and_hidden_word() :
    match wrong_guess_counter :
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
    print(hidden_secret_word, end="\n\n")


def print_remaining_number_of_guesses_and_hints() :
    print("Remaining number of guesses:", MAXIMUM_NUMBER_OF_WRONG_GUESSES - wrong_guess_counter)
    print("Remaining number of hints:", MAXIMUM_NUMBER_OF_HINTS - hints_asked_counter)
    print()


def print_hint() :
    global hints_asked_counter

    match hints_asked_counter :
        case 1 :
            print(HINTS[hints_asked_counter - 1])
        case 2 :
            print(HINTS[hints_asked_counter - 1])
        case 3 :
            print(HINTS[hints_asked_counter - 1])
        case _ :
            print("All hints used. You cannot ask for more")
            hints_asked_counter = MAXIMUM_NUMBER_OF_HINTS

    time.sleep(2)


if __name__ == "__main__" :
    main()
