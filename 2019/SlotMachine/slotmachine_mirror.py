#!/usr/bin/python3

import requests
import random
import collections
import json

#from secret import flag
flag='CSA{abcdefghijklmnopqrstuvwxyz1234567}'
s = requests.Session()
url = 'http://csa.bet/'
spin_url = 'http://csa.bet/spin/?coins='
r = s.get(url, allow_redirects=False)
REAL_FLAG = [c for c in flag]
found = [False for c in flag]

PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
flag_length = len(flag)
SLOT_LENGTH = 10
NO_COINS = "No more coins! Goodbye."
NOT_ENOUGH_COINS = "You don't have enough coins!"
INVALID_COIN_NUMBER = "Coin number can't be negative"
INITIAL_COINS = 10

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Slotmachine(object):
    def __init__(self):
        self.slots = [[i]+[random.choice(PRINTABLE) for i in range(SLOT_LENGTH)] for i in flag]
        self.attempt_num = 0
        self.total_coins = INITIAL_COINS
        self.last_result = ""
        self.last_gamble = 0
        self._j = None
        self._first = True

    def get_prize(self):
        #result = self.last_result
        #prize = sum([x for x in collections.Counter(result).values() if x > 2])
        #prize *= self.last_gamble
        #self.total_coins += prize
        prize = self._j['prize']
        return prize

    def check_invalid_input(self, coins):
        if self.total_coins <= 0:
            self.last_result = ""
            return NO_COINS
        if self.total_coins < coins:
            self.last_result = ""
            return NOT_ENOUGH_COINS
        if coins < 0:
            self.last_result = ""
            return INVALID_COIN_NUMBER
        return None

    def spin(self, coins):
        invalid_message = self.check_invalid_input(coins)
        if invalid_message:
            return invalid_message.center(flag_length, ' ')

        r = s.get(spin_url + str(coins))
        self._j = json.loads(r.content)

        self.last_gamble = coins
        #self.total_coins -= coins
        self.total_coins = self._j['current_coins']

        random.seed(coins + self.attempt_num)
        self.attempt_num += 1

        for i in self.slots:
            random.shuffle(i)

        result = ""
        for i in self.slots:
            result += random.choice(i)
        self.last_result = result
        result1 = ''
        if self._first:
            result1 = result
            self._first = False
        else:
            for i in range(len(result)):
                if result[i] == flag[i]:
                    result1 += bcolors.OKGREEN + result[i] + bcolors.ENDC
                    if not found[i]:
                        REAL_FLAG[i] = self._j['result'][i]
                        found[i] = True
                else:
                    result1 += result[i]
        return result1

# This is used to run the slotmachine locally, the server doesn't use this.
def main():
    slotmachine = Slotmachine()
    print("You have {} coins".format(slotmachine.total_coins))
    get_next_num = True
    while get_next_num:
        try:
            prize = 0 
            #coins =  int(input("Enter number of coins:\n"))
            coins = 1
            result = slotmachine.spin(coins)
            if result == NO_COINS:
                get_next_num = False
            elif result != NOT_ENOUGH_COINS:
                prize = slotmachine.get_prize()
            print(result)
            print(''.join(REAL_FLAG))
            if all(found):
                get_next_num = False
            print("You won {} coins!".format(prize))
            print("{} coins left.".format(slotmachine.total_coins))

        except ValueError:
            get_next_num = False
        except NameError:
            get_next_num = False

#CSA{D0n't_G4mbl3_W1th_youR_pRnG_SeeD5}
if __name__ == '__main__':
    main()
