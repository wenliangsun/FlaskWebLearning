#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'swl'
__mtime__ = '8/6/18'
"""

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views
