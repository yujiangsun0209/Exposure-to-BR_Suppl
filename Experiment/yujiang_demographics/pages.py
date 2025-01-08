from django.utils.translation import gettext as _

from ._builtin import Page


class DemogQuestionnaire(Page):
    form_model = "player"
    form_fields = ["year_of_birth", "gender", "nationality", "marital_status",
                   "student", "socioprofessional_group", "study_level", "study_discipline", "politique",
                   "experiment_participation"]

    def error_message(self, values):
        if values["student"] == 0 and values["socioprofessional_group"] is None:
            return _("Select your socio-professional group")

    def js_vars(self):
        return dict(
            fill_auto=self.session.config.get("fill_auto", False),
            radio_fields=["student", "experiment_participation"]
        )


page_sequence = [DemogQuestionnaire]
