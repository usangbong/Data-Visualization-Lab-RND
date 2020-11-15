from gym.envs.registration import register

register(
    id='bpp-v0',
    entry_point='gym_bpp.envs:BppEnv',
)
register(
    id='bpp-extrahard-v0',
    entry_point='gym_bpp.envs:BppExtraHardEnv',
)