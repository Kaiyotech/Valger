from rocket_learn.agent.actor_critic_agent import ActorCriticAgent
from rocket_learn.agent.discrete_policy import DiscretePolicy
from torch.nn import Linear
from torch import nn
import torch as th
from typing import Tuple


class ActorCriticEmbedderAgent(ActorCriticAgent):
    def __init__(self, actor, critic, embedder: Linear, optimizer):

        super().__init__(actor=actor, critic=critic, optimizer=optimizer)
        self.embedder = embedder

    def forward(self, *args, **kwargs):
        embedded = self.embedder(args[-1])
        obs = args[:-1]
        obs.extend(th.max(embedded, -2))
        return self.actor(obs, **kwargs), self.critic(obs, **kwargs)


class DiscreteEmbed(DiscretePolicy):
    def __init__(self, net: nn.Module,  embedder: Linear, shape: Tuple[int, ...] = (3,) * 5 + (2,) * 3, deterministic=False):
        super ().__init__(net=net, shape=shape, deterministic=deterministic)
        self.embedder = embedder

    def forward(self, obs):
        embedded = self.embedder(obs[1])
        new_obs = obs[0]
        new_obs.extend(th.max(embedded, -2))
        logits = self.net(new_obs)
        return logits