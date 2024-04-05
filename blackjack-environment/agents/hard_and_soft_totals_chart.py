#!/usr/bin/env python3

import gymnasium as gym
import blackjack
import random

hard_chart=[[1, 2, 2, 2, 2, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]

soft_chart=[[1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
            [1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
            [1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1],
            [3, 3, 3, 3, 3, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def agent_function(state):
    action = None
    obs = state.observation
    actions = blackjack.BlackjackModel.ACTIONS(state)
    cards = obs[:52]
    if obs[56] == 1:
        dealer = 0
        player = 0
        soft_hand = False
        for i, card in enumerate(cards):
            value = (i % 13) + 1
            if value in [11,12,13]:
                value = 10
            elif value == 1:
                value = 11
            if card == 1:
                dealer = value
            elif card == 2:
                if value == 11:
                    soft_hand = True
                player += value
        if player == 21:
            return 0
        if player > 21 and soft_hand == True:
            player -= 10
            soft_hand = False
        if player <= 8:
            action = 1
        elif soft_hand:
            action = soft_chart[player - 13][dealer - 2]
            if action == 2 and obs[57] != 1:
                action = 1
            if action == 3:
                if obs[57] == 1:
                    action = 2
                else: 
                    action = 0
        elif player >= 17:
            action = 0
        else:
            action = hard_chart[player - 9][dealer - 2]
            if action == 2 and obs[57] != 1:
                action = 1

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
    
