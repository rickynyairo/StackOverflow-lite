"""
This module sets up the questions resource

Authored by: Ricky Nyairo
"""
from flask import Blueprint

version1 = Blueprint('version1', __name__)

from . import questions, users
