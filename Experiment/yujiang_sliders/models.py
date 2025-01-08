import random

from django.utils.translation import gettext as _
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
)

author = 'D. Dubois'

doc = """
Tâche d'effort.
"""


class Constants(BaseConstants):
    name_in_url = 'yss'
    players_per_group = None
    num_rounds = 2

    flat_rate = c(10)
    show_up_fee = c(2)
    requirement = 15
    time_given = 420  # seconds


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            for r in range(Constants.num_rounds):
                p.participant.vars[f'slider_goals_{r + 1}'] = [random.randint(0, 100) for _ in range(10)]

    def vars_for_admin_report(self):
        players_infos = list()
        for p in self.get_players():
            players_infos.append(dict(
                joueur=p.id_in_subsession,
                label=p.participant.label,
                score=p.total_sliders_correct,
                total_score=sum([pr.total_sliders_correct for pr in p.in_all_rounds()]),
                continue_expe=_("Yes") if sum(
                    [pr.total_sliders_correct for pr in p.in_all_rounds()]) >= Constants.requirement else _("No"),
                payoff=p.payoff
            ))
        return dict(players_infos=players_infos)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    slider1 = models.IntegerField(min=0, max=100, initial=0)
    slider2 = models.IntegerField(min=0, max=100, initial=0)
    slider3 = models.IntegerField(min=0, max=100, initial=0)
    slider4 = models.IntegerField(min=0, max=100, initial=0)
    slider5 = models.IntegerField(min=0, max=100, initial=0)
    slider6 = models.IntegerField(min=0, max=100, initial=0)
    slider7 = models.IntegerField(min=0, max=100, initial=0)
    slider8 = models.IntegerField(min=0, max=100, initial=0)
    slider9 = models.IntegerField(min=0, max=100, initial=0)
    slider10 = models.IntegerField(min=0, max=100, initial=0)

    total_sliders_correct = models.IntegerField(initial=0)

    def check_slider_answers(self):
        for i in range(10):
            if getattr(self, f"slider{i + 1}") == self.participant.vars[f'slider_goals_{self.round_number}'][i]:
                self.total_sliders_correct += 1

        total = sum([p.total_sliders_correct for p in self.in_all_rounds()])
        if total >= Constants.requirement:
            self.payoff = Constants.flat_rate
        else:
            self.payoff = Constants.show_up_fee

        self.participant.vars["yujiang_sliders_payoff"] = self.payoff
        self.participant.vars["yujiand_sliders_txt_final"] = _(
            "You correctly positioned {} sliders overall, your payoff is therefore equal to {}.").format(
            total, self.payoff
        )
