from storyteller.storyteller_settings import *

INSTALLED_APPS = INSTALLED_APPS + ('storyteller.exbase.apps.ExConfig',)

BASE_CHARACTER_TYPECLASS = "storyteller.exalted3.classes.Ex3Character"

# CALENDAR
TIME_FACTOR = 3.0
TIME_SEC_PER_MIN = 60
TIME_MIN_PER_HOUR = 60
TIME_HOUR_PER_DAY = 24
TIME_DAY_PER_WEEK = 7
TIME_WEEK_PER_MONTH = 4
TIME_MONTH_PER_YEAR = 15

#ROOT_URLCONF = 'storyteller.exalted3.urls'