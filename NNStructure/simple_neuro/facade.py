from typing import Tuple

import numpy as np
import torch
from torch import nn

from Learning.game import Game
from NNStructure.base_facade import BaseFacade
from NNStructure.simple_neuro.struct import SimpleNeuroStruct
from utils.player_role import PlayerRole


class SimpleNeuroFacade(BaseFacade):
    loss_function: nn.BCELoss
    optimizer: torch.optim.Adam

    def __init__(self, lr: float):
        super().__init__()
        self.net = SimpleNeuroStruct()
        for el in self.net.layers[0].parameters():
            print("azazazaza")
            print(el)
        print("******")
        self.loss_function = nn.BCELoss()
        self.lr = lr

    def make_move(self, field: np.ndarray) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.zeros((1, 225), dtype='f')
        for i, val in enumerate(np.nditer(field)):
            res[0, i] = val
        return torch.tensor(res)

    def learn(self, game_history: Game, your_role: PlayerRole):
        for field, inp_ans in game_history.get_steps():
            fc = field.clone()
            for i, j in range(15):
                if fc[i][j] == 0:
                    fc[i][j] = 1

            self.one_learning_step(field, inp_ans)

    def one_learning_step(self, field: np.ndarray, isgood: bool):
        field = self.prepare_field(field)

        output = self.net(field)
        p2 = torch.tensor([[float(isgood)]])
        print(output)
        loss = self.loss_function(output, p2)

        loss.backward()

        return loss, output
