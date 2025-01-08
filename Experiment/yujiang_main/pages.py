import random

from django.utils.translation import gettext as _

from ._builtin import Page, WaitPage
from .models import Constants


class WaitForPairing(WaitPage):
    group_by_arrival_time = True
    body_text = "Nous attendons les autres participants"


class StartTask2(Page):
    def vars_for_template(self):
        return dict(
            treatment=self.subsession.treatment
        )

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Instruction(Page):
    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class AttentionCheck(Page):
    form_model = 'player'
    form_fields = ['attempt_1', 'attempt_2', 'attempt_3']

    def is_displayed(self):
        return self.subsession.treatment != Constants.baseline

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))

    def before_next_page(self):
        self.player.compute_faults()


class ResultsOfAttentionCheck(Page):
    def is_displayed(self):
        return self.subsession.treatment != Constants.baseline

    def vars_for_template(self):
        the_dict = dict()
        if self.subsession.treatment == Constants.one_sided_dictator:
            the_dict["ans_1"] = _('Participant 1 earned €15, and Participant 2 earned €15')
            the_dict["ans_2"] = _('Participant 1 earned €30, and Participant 2 earned €20')
            the_dict["ans_3"] = _('Participant 1 earned €5, and Participant 2 earned €25')
        elif self.subsession.treatment == Constants.one_sided_recipient:
            the_dict['ans_1'] = _('Participant 1 earned €25, and Participant 2 earned €5')
            the_dict['ans_2'] = _('Participant 1 earned €20, and Participant 2 earned €30')
            the_dict['ans_3'] = _('Participant 1 earned €15, and Participant 2 earned €15')
        elif self.subsession.treatment == Constants.common_sym:
            the_dict['ans_1'] = _('Participant 1 earned €15, and Participant 2 earned €5')
            the_dict['ans_2'] = _('Participant 1 earned €30, and Participant 2 earned €30')
            the_dict['ans_3'] = _('Participant 1 earned €5, and Participant 2 earned €15')
        elif self.subsession.treatment == Constants.common_indep:
            the_dict['ans_1'] = _('Participant 1 earned €35, and Participant 2 earned €25')
            the_dict['ans_2'] = _('Participant 1 earned €30, and Participant 2 earned €10')
            the_dict['ans_3'] = _('Participant 1 earned €5, and Participant 2 earned €15')
        the_dict["treatment"] = self.subsession.treatment
        return the_dict

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class RoleAssignment(Page):
    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Distribution(Page):
    form_model = 'group'
    form_fields = ['give']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "compute_payoffs"
    wait_for_all_groups = False


class BePatient(Page):
    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class GachterCircles(Page):
    form_model = "player"
    form_fields = ["gachter_circles"]

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))

    def before_next_page(self):
        if self.timeout_happened:
            self.player.gachter_circles = random.randint(1, 7)


page_sequence = [
    WaitForPairing,
    StartTask2,
    Instruction,
    AttentionCheck,
    ResultsOfAttentionCheck,
    RoleAssignment,
    Distribution,
    ResultsWaitPage,
    GachterCircles,
    BePatient
]
