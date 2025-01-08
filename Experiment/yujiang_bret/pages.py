from ._builtin import Page
from .models import Constants


class StartPart(Page):
    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Instructions(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return self.player.vars_for_template()

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Decision(Page):
    form_model = 'player'
    form_fields = ['bomb', 'boxes_collected', 'bomb_row', 'bomb_col']

    def vars_for_template(self) -> dict:
        return self.player.vars_for_template()

    def js_vars(self):
        reset = self.participant.vars.get('reset', False)
        if reset:
           del self.participant.vars['reset']

        input = not Constants.devils_game if not Constants.dynamic else False

        otree_vars = {
            'reset': reset,
            'input': input,
            'random': Constants.random,
            'dynamic': Constants.dynamic,
            'num_rows': Constants.num_rows,
            'num_cols': Constants.num_cols,
            'feedback': Constants.feedback,
            'undoable': Constants.undoable,
            'box_width': Constants.box_width,
            'box_height': Constants.box_height,
            'time_interval': Constants.time_interval,
        }
        otree_vars.update(dict(fill_auto=self.session.config.get("fill_auto", False)))
        return otree_vars

    def before_next_page(self):
        self.participant.vars['reset'] = True
        self.player.set_payoff()


class BePatient(Page):
    def vars_for_template(self):
        return self.player.vars_for_template()

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Results(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        the_dict = self.player.vars_for_template()
        the_dict["boxes_collected"] = self.player.boxes_collected
        the_dict["bomb"] = self.player.bomb
        the_dict["round_payoff"] = self.player.round_payoff
        return the_dict

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


page_sequence = [StartPart, Instructions, Decision, BePatient,
                 # Results
                 ]

