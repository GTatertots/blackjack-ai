#!/usr/bin/env python3

import gymnasium as gym
import blackjack
import random

def counter(cards):
    total = 0
    for i, card in enumerate(cards):
        if card != 0:
            value = (i % 13) + 1
            if value in [11,12,13]:
                value = 10
            elif value == 1:
                value = 11
            if value <= 6:
                total += 1
            elif value >= 10:
                total -= 1
    return total

def agent_function(state):
    action = None
    obs = state.observation
    actions = blackjack.BlackjackModel.ACTIONS(state)
    cards = obs[:52]
    #BETTING PHASE
    if obs[55] == 1:
        running_total = counter(cards)
        if running_total < 0:
            action = 3
        elif running_total < 3:
            action = 4
        elif running_total >= 3:
            action = 5
    #PLAYING PHASE
    if obs[56] == 1:
        undealt = 0
        score = 0 
        for i, card in enumerate(cards):
            value = (i % 13) + 1
            if value in [11,12,13]:
                value = 10
            elif value == 1:
                value = 11
            if card == 0:
                undealt += 1
            elif card == 2:
                score += value
        needed = 21 - score
        decent = 0
        great = 0
        perfect = 0
        for i, card in enumerate(cards):
            value = (i % 13) + 1
            if value in [11,12,13]:
                value = 10
            elif value == 1:
                value = 11
            if card == 0 and value <= needed:
                decent += 1
                if (needed - value) >= 0 and (needed - value) <= 3:
                    great += 1
                if value == needed:
                    perfect += 1
        print(undealt, decent, decent/undealt)
        if (decent/undealt) < 0.2:
            action = 0
        elif (great/undealt) > 0.5 and obs[57] == 1:
            action = 2
        else:
            action = 1
            
        count = counter(cards)
        dealer = 0
        player = 0
        for i, card in enumerate(cards):
            value = (i % 13) + 1
            if value in [11,12,13]:
                value = 10
            elif value == 1:
                value = 11
            if card == 1:
                dealer = value
            elif card == 2:
                player += value 
        if player == 16 and dealer == 10:
            if count < 0: action = 1
            else: action = 0
        if player == 15 and dealer == 10:
            if count < 4: action = 1
            else: action = 0
        if obs[57] == 1 and player == 10 and dealer == 10:
            if count < 4: action = 1
            else: action = 2
        if player == 12 and dealer == 3:
            if count < 2: action = 1
            else: action = 0
        if player == 12 and dealer == 4:
            if count < 3: action = 1
            else: action = 0
        if player == 11 and dealer == 11:
            if count < 1: action = 1
            else: action = 2
        if player == 9 and dealer == 2:
            if count < 1: action = 1
            else: action = 2
        if player == 10 and dealer == 11:
            if count < 4: action = 1
            else: action = 2
        if player == 9 and dealer == 7:
            if count < 3: action = 1
            else: action = 2
        if player == 16 and dealer == 9:
            if count < 5: action = 1
            else: action = 0
        if player == 13 and dealer == 2:
            if count < -1: action = 1
            else: action = 0
        if player == 12 and dealer == 4:
            if count < 0: action = 1
            else: action = 0
        if player == 12 and dealer == 5:
            if count < -2: action = 1
            else: action = 0
        if player == 12 and dealer == 6:
            if count < -1: action = 1
            else: action = 0
        if player == 13 and dealer == 3:
            if count < -2: action = 1
            else: action = 0

    #-- Failsafe if no action is picked
    if action == None:
        action = random.choice(actions)
    #--

    return action

def main():
    RUNS = 10000
    running_total = 0
    for i in range(RUNS):
        render_mode = None
        #render_mode = "ansi"

        env = gym.make('blackjack/Blackjack-v0', render_mode=render_mode)
        observation, info = env.reset()
        state = blackjack.BlackjackState()
        state.observation = observation
    
        terminated = truncated = False
        if render_mode == "ansi":
            print("Current state:", env.render())
        while not (terminated or truncated):
            action = agent_function(state)
            if render_mode == "ansi":
                print()
                words = ""
                if action == 0:
                    words = "Stand"
                elif action == 1:
                    words = "Hit"
                elif action == 2:
                    words = "Double Down"
                elif action == 3:
                    words = "Bet 10"
                elif action == 4:
                    words = "Bet 25"
                elif action == 5:
                    words = "Bet 50"
                print(f"Action: {words}")
            observation, reward, terminated, truncated, info = env.step(action)
            state.observation = observation
            if render_mode == "ansi":
                print("Current state:\n", env.render())
        score = state.observation[53] - 500
        print(f"\nScore after 10 rounds: {score}")
        running_total += score
        env.close()
    print(f"After {RUNS}, Score: {running_total}")
    return

if __name__ == "__main__":
    main()
    
