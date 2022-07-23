from .exbase_settings import *

STORY_TEMPLATE_PATHS.extend([
    "storyteller.exalted2.templates"
])

SYSTEMS.extend([
    "storyteller.systems.Exalted2System"
])

# HOUSE RULES TERRITORY

# Set this true to enable Firearms and Drive and associated stats.
EXALTED_SHARDS = False

# If true, personal and peripheral essence pool calculations will treat
# all Virtues to be 5, even if they are not.
EXALTED_POOL_MAX_VIRTUES = False