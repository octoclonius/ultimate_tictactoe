from ultimate_tictactoe import ultimate_tictactoe_v0 as utt_v0

if __name__ == '__main__':
    env = utt_v0.env(render_mode='human')
    env.reset(seed=42)
    for agent in env.agent_iter():
        print(env.render())
        observation, reward, termination, truncation, info = env.last()
        if termination or truncation:
            action = None
        else:
            if 'action_mask' in info:
                mask = info['action_mask']
            elif isinstance(observation, dict) and 'action_mask' in observation:
                mask = observation['action_mask']
            else:
                mask = None
            action = env.action_space(agent).sample(mask)
        env.step(action)
    env.close()