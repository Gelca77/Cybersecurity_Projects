#!/usr/bin/env python 3

#cheating hangman


import random
import string

# global variables
all_words = set()
words = set()
guessed_letters = set()
max_word_length = 0
min_word_length = 0
show_details = False

def start_game():
    """Starts the hangman game

    Args:
        None

    Returns:
       None
    """     
    # initialize global all words set , max word length, min word length
    initialize()
    global guessed_letters
    global show_details
    global words

    length = input('What word length? ')
    int_length = int(length)
    
    if abs(int_length) >= min_word_length and abs(int_length) <= max_word_length:
        # if input length is negative, enable show details flag
        if int_length < 0:
            show_details = True
    
        # get words set based on length
        for word in all_words:
            if len(word) == abs(int_length):
                words.add(word)

        if show_details:
            print('Potential words:', words)

        print('There are ' + str(len(words)) + ' possible words')

        # initialize number of guesses
        guesses = 5
        print('You have ' + str(guesses) + ' guesses remaining')
        print('Current hint:', mask_word(list(words)[0], guessed_letters))         

        is_win = False

        # loop while there are available guesses
        while guesses != 0:
            valid_guess = False
            guess = None

            # loop while guess is not valid
            while valid_guess == False:
                guess = input('Enter a letters: ')
                if guess in guessed_letters:
                    print('That letter has already been guessed.')
                elif guess not in string.ascii_letters or guess == '':
                    print('That is not a letter.')
                else:
                    valid_guess = True

            # add new guess input to guessed letters
            guessed_letters.add(guess)

            # get partitions based on the current words set and guessed letters
            partitions = partition(words, guessed_letters)

            # select max partition
            selected_partition = max_partition(partitions)

            if show_details:
                print('Partitions:')
                for partite in partitions.items():
                    print(partite[0],':',partite[1])
                print('Selected partition:', selected_partition)

            if guess in selected_partition:
                print("Yes! " + guess + " is in the word!")

                # check if there are still hyphens, if none, then its a win
                if '-' not in selected_partition:
                    is_win = True
                    break

            else:
                # subtract guesses 
                guesses = guesses - 1
                print("I'm sorry " + guess + " is not in the word.")

            if show_details:
                print('Potential words:', words)

            print('There are ' + str(len(words)) + ' possible words')
            print('You have ' + str(guesses) + ' guesses remaining')
            print('Guessed letters:', guessed_letters)
            print('Current hint:', selected_partition)         

        if is_win:
            print('You win! The word was ' + list(words)[0])

        else:
            print('You have lost. The word was ' + list(words)[0])

    else:
        print('No words of length ' + length + ' found')


def initialize():
    """Initializes global all words set, max word length, min word length

    Args:
        None

    Returns:
       None
    """ 

    # global variables
    global all_words
    global max_word_length
    global min_word_length
    global words
    words = set()

    word_lengths = []
    # open text file and load words to all words set
    with open("./word_list.txt") as file:
        for word in file: 
            word = word.strip()
            all_words.add(word)
            word_lengths.append(len(word))
    
    # get max and minimum word lengths
    max_word_length = max(word_lengths)
    min_word_length = min(word_lengths)


def mask_word(word, guessed):
    """Returns word with all letters not in guessed replaced with hyphens

    Args:
        word (str): the word to mask
        guessed (set): the guessed letters

    Returns:
        str: the masked word
    """ 
    masked_list = []
    # loop through all letters of the word
    for letter in word:
        # if letter in in guessed, replace with hyphen
        if letter not in guessed:
            letter = '-'
        masked_list.append(letter)
    masked_word = ''.join(masked_list)
    return masked_word
            

def partition(words, guessed):
    """Generates the partitions of the set words based upon guessed

    Args:
        words (set): the word set
        guessed (set): the guessed letters

    Returns:
        dict: The partitions
    """
    # initialize partitions dictionary
    dict = {}
    # loop through words
    for word in words:
        masked = mask_word(word, guessed)
        if masked in dict:
            dict[masked].add(word)
        else:
            dict[masked] = {word}
    return dict

def max_partition(partitions):
    """Returns the hint for the largest partite set

    The maximum partite set is selected by selecting the partite set with
    1. The maximum size partite set
    2. If more than one maximum, prefer the hint with fewer revealed letters
    3. If there is still a tie, select randomly

    Args:
        partitions (dict): partitions from partition function

    Returns:
        str: hint for the largest partite set
    """
    global words
    global guessed_letters

    # initialize the hint of the max partite set
    hint = None

    # get sizes of partite sets
    partite_count_list = []
    for partition in partitions.values():
        partite_count_list.append(len(partition))

    max_size = max(partite_count_list)

    # get partite sets with max size
    max_partite_hint_list = []
    for partite_set in partitions:
        if len(partitions[partite_set]) == max_size:
            max_partite_hint_list.append(partite_set)

    # if only 1 partite set with max size
    if len(max_partite_hint_list) == 1:
        hint = max_partite_hint_list[0]

    # 2 or more partite sets with max size, get the fewer revealed letters in the hint
    else:

        # get the number of revealed letters in the max hint list
        revealed_letters_count = []
        for hint in max_partite_hint_list:
            revealed_letters_count.append(count_letters(hint))

        # get the minimum number of revealed letters
        min_revealed_count = min(revealed_letters_count)
        
        # get hint with minimum number of revealed letters
        min_revealed_hint_list = []
        for hint in max_partite_hint_list:
            if count_letters(hint) == min_revealed_count:
                min_revealed_hint_list.append(hint)  

        # if there is only 1 hint in the list
        if len(min_revealed_hint_list) == 1:
            hint = min_revealed_hint_list[0]

        else:
            # get a hint at random
            hint = random.choice(max_partite_hint_list)

    words = partitions[hint]
    return hint
    
    

def count_letters(masked_word):
    """Returns the number of letters in a masked_word excluding hyphens

    Args:
        masked_word: word made up of letters and hyphens

    Returns:
        cnt: number of letters
    """
    cnt = 0
    for letter in masked_word:
        if letter.isalpha():
            cnt = cnt + 1
    return cnt


def test_mask_word():
    if mask_word('abcdefg', {'a', 'c', 'e', 'g'}) != 'a-c-e-g':
        print("Error with mask_word('abcdefg', {'a', 'c', 'e', 'g'})")
    if mask_word('abcdefg', {'h', 'i', 'j'}) != '-------':
        print("Error with mask_word('abcdefg', {'h', 'i', 'j'})")        
    if mask_word('aaabbbcccddd', {'b','d'}) != '---bbb---ddd':
        print("Error with mask_word('aaabbbcccddd', {'b','d'})")     
  

def test_count_letters():
    if count_letters('------') != 0:
        print("Error with count_letters('------')")    
    if count_letters('---a') != 1:
        print("Error wiht count_letters('---a')")
    if count_letters('---ab--') != 2:
        print("Error with count_letters('---ab--')")
    if count_letters('-aabbcc---') != 6:
        print("Error with count_letters('-aabbcc---')")

def test_partition():
    if partition({'test', 'abcd'}, {'a'}) != {'----': {'test'}, 'a---': {'abcd'}}:
        print("Error with partition({'test', 'abcd'}, {'a'})")
    if partition({'test', 'abcd', 'cdef'}, {'a'}) != {'----': {'test', 'cdef'}, 'a---': {'abcd'}}:
        print("Error with partition({'test', 'abcd', 'cdef'}, {'a'})")
    if partition({'test', 'abcd', 'cdef'}, {'a', 'e'}) != {'--e-': {'cdef'}, '-e--': {'test'}, 'a---': {'abcd'}}:
        print("Error with partition({'test', 'abcd', 'cdef'}, {'a', 'e'})")

def test_max_partition():
    if max_partition({'----': {'test', 'efgh'}, 'a---': {'abcd'}}) != '----':
        print ("Error with max_partition({'----': {'test', 'efgh'}, 'a---': {'abcd'}})")
    if max_partition({'----': {'test', 'efgh'}, 'a---': {'abcd', 'acde'}}) != '----':
        print ("Error with max_partition({'----': {'test', 'efgh'}, 'a---': {'abcd', 'acde'}})")
    if max_partition({'----': {'test'}, 'a---': {'abcd'}}) != '----':
        print("Error with max_partition({'----': {'test'}, 'a---': {'abcd'}})")
    if max_partition({'-es-': {'test'}, 'a---': {'abcd'}}) != 'a---':
        print("Error with max_partition({'-es-': {'test'}, 'a---': {'abcd'}})")

if __name__ == '__main__':
    test_mask_word()
    test_count_letters()
    test_partition()
    test_max_partition()
    start_game()
