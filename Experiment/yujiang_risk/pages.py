from ._builtin import Page


class StartPart(Page):
    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Risk(Page):
    form_model = "player"
    form_fields = [
        "risque_general", "risque_sante", "risque_argent", "patience", "confiance_autres",
        "confiance_autres_general", "confiance_autres_famille", "confiance_autres_travail"
    ]

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


page_sequence = [StartPart, Risk]
