from gymnasium.envs.registration import register

from blackjack.envs.blackjack_env import BlackjackEnv
from blackjack.envs.blackjack_model import BlackjackModel
from blackjack.envs.blackjack_model import BlackjackState

register(
    id="blackjack/Blackjack-v0",
    entry_point="blackjack.envs:BlackjackEnv",
    max_episode_steps=50,
)
