#!/usr/bin/env python3

import gymnasium as gym
import blackjack
import random

def agent_function(state):
    action = random.choice(blackjack.BlackjackModel.ACTIONS(state))
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
    
