import random

from otree.api import Submission

from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        dict_choices = {k: random.randint(0, 8) for k in [f"svo_{i}" for i in range(1, len(Constants.matrices) + 1)]}
        yield Submission(pages.Decision, dict_choices, check_html=False)
        yield (pages.Result)

