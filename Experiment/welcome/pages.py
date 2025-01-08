from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import get_language


class Welcome(Page):
    def vars_for_template(self):
        return dict(language=get_language())

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class WelcomeWaitForAll(WaitPage):
    pass


page_sequence = [Welcome,
                 # WelcomeWaitForAll
                 ]
