from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield pages.Instructions
        boxes_collected = random.randint(1, Constants.num_boxes)
        yield (
            pages.Decision,
            {
                'bomb_row': random.randint(1, Constants.num_rows),
                'bomb_col': random.randint(1, Constants.num_cols),
                'boxes_collected': boxes_collected,
                'bomb': random.randint(0, 1)
            }
        )
        expected_round_result = 0 if self.player.bomb else round(boxes_collected * self.subsession.box_value, 2)
        assert self.player.round_payoff == expected_round_result
        yield pages.Results
