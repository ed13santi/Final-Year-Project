import gym
import numpy as np

from gym.spaces import Box, Discrete


class DiscretizedObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env, n_bins=10, low=None, high=None):
        super().__init__(env)
        assert isinstance(env.observation_space, Box)

        low = self.observation_space.low if low is None else low
        high = self.observation_space.high if high is None else high

        low = np.array(low)
        high = np.array(high)

        self.n_bins = n_bins
        self.val_bins = [np.linspace(l, h, n_bins + 1) for l, h in
                         zip(low.flatten(), high.flatten())]
        self.ob_shape = self.observation_space.shape

        print("New ob space:", Discrete((n_bins + 1) ** len(low)))
        self.observation_space = Discrete(n_bins ** len(low))

    def _convert_to_one_number(self, digits):
        return sum([d * ((self.n_bins + 1) ** i) for i, d in enumerate(digits)])

    def observation(self, observation):
        #print(observation)
        digits = [np.digitize([x], bins)[0]
                  for x, bins in zip(observation.flatten(), self.val_bins)]
        return self._convert_to_one_number(digits)

class DiscretizedActionWrapper(gym.ActionWrapper):
    def __init__(self, env, n_bins=10, low=None, high=None):
        super().__init__(env)
        assert isinstance(env.action_space, Box)

        low = self.action_space.low if low is None else low
        high = self.action_space.high if high is None else high

        low = np.array(low)
        high = np.array(high)

        self.n_bins = n_bins
        self.val_bins = [np.linspace(l, h, n_bins + 1) for l, h in
                         zip(low.flatten(), high.flatten())]
        self.ob_shape = self.action_space.shape

        print("New action space:", Discrete((n_bins) ** len(low)))
        self.action_space = Discrete(n_bins ** len(low))

    def _convert_to_digits(self, singleNum):
        return [ int(singleNum / (self.n_bins ** i)) % self.n_bins
                for i in range(list(self.env.action_space.shape)[0])]

    def action(self, action):
        #print(action)
        digits = self._convert_to_digits(action)
        return [(bins[x]+bins[x+1])/2
                for x, bins in zip(digits, self.val_bins)]