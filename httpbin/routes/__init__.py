# -*- coding: utf-8 -*-

"""
httpbin.routes
~~~~~~~~~~~~~~

Route modules for httpbin API testing endpoints.
"""

from .advanced.advanced_routes import advanced_bp
from .basic.api_routes import api_bp
from .data.data_routes import data_bp
from .testing.simulation_routes import sim_bp
from .utils.utility_routes import util_bp

__all__ = ["api_bp", "data_bp", "sim_bp", "util_bp", "advanced_bp"]
