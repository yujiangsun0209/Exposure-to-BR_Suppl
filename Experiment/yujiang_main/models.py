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
Tâche principale - Choix de répartition d'une dotation. <br>
4 traitements: baseline (0), one_sided_dictator (1), one_sided_recipient (2) et common_sym (3)
"""


class Constants(BaseConstants):
    name_in_url = 'ysm'
    players_per_group = 2
    num_rounds = 1

    # in DG_with_AttentionCheck, the dictator is additionally endowed with 20 euros
    endowment = c(20)
    # the magnitude of background risk (BR) is fixed at 10 euros
    magnitude_BR = c(10)
    # those who passed sliders task will get 10 euros in the beginning so that they can have a minimal ability to
    # afford the potential loss from BR
    flat_rate = c(10)

    # numbering the treatments
    baseline = 0
    one_sided_dictator = 1
    one_sided_recipient = 2
    common_sym = 3
    common_indep = 4


class Subsession(BaseSubsession):
    treatment = models.IntegerField()

    def creating_session(self):
        self.treatment = self.session.config['treatment']

    def vars_for_admin_report(self):
        players_infos = list()
        for p in self.get_players():
            players_infos.append(dict(
                joueur=p.id_in_subsession,
                label=p.participant.label,
                group=p.group.id_in_subsession,
                role="Dict." if p.id_in_group == 1 else "Receiv.",
                sent=p.group.give,
                die_1=p.group.die_1,
                die_2=p.group.die_2,
                payoff=p.payoff
            ))
        return dict(players_infos=players_infos)


class Group(BaseGroup):
    give = models.CurrencyField(label=_('I decide to send '), min=c(0), max=Constants.endowment)
    die_1 = models.IntegerField(initial=0)
    die_2 = models.IntegerField(initial=0)

    # if Subsession.treatment == Constants.common_indep:  # BAD IDEA
    # else:
    #     die = models.IntegerField(initial=0)

    def compute_payoffs(self):
        dictator = self.get_player_by_id(1)
        recipient = self.get_player_by_id(2)

        # in treatment 0 (baseline), the payoffs are given by:
        if self.subsession.treatment == Constants.baseline:
            dictator.payoff = Constants.flat_rate + Constants.endowment - self.give
            recipient.payoff = Constants.flat_rate + self.give

        # in treatment 4 (common_indep), the payoffs are given by:
        elif self.subsession.treatment == Constants.common_indep:
            self.die_1 = random.randint(1, 6)
            self.die_2 = random.randint(1, 6)

            if self.die_1 % 2 == 0:
                dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                  + Constants.magnitude_BR
            else:
                dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                  - Constants.magnitude_BR
            if self.die_2 % 2 == 0:
                recipient.payoff = Constants.flat_rate + self.give + Constants.magnitude_BR
            else:
                recipient.payoff = Constants.flat_rate + self.give - Constants.magnitude_BR

        # in other treatments (i.e., 1, 2, 3), the answers are given by:
        else:
            self.die_1 = random.randint(1, 6)
            # in treatment 1 (one_sided_dictator)
            if self.subsession.treatment == Constants.one_sided_dictator:
                if self.die_1 % 2 == 0:
                    dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                      + Constants.magnitude_BR
                else:
                    dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                      - Constants.magnitude_BR
                recipient.payoff = Constants.flat_rate + self.give

            # in treatment 2 (one_sided_recipient)
            elif self.subsession.treatment == Constants.one_sided_recipient:
                dictator.payoff = Constants.flat_rate + Constants.endowment - self.give

                if self.die_1 % 2 == 0:
                    recipient.payoff = Constants.flat_rate + self.give + Constants.magnitude_BR
                else:
                    recipient.payoff = Constants.flat_rate + self.give - Constants.magnitude_BR

            # in treatment 3
            else:
                if self.die_1 % 2 == 0:
                    dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                      + Constants.magnitude_BR
                    recipient.payoff = Constants.flat_rate + self.give + Constants.magnitude_BR
                else:
                    dictator.payoff = Constants.flat_rate + Constants.endowment - self.give \
                                      - Constants.magnitude_BR
                    recipient.payoff = Constants.flat_rate + self.give - Constants.magnitude_BR

        for p in self.get_players():
            p.set_txt_final()


class MyFields:
    @staticmethod
    def get_exercice_choices(question):
        if question == 1:
            the_label = _(
                "Suppose Participant 1 sent €5, and the die results in 1. Including the {} earned in Task 1, "
                "how much did each of them ended up with in Part 1?").format(Constants.flat_rate)
            the_choices = [
                (0, _('Participant 1 earned €25, and Participant 2 earned €5')),
                (1, _('Participant 1 earned €15, and Participant 2 earned €5')),
                (2, _('Participant 1 earned €15, and Participant 2 earned €15'))
            ]
        elif question == 2:
            the_label = _('Suppose Participant 1 sent €10, and the die results in 4. Including the {} earned '
                          'in Task 1, how much did each of them ended up with in Part 1?').format(
                Constants.flat_rate)
            the_choices = [
                (0, _('Participant 1 earned €20, and Participant 2 earned €30')),
                (1, _('Participant 1 earned €30, and Participant 2 earned €30')),
                (2, _('Participant 1 earned €30, and Participant 2 earned €20'))
            ]
        else:
            the_label = _('Suppose Participant 1 sent €15, and the die results in 5. Including the {} earned '
                          'in Task 1, how much did each of them ended up with in Part 1?').format(
                Constants.flat_rate)
            the_choices = [
                (0, _('Participant 1 earned €5, and Participant 2 earned €15')),
                (1, _('Participant 1 earned €15, and Participant 2 earned €15')),
                (2, _('Participant 1 earned €5, and Participant 2 earned €25'))
            ]

        return models.IntegerField(label=the_label, choices=the_choices)


class Player(BasePlayer):
    attempt_1 = MyFields.get_exercice_choices(1)
    attempt_2 = MyFields.get_exercice_choices(2)
    attempt_3 = MyFields.get_exercice_choices(3)
    ans_check = models.IntegerField(initial=0)
    gachter_circles = models.IntegerField()

    def compute_faults(self):
        if self.subsession.treatment == Constants.one_sided_dictator:
            if self.attempt_1 != 2:
                self.ans_check += 1
            if self.attempt_2 != 2:
                self.ans_check += 1
            if self.attempt_3 != 2:
                self.ans_check += 1

        elif self.subsession.treatment == Constants.one_sided_recipient:
            if self.attempt_1 != 0:
                self.ans_check += 1
            if self.attempt_2 != 0:
                self.ans_check += 1
            if self.attempt_3 != 1:
                self.ans_check += 1
        elif self.subsession.treatment == Constants.common_sym:
            if self.attempt_1 != 1:
                self.ans_check += 1
            if self.attempt_2 != 1:
                self.ans_check += 1
            if self.attempt_3 != 0:
                self.ans_check += 1
        elif self.subsession.treatment == Constants.common_indep:
            if self.attempt_1 != 2:
                self.ans_check += 1
            if self.attempt_2 != 2:
                self.ans_check += 1
            if self.attempt_3 != 2:
                self.ans_check += 1

    def set_txt_final(self):
        txt_final = ""
        # for treatment 0 (baseline)
        if self.subsession.treatment == Constants.baseline:
            if self.id_in_group == 1:
                txt_final += _("You decided to send {} to Participant 2, and kept {} to yourself. "
                               "Therefore, your payoff from Part 1 is ({} + {} - {}) {}.").format(
                    self.group.give, Constants.endowment - self.group.give, Constants.flat_rate,
                    Constants.endowment, self.group.give, self.payoff)
                txt_final += " " + _("As to your counterpart (Participant 2), her or his payoff from "
                                     "Part 1 is {}.").format(self.get_others_in_group()[0].payoff)
            else:
                txt_final += _("Since Participant 1 decided to send you {}. Therefore, your payoff from Part 1 "
                               "is ({} + {}) {}.").format(self.group.give, Constants.flat_rate, self.group.give,
                                                          self.payoff)
                txt_final += " " + _("As to your counterpart (Participant 1), her or his payoff from "
                                     "Part 1 is {}.").format(self.get_others_in_group()[0].payoff)

        # for treatment 1 (one_sided_dictator)
        elif self.subsession.treatment == Constants.one_sided_dictator:
            if self.id_in_group == 1:
                txt_final += _("You decided to send {} to Participant 2, and kept {} to yourself. "
                               "Since the die resulted in {},").format(self.group.give,
                                                                       Constants.endowment - self.group.give,
                                                                       self.group.die_1)
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _(
                        "your payoff from Part 1 is reduced by {}. Therefore, your payoff from Part 1 is "
                        "({} + {} - {} - {}) {}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                          Constants.endowment, self.group.give,
                                                          Constants.magnitude_BR, self.payoff)
                else:
                    txt_final += " " + _(
                        "your payoff from Part 1 is increased by {}. Therefore, your payoff from Part 1 is "
                        "({} + {} - {} + {}) {}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                          Constants.endowment, self.group.give,
                                                          Constants.magnitude_BR, self.payoff)
                txt_final += " " + _(
                    "As to your counterpart (Participant 2), her or his payoff from Part 1 is {}.").format(
                    self.get_others_in_group()[0].payoff)
            else:
                txt_final += _("Your payoff from Part 1 is ({} + {}) {}, as your counterpart (Participant 1) sent {} "
                               "to you.").format(Constants.flat_rate, self.group.give, self.payoff, self.group.give)
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("However, the die resulted in {}, so Participant 1's payoff from Part 1 was"
                                         " reduced by {}, that is {}.").format(self.group.die_1, Constants.magnitude_BR,
                                                                               self.get_others_in_group()[0].payoff)
                else:
                    txt_final += " " + _(
                        "Besides, the die resulted in {}, so Participant 1's payoff payoff from Part 1 was"
                        " increased by {}, that is {}.").format(self.group.die_1, Constants.magnitude_BR,
                                                                self.get_others_in_group()[0].payoff)

        # for treatment 2 (one_sided_recipient)
        elif self.subsession.treatment == Constants.one_sided_recipient:
            if self.id_in_group == 1:
                txt_final += _("You decided to send {} to Participant 2, and kept {} to yourself."
                               " Therefore, your payoff from Part 1 is ({} + {} - {}) {}. "
                               "As to your counterpart (Participant 2), since the die resulted in {},").format(
                    self.group.give, Constants.endowment - self.group.give, Constants.flat_rate, Constants.endowment,
                    self.group.give, self.payoff, self.group.die_1)
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("her or his payoff from Part 1 was reduced by {}, that is {}.").format(
                        Constants.magnitude_BR, self.get_others_in_group()[0].payoff)
                else:
                    txt_final += " " + _("her or his payoff from Part 1 was increased by {}, that is {}.").format(
                        Constants.magnitude_BR, self.get_others_in_group()[0].payoff)
            else:
                txt_final += _("Participant 1 sent you {}, and since the die resulted in {},").format(
                    self.group.give, self.group.die_1)
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("Your payoff from Part 1 is ({} + {} - {}) {}.").format(Constants.flat_rate,
                                                                                                 self.group.give,
                                                                                                 Constants.magnitude_BR,
                                                                                                 self.payoff)
                else:
                    txt_final += " " + _("Your payoff from Part 1 is ({} + {} + {}) {}.").format(Constants.flat_rate,
                                                                                                 self.group.give,
                                                                                                 Constants.magnitude_BR,
                                                                                                 self.payoff)
                txt_final += " " + _(
                    "As to your counterpart (Participant 1), her or his payoff from Part 1 is {}.").format(
                    self.get_others_in_group()[0].payoff)

        # for treatment 3 (common_sym)
        elif self.subsession.treatment == Constants.common_sym:
            txt_final += _("Since the die resulted in {},").format(self.group.die_1, )
            if self.id_in_group == 1:
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("your and your counterpart's (Participant 2's) payoff from Part 1 were both "
                                         "reduced by {0}. Besides, you decided to sent {1} to Participant 2. "
                                         "Therefore, your payoff from Part 1 is ({2} + {3} - {4} - {5}) {6}, "
                                         "and your counterpart (Participant 2) ended up with {7}.").format(
                        Constants.magnitude_BR, self.group.give, Constants.flat_rate, Constants.endowment,
                        self.group.give,
                        Constants.magnitude_BR, self.payoff, self.get_others_in_group()[0].payoff)
                else:
                    txt_final += " " + _("your and your counterpart's (Participant 2's) payoff from Part 1 were both "
                                         "increased by {0}. Besides, you decided to sent {1} to Participant 2. "
                                         "Therefore, your payoff from Part 1 is ({2} + {3} - {4} + {5}) {6}, "
                                         "and your counterpart (Participant 2) ended up with {7}.").format(
                        Constants.magnitude_BR, self.group.give, Constants.flat_rate, Constants.endowment,
                        self.group.give,
                        Constants.magnitude_BR, self.payoff, self.get_others_in_group()[0].payoff)
            else:
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("your and your counterpart's (Participant 1's) payoff from Part 1 were both "
                                         "reduced by {0}. Besides, Participant 1 sent you {1}."
                                         " Therefore, your payoff from Part 1 is ({2} + {3} - {4}) {5},"
                                         " and your counterpart (Participant 1) ended up with {6}.").format(
                        Constants.magnitude_BR, self.group.give, Constants.flat_rate, self.group.give,
                        Constants.magnitude_BR, self.payoff, self.get_others_in_group()[0].payoff)
                else:
                    txt_final += " " + _("your and your counterpart's (Participant 1's) payoff from Part 1 were both "
                                         "increased by {0}. Besides, Participant 1 sent you {1}."
                                         " Therefore, your payoff from Part 1 is ({2} + {3} + {4}) {5},"
                                         " and your counterpart (Participant 1) ended up with {6}.").format(
                        Constants.magnitude_BR, self.group.give, Constants.flat_rate, self.group.give,
                        Constants.magnitude_BR, self.payoff, self.get_others_in_group()[0].payoff)

        # for treatment 4 (common_indep)
        elif self.subsession.treatment == Constants.common_indep:
            txt_final += _("Die 1 resulted in {} and Die 2 resulted in {}.").format(self.group.die_1, self.group.die_2)
            if self.id_in_group == 1:
                txt_final += " " + _("Since you sent {} to Participant 2, and according to the rule").format(
                    self.group.give)
                if self.group.die_1 % 2 != 0:
                    txt_final += " " + _("your payoff from Part 1 was reduced by {}, that is"
                                         " ({} + {} - {} - {}) {}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                                            Constants.endowment, self.group.give,
                                                                            Constants.magnitude_BR, self.payoff)
                else:
                    txt_final += " " + _("your payoff from Part 1 was increased by {}, that is"
                                         " ({} + {} - {} + {}) {}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                                            Constants.endowment, self.group.give,
                                                                            Constants.magnitude_BR, self.payoff)
                txt_final += " " + _("And similarly, your counterpart (Participant 2) ended up with {}.").format(
                    self.get_others_in_group()[0].payoff)
            else:
                txt_final += " " + _("Since Participant 1 sent you {}, and according to the rule").format(
                    self.group.give)
                if self.group.die_2 % 2 != 0:
                    txt_final += " " + _("your payoff from Part 1 was reduced by {0}, that is"
                                         " ({1} + {2} - {3}) {4}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                                       self.group.give, Constants.magnitude_BR,
                                                                       self.payoff)
                else:
                    txt_final += " " + _("your payoff from Part 1 was increased by {0}, that is"
                                         " ({1} + {2} + {3}) {4}.").format(Constants.magnitude_BR, Constants.flat_rate,
                                                                       self.group.give, Constants.magnitude_BR,
                                                                       self.payoff)
                txt_final += " " + _("And similarly, your counterpart (Participant 1) ended up with {}.").format(
                    self.get_others_in_group()[0].payoff)

        self.participant.vars["yujiang_main_txt_final"] = txt_final
        self.participant.vars["yujiang_main_payoff"] = self.payoff

        # a ce stage le gain de l'expérience est le gain de la partie 1 (le gain sliders est compris dedans)
        self.participant.payoff = self.payoff
