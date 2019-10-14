import collections
import numpy as np
import time

def main():
    state = [5, 5, 6]
    n = Nim(state)
    n.play_game(True)

class Nim(object):
    def __init__(self, state):
        self.state = state  # current state of game
        new_state = []  # the state we use to create the array
        for item in state:
            new_state.append(item+1)  # we have to add 1 to everything to account for the possibility zero
        self.N = len(state)
        self.dp = np.zeros(tuple(new_state), dtype=np.bool)  # use the modified state to form an array
        self.dp = ~self.dp

        start = []
        for i in range(self.N):
            start.append(0)  # the start is [0, 0, ..., 0, 0]

        fill_grid(self.N, start, new_state, self.dp)  # find all the states


    def play_game(self, AI_start):  # True means AI is starting, False means you start
        if AI_start:
            move = True  # move tells you whether or not it is the AI's move
        else:
            move = False

        print("WHEN IT IS YOUR TURN, TYPE THE NUMBER OF ITEMS YOU WANT TO BE IN EACH HEAP WITH EACH NUMBER SEPARATED BY ONE SPACE, PRESERVING THE ORDER GIVEN")
        time.sleep(.5)
        print(f"CURRENT STATE: {self.state}")

        while True:
            if move:
                print("AI MOVE")
                self.AI_move()
            else:
                self.player_move()

            check = True  # checks whether or not the game is over
            for item in self.state:
                if item != 0:
                    check = False
                    break
            print(f"CURRENT STATE: {self.state}")


            if check:
                if move:  # depending on whose move it was, we see who won
                    print("YOU WIN!")
                else:
                    print("YOU LOSE!")
                break

            move = not move  # it is now the other persons move, so change move


    def AI_move(self):
        if not winning_move(self.state, self.dp):  # if we are at a losing state
            while True:  # until we find a legitimate move
                rand = np.random.randint(0, self.N)  # choose a pile
                if self.state[rand] != 0:  # if we can make a move from this pile
                    rand2 = np.random.randint(0, self.state[rand])  # choose the move randomly
                    self.state[rand] = rand2  # make the move
                    break
        else:  # else return the winning move
            self.state = winning_move(self.state, self.dp)

    def player_move(self):
        x = input("WHAT IS YOUR MOVE?\n")
        lst = x.split()  # split up the piles
        for i in range(len(lst)):  # convert each pile to an integer
            try:
                lst[i] = int(lst[i])
            except:  # if they have given something that is not a number
                print("ILLEGAL MOVE")
                return self.player_move()
        count = 0  # number of changes the player made (to check legality)
        if len(lst) != self.N:  # if they have given the wrong number of piles
            print("ILLEGAL MOVE")
            return self.player_move()  # make another move
        for i in range(len(lst)):
            if lst[i] > self.state[i]:  # if they have added on a pile
                print("ILLEGAL MOVE")
                return self.player_move()
            elif lst[i] < self.state[i]:
                count += 1
        if count != 1:  # if they made 0 moves or more than 1 move
            print("ILLEGAL MOVE")
            return self.player_move()
        self.state = lst  # if no errors, update state


def fill_grid(N, cur, piles, dp):
    queue = collections.deque()
    visited=set()  # so we don't access the same thing multiple times

    while True:
        if str(cur) not in visited:
            visited.add(str(cur))

            check=False  # whether or not this is a winning state
            to_break = False  # whether or not we have found a winning move yet
            for i in range(N):
                for j in range(cur[i]):  # cur is the index, so we check every accessible state
                    new_cur = cur.copy()
                    new_cur[i]=j  # check this possible move
                    if not dp[tuple(new_cur)]:  # if this is a winning move for us
                        check=True
                        to_break=True
                        break
                if to_break:
                    break

            check_start = True
            for i in range(N): # check if this is the starting state
                if cur[i] != 0:
                    check_start=False
                    break

            if not check and not check_start:  # if this is a winning state and not the start state (since the start is a losing state but will be counted as a winning state
                dp[tuple(cur)] = False

            count = 0  # check the number of locations to add to queue
            for i in range(N):
                new_cur = cur.copy()
                new_cur[i]+=1
                if new_cur[i] != piles[i]:  # if this is a real location
                    count += 1
                    queue.appendleft(new_cur)  # add it to the queue
        if len(queue) == 0:
            return
        cur = queue.pop()  # update cur


def winning_move(state, dp):
    if not dp[tuple(state)]:  # if this is a losing state
        return False
    for i in range(len(state)):  # if it a winning state
        for j in range(state[i]):
            new_state = state.copy()
            new_state[i]=j
            if not dp[tuple(new_state)]:  # find a losing state to change to so the other player will lose
                return new_state

main()
