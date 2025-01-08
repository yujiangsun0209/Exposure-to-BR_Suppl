from os import environ

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
SECRET_KEY = ''
INSTALLED_APPS = ['otree']

DEMO_PAGE_INTRO_HTML = """
"""
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    fill_auto=False,
)

ROOMS = []

LANGUAGE_CODE = 'fr'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False
POINTS_CUSTOM_NAME = 'ECU'

SESSION_CONFIGS = [
    dict(
        name='yujiang',
        display_name="Yujiang",
        num_demo_participants=2,
        app_sequence=['welcome', 'yujiang_sliders', 'yujiang_main', 'yujiang_bret', 'yujiang_svo', 'yujiang_risk',
                   'yujiang_demographics', "yujiang_final"],
        treatment=1,   # values from 0 to 4
    ),
]
