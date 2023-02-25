import argparse
import random
from cowsay import cowsay, list_cows
from typing import Tuple
from urllib.request import urlopen


def bullscows(guess: str, secret: str) -> Tuple[int, int]:

    bulls = 0
    set_guess = set()
    set_secret = set()

    for a, b in zip(guess, secret):

        if a == b:
            bulls += 1
        
        set_guess.add(a)
        set_secret.add(b)
    
    cows = len(set_guess.intersection(set_secret))

    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        word = input(
            cowsay(
                message=prompt,
                cow=random.choice(list_cows()),
        ) + '\n'
        )
        if valid is None or word in valid:
            return word


def inform(format_string: str, bulls: int, cows: int):
    print(
        cowsay(
            message=format_string.format(bulls, cows),
            cow=random.choice(list_cows()),
        )
    )


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    n_try = 0
    while True:
        guess = ask('Введите слово: ', words)
        n_try += 1

        if secret == guess:
            return n_try

        bulls, cows = bullscows(guess=guess, secret=secret)
        inform('Быки: {}, Коровы: {}', bulls, cows)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dict', type=str)
    parser.add_argument('len', type=int, default=5, nargs='?')
    args = parser.parse_args()

    try:
        words = urlopen(args.dict).read().decode().split()
    except:
        try:
            words = open(args.dict, 'r').read().split()
        except:
            print(f'Wrong dictionary {args.dict}')
    
    words = [w for w in words if len(w) == args.len]

    print(f'Количество попыток: {gameplay(ask=ask, inform=inform, words=words)}')
