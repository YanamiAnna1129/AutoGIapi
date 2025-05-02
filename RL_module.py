import torch
from torch import nn
import os
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = "cpu"
current_dir = os.path.dirname(__file__)
filename = os.path.join(current_dir,"dqn.pth")
class DuelingDQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DuelingDQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)

        self.value = nn.Linear(128, 1)
        self.advantage = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        value = self.value(x)
        advantage = self.advantage(x)

        q_value = value + advantage - advantage.mean()
        return q_value
    

class DuelingDDQNAgent:
    def __init__(self, state_dim=16, action_dim=6):
        self.policy_net = DuelingDQN(state_dim, action_dim).to(device)
        self.target_net = DuelingDQN(state_dim, action_dim).to(device)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.target_update_freq = 10
        self.test = False

    def load_policy(self, filename=filename):
        checkpoint = torch.load(filename)
        self.policy_net.load_state_dict(checkpoint['policy_net'])
        self.target_net.load_state_dict(checkpoint['target_net'])

    def get_action(self, state) -> int:

        with torch.no_grad():
            state = torch.tensor(state, dtype=torch.float).to(device)
            q_value = self.policy_net(state)
            action = torch.argmax(q_value).item()
            return action

action_dict = {
    0: 'end',
    1: 'sw_char 0',
    2: 'sw_char 1',
    3: 'sw_char 2',
    4: 'skill 1',
    5: 'skill 2'
}


# dqn_agent = DuelingDDQNAgent(16,6)
# state = [
# 1,2,10,10,10,10,5,10,0,0,0,0,0,0,6,0
# ]
# dqn_agent.load_policy()
# a = dqn_agent.get_action(state=state)
# print(a)