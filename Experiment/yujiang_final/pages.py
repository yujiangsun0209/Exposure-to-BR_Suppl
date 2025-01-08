from ._builtin import Page


class Final(Page):
    form_model = "player"
    form_fields = ["comments"]

    def js_vars(self):
        return dict(fill_auto=self.session.config.get("fill_auto", False))


class Final_after_comments(Page):
    def js_vars(self):
        return dict(fill_auto=False)


page_sequence = [Final, Final_after_comments]
