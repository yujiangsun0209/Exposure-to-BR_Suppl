import time
from ._builtin import Page
from .models import Constants
from django.utils.translation import gettext as _


class StartExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class AboutExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Instruction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(time_given=Constants.time_given // 60)

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))

    def before_next_page(self):
        self.participant.vars['expiry'] = time.time() + 1.0 * Constants.time_given


class Sliders(Page):
    form_model = 'player'
    form_fields = ['slider1', 'slider2', 'slider3', 'slider4', 'slider5', 'slider6', 'slider7', 'slider8', 'slider9',
                   'slider10']

    timer_text = _("Time left") + " : "

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return dict(
            slider_goals_this_round=self.participant.vars[f'slider_goals_{self.round_number}']
        )

    def js_vars(self):
        return dict(
            fill_auto=self.session.config.get("fill_auto", False),
            slider_goals_this_round=self.participant.vars[f'slider_goals_{self.round_number}']
        )

    def before_next_page(self):
        self.player.check_slider_answers()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            player_in_all_rounds=self.player.in_all_rounds(),
            total_sliders_correct=sum([p.total_sliders_correct for p in self.player.in_all_rounds()])
        )

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


page_sequence = [
    AboutExperiment, Instruction, Sliders, Results
]
