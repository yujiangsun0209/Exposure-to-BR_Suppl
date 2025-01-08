from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)
from django.utils.translation import gettext as _


author = 'D. Dubois'

doc = """
Sensibilité au risque, déclarée. Dohmen et al. (2011).
"""


class Constants(BaseConstants):
    name_in_url = 'ysri'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    risque_general = models.IntegerField(
        choices=[(0, "0 - Pas du tout prêt(e) à prendre des risques"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Tout à fait prêt(e) à prendre des risque")]
    )
    risque_sante = models.IntegerField(
        choices=[(0, "0 - Pas du tout prêt(e) à prendre des risques"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Tout à fait prêt(e) à prendre des risque")]
    )
    risque_argent = models.IntegerField(
        choices=[(0, "0 - Pas du tout prêt(e) à prendre des risques"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Tout à fait prêt(e) à prendre des risque")]
    )
    patience = models.IntegerField(
        choices=[(0, "0 - Très impatient(e)"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Très patient(e)")]
    )
    confiance_autres = models.IntegerField(
        choices=[(0, "On n'est jamais assez trop prudent"),
                 (1, "On peut faire confiance à la plupart des gens")]
    )
    confiance_autres_general = models.IntegerField(
        choices=[(0, "0 - Très prudent(e) dans mes relations avec les autres"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Très confiant(e) dans mes relations avec les autres")]
    )
    confiance_autres_famille = models.IntegerField(
        choices=[(0, "0 - Très prudent(e) dans mes relations avec les autres"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Très confiant(e) dans mes relations avec les autres")]
    )
    confiance_autres_travail = models.IntegerField(
        choices=[(0, "0 - Très prudent(e) dans mes relations avec les autres"),
                 (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Très confiant(e) dans mes relations avec les autres")]
    )