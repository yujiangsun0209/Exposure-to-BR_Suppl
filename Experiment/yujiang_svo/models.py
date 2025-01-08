import random

import numpy as np
from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Currency as c
)
from django.utils.translation import gettext as _

author = 'D. Dubois'

doc = """
Social value orientation (Murphy et al. 2011).
"""


class Constants(BaseConstants):
    name_in_url = 'yssvo'
    players_per_group = 2
    num_rounds = 1

    matrices = {
        1: [(85, 85), (85, 76), (85, 68), (85, 59), (85, 50), (85, 41), (85, 33), (85, 24), (85, 15)],
        2: [(85, 15), (87, 19), (89, 24), (91, 28), (93, 33), (94, 37), (96, 41), (98, 46), (100, 50)],
        3: [(50, 100), (54, 98), (59, 96), (63, 94), (68, 93), (72, 91), (76, 89), (81, 87), (85, 85)],
        4: [(50, 100), (54, 89), (59, 79), (63, 68), (68, 58), (72, 47), (76, 36), (81, 26), (85, 15)],
        5: [(100, 50), (94, 56), (88, 63), (81, 69), (75, 75), (69, 81), (63, 88), (56, 94), (50, 100)],
        6: [(100, 50), (98, 54), (96, 59), (94, 63), (93, 68), (91, 72), (89, 76), (87, 81), (85, 85)]
    }

    conversion_rate = 0.05


class Subsession(BaseSubsession):
    svo_conversion_rate = models.FloatField()

    def creating_session(self):
        self.svo_conversion_rate = self.session.config.get("svo_conversion_rate", Constants.conversion_rate)

    def vars_for_admin_report(self):
        matrices = dict()
        for k, v in Constants.matrices.items():
            matrices[k] = dict(top=[e[0] for e in v], bottom=[e[1] for e in v])

        infos_participants = list()
        for p in self.get_players():
            infos_participants.append(
                dict(
                    code=p.participant.code,
                    label=p.participant.label,
                    group=p.group.id_in_subsession,
                    id_in_group=p.id_in_group,
                    paid_matrice=p.group.svo_paid_choice,
                    choice=getattr(p, f"svo_{p.group.svo_paid_choice}"),
                    svo_payoff=p.svo_payoff,
                    payoff=p.payoff
                )
            )
        return dict(matrices=matrices, infos_participants=infos_participants)


class Group(BaseGroup):
    svo_paid_choice = models.IntegerField()

    def compute_payoffs(self):
        self.svo_paid_choice = random.randint(1, 6)
        for p in self.get_players():
            p.compute_payoff()


class Player(BasePlayer):
    svo_1 = models.IntegerField()
    svo_2 = models.IntegerField()
    svo_3 = models.IntegerField()
    svo_4 = models.IntegerField()
    svo_5 = models.IntegerField()
    svo_6 = models.IntegerField()
    svo_payoff = models.IntegerField()
    svo_mean_self = models.FloatField()
    svo_mean_other = models.FloatField()
    svo_score = models.FloatField()
    svo_classification = models.StringField()

    def compute_payoff(self):
        # calcul gains
        paid_matrice = Constants.matrices[self.group.svo_paid_choice]
        txt_final = _("C'est la répartition {} qui a été tirée au sort. ").format(self.group.svo_paid_choice)
        if self.id_in_group == 1:  # choix qui s'applique aux deux
            choice = getattr(self, f"svo_{self.group.svo_paid_choice}")
            self.svo_payoff, payoff_other = paid_matrice[choice]
            txt_final += _("C'est votre choix qui s'est appliqué dans la paire. "
                           "Vous avez choisi {} pour vous et {} pour l'autre joueur. Votre gain est donc {}€.").format(
                self.svo_payoff, payoff_other, f"{self.svo_payoff * self.subsession.svo_conversion_rate:.2f}"
            )
            self.payoff = c(self.svo_payoff * self.subsession.svo_conversion_rate)
        else:
            choice = getattr(self.get_others_in_group()[0], f"svo_{self.group.svo_paid_choice}")
            payoff_other, self.svo_payoff  = paid_matrice[choice]
            txt_final += _("C'est le choix de l'autre joueur qui s'est appliqué dans la paire. "
                           "Il a choisi {} pour lui et {} pour vous. Votre gain est donc {}€.").format(
                payoff_other, self.svo_payoff, f"{self.svo_payoff * self.subsession.svo_conversion_rate:.2f}"
            )
            self.payoff = c(self.svo_payoff * self.subsession.svo_conversion_rate)

        self.participant.vars["yujiang_svo_txt_final"] = txt_final
        self.participant.vars["yujiang_svo_payoff"] = self.payoff

        # calcul score
        values_self, values_other = [], []
        for i in range(1, len(Constants.matrices) + 1):
            choice = getattr(self, f"svo_{i}")
            values_self.append(Constants.matrices[i][choice][0])
            values_other.append(Constants.matrices[i][choice][1])
        self.svo_mean_self = np.round(np.mean(values_self), 3)
        self.svo_mean_other = np.round(np.mean(values_other), 3)
        self.svo_score = np.round(np.degrees(np.arctan((self.svo_mean_other - 50) / (self.svo_mean_self - 50))), 3)
        if self.svo_score <= -12.04:
            self.svo_classification = "competitive"
        elif -12.04 < self.svo_score <= 22.45:
            self.svo_classification = "individualist"
        elif 22.45 < self.svo_score <= 57.15:
            self.svo_classification = "prosocial"
        else:
            self.svo_classification = "altruist"

    def vars_for_template(self):
        matrices = dict()
        for k, v in Constants.matrices.items():
            matrices[k] = dict(top=[e[0] for e in v], bottom=[e[1] for e in v])
        return dict(matrices=matrices)

