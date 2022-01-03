from collections import Counter
import random
import string
from os import system, name
from rich import print

WORD_LENGTH = 5
MAX_GUESSES = 6
ALPHABET = string.ascii_uppercase
GREEN = "#52e837"
YELLOW = "#f7ff11"
GRAY = "#bec1bd"

INSTRUCTIONS = f"""[b]Welcome to Wordle in Python[/b]
Attempt to guess the five letter word in six tries.
After each guess the word will be highlighted based on how close your guess was to the word.
If a letter is [{GREEN}]green[/{GREEN}], it is in the correct position.
If a letter is [{YELLOW}]yellow[/{YELLOW}], it is in the word but in the wrong sport.
If a letter is is not highlighted, it is not in the word at all."""

with open("count_1w.txt", 'r', encoding='utf-8') as file:
    word_bank = [word.strip().upper() for word in file if len(word.strip()) == 5]
    word_bank = word_bank[:3000]
    random.shuffle(word_bank)


print(INSTRUCTIONS)
input("Press Enter when you are ready to begin.")

def main():

    while True:  # Main game loop.
        bad_letters = set()
        good_letters = set()
        perfect_letters = set()
        guesses = []
 
        secret_word = generate_secret_word()
        num_guesses = 1
        while num_guesses <= MAX_GUESSES:
            # Create loop for user input and make sure it is valid.
            clear()
            print_letter_bank(bad_letters, good_letters, perfect_letters)
            print_guesses(guesses)

            print(f"Guess #{num_guesses}: ")
            guess = get_guess(bad_letters)

            # Get the clues based on the user input
            bad_letters, good_letters, perfect_letters, clues = get_clues(
                guess, secret_word, bad_letters, good_letters, perfect_letters
            )
            guesses.append(clues)
            num_guesses += 1
            if guess == secret_word:
                print(f"You got it! The solution was {secret_word}.")
                break
            if num_guesses > MAX_GUESSES:
                print("You ran out of guesses.")
                print(f"The answer was {secret_word}.")

        # Ask player if they want to play again.
        print("Do you want to play again? (yes or no)")
        if not input("> ").lower().startswith("y"):
            break
    print("Thanks for playing!")


def clear():
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def generate_secret_word():
    """Returns a word from the word bank."""
    return word_bank.pop()


def get_guess(bad_letters):
    while True:
        valid_guess = True
        guess = input("> ").upper()
        if len(guess) != WORD_LENGTH or not guess.isalpha():
            print("Enter a valid guess.")
            continue
        for letter in guess:
            if letter in bad_letters:
                print("You entered letters that are known to be bad. Try again.")
                valid_guess = False
                break
        if valid_guess:
            break
    return guess.upper()


def get_clues(guess, secret_word, bad_letters, good_letters, perfect_letters):
    """Returns a string formatted with YELLOW, GREEN or black."""
    if guess == secret_word:
        return bad_letters, good_letters, perfect_letters, "You got it!"

    secret_counts = Counter(secret_word)
    guess_counts = Counter()
    clues = []

    for i, letter in enumerate(guess):
        guess_counts.update(letter)

        if guess[i] == secret_word[i]:
            clues.append(f"[{ GREEN }]{letter}[/{ GREEN }]")
            perfect_letters.add(letter)
            
        elif guess[i] in secret_word and guess_counts[letter] <= secret_counts[letter]:
            clues.append(f"[{ YELLOW }]{letter}[/{ YELLOW }]")
            good_letters.add(letter)
        else:
            clues.append(letter)
            bad_letters.add(letter)
    good_letters = good_letters - perfect_letters
    bad_letters = bad_letters - perfect_letters
    return bad_letters, good_letters, perfect_letters, "".join(clues)


def print_letter_bank(bad_letters, good_letters, perfect_letters):
    """Prints out the alphabet color coded according to usage in the game."""
    letter_bank = []
    for letter in ALPHABET:
        if letter in bad_letters:
            letter_bank.append(f"[{GRAY}]{letter}[/{ GRAY }]")
        elif letter in good_letters:
            letter_bank.append(f"[{ YELLOW }]{letter}[/{ YELLOW }]")
        elif letter in perfect_letters:
            letter_bank.append(f"[{ GREEN }]{letter}[/{ GREEN }]")
        else:
            letter_bank.append(letter)
    print("LETTER BANK")
    print("-----------")
    for i, letter in enumerate(letter_bank):
        if i != 0 and (i + 1) % 5 == 0:
            print(letter)
        else:
            print(letter, end=" ")
    print("\n\n")


def print_guesses(guesses):
    """TODO: Prints the guesses made."""
    for guess in guesses:
        print(guess)
    print()


# If the program is run (instead of imported), run the game:
if __name__ == "__main__":
    main()
