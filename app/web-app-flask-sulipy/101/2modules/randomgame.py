from random import randint
import sys

def run_guess(guess, answer):
    if 0 < guess < 11:
        if guess == answer:
            print('you are a genius!')
            # break : ezt kommentelni kellett mert a while alól kikerültünk, használjunk tehát return-t
            return True
    else:
        print('hey bozo, i said 1~10')

if __name__ == '__main__':
    # answer = randint(1,10)
    answer = randint(int(sys.argv[1]),  int(sys.argv[2]))
    # input from user
    # check that input is a number
    while  True:
        try:
            guess = int(input('guess a number 1-10: '))
            if (run_guess(guess, answer)):
                break
        except ValueError:
            print('please enter a number! ')
            continue

