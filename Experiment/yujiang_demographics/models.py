from datetime import date

from django.utils.translation import gettext as _
from django_countries import countries
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    widgets
)

author = 'D. Dubois'

doc = """
Questionnaire demographique
"""


class Constants(BaseConstants):
    name_in_url = 'ysdem'
    players_per_group = None
    num_rounds = 1

    disciplines = [
        _("Administration"), _("Archeology"), _("Biology"),
        _("Buisiness school"), _("Chemistry"),
        _("Computer science"), _("Economics"),
        _("Education"), _("Law"), _("Management"),
        _("Nursing school"), _("Engineering"), _("Foreing language"),
        _("Geography"),
        _("History"), _("Letters"), _("Mathematics"),
        _("Medicine"), _("Music"), _("Pharmacy"),
        _("Philosophy"), _("Physics"), _("Politics"),
        _("Psychology"), _("Sociology"), _("Sport"),
        _("-- Not in the list --")
    ]

    revenus = [
        "moins de 1000", "[1000 - 2000)", "[2000-3000)", "[3000-4000)", "[4000-5000)", "[5000-6000)", "[6000-7000)",
        "7000 et plus"
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    year_of_birth = models.IntegerField(
        choices=range(date.today().year - 15, date.today().year - 101, -1), label=_("Year of birth")
    )
    gender = models.IntegerField(choices=[(0, _("Female")), (1, _("Male"))], label=_("Gender"))
    nationality = models.StringField(
        label=_("Nationality"), choices=countries, blank=False)
    marital_status = models.IntegerField(
        choices=list(zip(range(5), [_("Single"), _("Pacsé(e)"), _("Married"), _("Divorced"), _("Widowed")])),
        label=_("Marital status")
    )
    student = models.BooleanField(label=_("Are you a student"), widget=widgets.RadioSelectHorizontal)
    study_level = models.IntegerField(
        choices=list(zip(range(8), ["Bac", "Bac+1", "Bac+2", "Bac+3", "Bac+4", "Bac+5", "Bac+6", "Bac+8"])),
        label=_("Level of study")
    )
    study_discipline = models.IntegerField(
        choices=list(zip(range(len(Constants.disciplines)), Constants.disciplines)), label=_("Discipline of study")
    )
    socioprofessional_group = models.IntegerField(
        choices=[(1, _("Agriculteurs exploitants")),
                 (2, _("Artisans, commerçants et chefs d’entreprise")),
                 (3, _("Cadres et professions intellectuelles supérieures")),
                 (4, _("Professions Intermédiaires")),
                 (5, _("Employés")),
                 (6, _("Ouvriers")),
                 (7, _("Retraités")),
                 (8, _("Autres personnes sans activité professionnelle"))],
        label=_("Socio-professional group"), blank=True
    )
    politique = models.IntegerField(
        choices=[(0, "0 - Fortement à gauche"), (1, 1), (2, 2), (3, 3),
                 (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                 (10, "10 - Fortement à droite")],
        label=_("En matière politique, les gens sont souvent catégorisés comme étant de 'gauche' ou de 'droite'. Sur "
                "une échelle de 0 (très à gauche) à 10 (très à droite) comment diriez-vous que vous vous situez ?")
    )
    experiment_participation = models.BooleanField(label=_("Have you ever participated to an economic experiment ?"),
                                                   widget=widgets.RadioSelectHorizontal)
