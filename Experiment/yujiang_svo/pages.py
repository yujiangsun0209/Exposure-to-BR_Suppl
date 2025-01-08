from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import gettext as _


class WaitForPairing(WaitPage):
    group_by_arrival_time = True
    body_text = "Nous attendons les autres participants"


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Decision(Page):
    form_model = "player"
    form_fields = [f"svo_{i}" for i in range(1, len(Constants.matrices) + 1)]

    def vars_for_template(self):
        return self.player.vars_for_template()

    def js_vars(self):
        d_vars = self.vars_for_template()
        d_vars.update(
            dict(
                fill_auto=self.session.config.get("fill_auto", False),
                radio_fields=self.form_fields)
        )
        return d_vars


class DecisionWaitForGroup(WaitPage):
    wait_for_all_groups = False
    title_text = _("Veuillez patienter")
    body_text = _("Nous attendons les autres participants")
    after_all_players_arrive = "compute_payoffs"


class Result(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


page_sequence = [
    # Instructions,
    WaitForPairing,
    Decision, DecisionWaitForGroup,
    # Result
]
