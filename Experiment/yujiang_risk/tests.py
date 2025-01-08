import random

from . import pages
from ._builtin import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield pages.RISKGeneral, dict(RISK_general=random.randint(0, 10))
        yield pages.RISKDetaille, dict(
            RISK_conduite=random.randint(0, 10),
            RISK_finance=random.randint(0, 10),
            RISK_sport=random.randint(0, 10),
            RISK_travail=random.randint(0, 10),
            RISK_sante=random.randint(0, 10),
            RISK_autres=random.randint(0, 10)
        )
