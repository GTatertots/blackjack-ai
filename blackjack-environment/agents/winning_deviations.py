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
        
        #SPECIALIZED CASES
        running_total = counter(cards)
        if running_total > 2:
            dealer_total = 0
            player_total = 0
            for i, card in enumerate(cards):
                value = (i % 13) + 1
                if value in [11,12,13]:
                    value = 10
                elif value == 1:
                    value = 11
                if card == 1:
                    dealer_total = value
                elif card == 2:
                    player_total += value
            if player_total >= 16 and dealer_total == 10:
                action = 0
            elif player_total >= 13 and dealer_total == 2:
                action = 0
            elif player_total >= 12 and dealer_total <= 3:
                action = 0
            elif obs[57] == 1 and player_total == 10 and dealer_total == 11:
                action = 2
            elif obs[57] == 1 and player_total == 9 and dealer_total == 7:
                action = 2


    #-- Failsafe if no action is picked
    if action == None:
        action = random.choice(actions)
    #--

    return action

def main():
    # render_mode = None
    render_mode = "ansi"

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

    print(f"\nFinal score: {state.observation[53] - 500}")
    env.close()
    return

if __name__ == "__main__":
    main()
    
