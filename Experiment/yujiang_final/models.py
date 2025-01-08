import random

from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)

author = 'D. DUBOIS'

doc = """
Ecran final
"""


class Constants(BaseConstants):
    name_in_url = 'ysfin'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        players_infos = list()

        for p in self.get_players():
            players_infos.append(dict(
                joueur=p.id_in_subsession,
                label=p.participant.label,
                part1_payoff=p.participant.vars.get("yujiang_main_payoff", 0),
                part2_selected_task=p.part2_selected_task,
                part2_payoff=p.participant.vars.get("yujiang_bret_payoff", 0) if p.part2_selected_task == 1 else
                    p.participant.vars.get("yujiang_svo_payoff", 0) if p.part2_selected_task == 2 else 0,
                payoff=p.payoff
            ))
        return dict(players_infos=players_infos)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    part2_selected_task = models.IntegerField()
    comments = models.LongStringField(blank=True)

    def start(self):
        self.part2_selected_task = random.randint(1, 2)

        self.payoff = self.participant.vars.get("yujiang_main_payoff", 0)

        if self.part2_selected_task == 1:
            self.payoff += self.participant.vars.get("yujiang_bret_payoff", 0)
        else:
            self.payoff += self.participant.vars.get("yujiang_svo_payoff", 0)

        self.participant.payoff = self.payoff
