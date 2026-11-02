"""
Main Application Entry Point — AgriVision AI.
Launches the Executive Dashboard and sets up multi-page navigation.
"""

import os
import sys

# Ensure matplotlib cache is in /tmp/matplotlib
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

# Execute Dashboard code
with open(os.path.join(PROJECT_ROOT, "pages", "1_Dashboard.py")) as f:
    code = compile(f.read(), "1_Dashboard.py", "exec")
    exec(code)
