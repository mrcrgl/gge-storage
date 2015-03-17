__author__ = 'mriegel'

import os

environment = os.environ.get("DJANGO_ENV", "staging")

if environment == "staging":
    from .staging import *

if environment == "development":
    from .development import *