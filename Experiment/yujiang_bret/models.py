from django.utils.translation import gettext as _
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c
)

author = 'Felix Holzmeister & Armin Pfurtscheller'

doc = """
Bomb Risk Elicitation Task (BRET).  
"""


class Constants(BaseConstants):
    name_in_url = 'ysb'
    players_per_group = None
    num_rounds = 1

    num_rows = 10
    num_cols = 10
    num_boxes = num_rows * num_cols
    box_height = '30px'
    box_width = '30px'

    random_payoff = False
    feedback = True
    results = True
    dynamic = False
    time_interval = 1.00
    random = True
    devils_game = False
    undoable = False


class Subsession(BaseSubsession):
    box_value = models.FloatField()

    def creating_session(self):
        self.box_value = self.session.config.get("yujiang_bret_box_value", 0.1)  # 1 par défault

    def vars_for_admin_report(self):
        players_infos = list()
        for p in self.get_players():
            players_infos.append(
                dict(
                    joueur=p.id_in_subsession,
                    label=p.participant.label,
                    payoff=p.payoff
                )
            )
        return dict(players_infos=players_infos)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # whether bomb is collected or not
    bomb = models.IntegerField()
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()
    boxes_collected = models.IntegerField()

    def set_payoff(self):
        if self.bomb:
            self.payoff = 0
        else:
            self.payoff = round(self.boxes_collected * self.subsession.box_value, 2)

        txt_final = _(
            "You chose to collect {} out of {} boxes. The bomb was hidden behind the box in row {}, column {}.").format(
            self.boxes_collected, Constants.num_boxes, self.bomb_row, self.bomb_col)
        txt_final += " "
        if self.bomb:
            txt_final += " " + _("The bomb was among your {} collected boxes. Accordingly, all your earnings "
                                 "in this task were destroyed and your payoff amounts to {}. ").format(
                self.boxes_collected, self.payoff)
        else:
            txt_final += _("Your collected boxes did not contain the bomb. Thus, you receive {} for each of the {} "
                           "boxes you collected such that your payoff amounts to {}.").format(c(self.subsession.box_value),
                                                                                              self.boxes_collected,
                                                                                              self.payoff)

        self.participant.vars["yujiang_bret_payoff"] = self.payoff
        self.participant.vars["yujiang_bret_txt_final"] = txt_final


    def vars_for_template(self):
        return dict(
            num_rows=Constants.num_rows,
            num_cols=Constants.num_cols,
            num_boxes=Constants.num_boxes,
            num_nobomb=Constants.num_rows * Constants.num_cols - 1,
            box_value=self.subsession.box_value,
            time_interval=Constants.time_interval
        )
