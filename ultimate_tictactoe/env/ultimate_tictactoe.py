from gymnasium.utils import EzPickle
from gymnasium import spaces
from pettingzoo.utils.agent_selector import agent_selector
from pettingzoo.utils import wrappers
from pettingzoo import AECEnv
from ultimate_tictactoe.env.ultimateboard import UltimateBoard
import functools
import numpy as np

def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

class raw_env(AECEnv, EzPickle):
    metadata = {
        'is_parallelizable': False,
        'name': 'ultimate_tictactoe_v0',
        'render_fps': 1,
        'render_modes': [
            'human'
        ],
    }

    def __init__(self, render_mode=None):
        super().__init__()
        EzPickle.__init__(self)

        self.possible_agents = ['player_1', 'player_2']
        self.agents = self.possible_agents[:]

        assert render_mode is None or render_mode in self.metadata['render_modes']
        self.render_mode = render_mode

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

        self.board = UltimateBoard()

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
    
    def step(self, action):
        if (
            self.terminations[self.agent_selection] or
            self.truncations[self.agent_selection]
        ):
            return self._was_dead_step(action)

        agent = self.agent_selection
        agent_index = self.agents.index(agent)

        board_x = action // 3 % 3
        board_y = action // 27
        tile_x = action % 3
        tile_y = action // 9 % 3
        assert self.board.mark(board_x, board_y, tile_x, tile_y) is True

        if self.board.is_game_over:
            winner = self.board.winner
            if winner is not None:
                winner = agent_index
                loser = winner ^ 1
                self.rewards[self.agents[winner]] += 1
                self.rewards[self.agents[loser]] -= 1

            self.terminations = {agent: True for agent in self.agents}
            self._accumulate_rewards()

        self.agent_selection = self._agent_selector.next()

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

        self.board.reset()

        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.reset()
    
    def observe(self, agent):
        ub = self.board
        cur_symbol, opp_symbol = ('X', 'O') if ub.turn % 2 else ('O', 'X')
        observation = np.array([
            (ub.ultimate_board == cur_symbol),
            (ub.ultimate_board == opp_symbol)
        ], dtype=bool)

        action_mask = np.empty(81, dtype=np.int8)
        if agent == self.agent_selection:
            for board_y in range(3):
                for tile_y in range(3):
                    for board_x in range(3):
                        for tile_x in range(3):
                            board_index = 3 * board_y + board_x
                            cell_index = 27 * board_y + 3 * board_x + 9 * tile_y + tile_x
                            action_mask[cell_index] = ub.turn == 1 or (
                                ub.boards[board_index] == ' ' and
                                ub.ultimate_board[cell_index] == ' ' and (
                                    (board_x, board_y) == (ub.prev_move[2], ub.prev_move[3]) or
                                    ub.boards[3 * ub.prev_move[3] + ub.prev_move[2]] != ' '
                                )
                            )

        return {'observation': observation, 'action_mask': action_mask}

    def render(self):
        if self.render_mode is None:
            gymnasium.logger.warn('You are calling render method without specifying any render mode.')
            return
        return str(self.board)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return spaces.Box(low=0, high=1, shape=(2, 81), dtype=bool)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.Discrete(81)