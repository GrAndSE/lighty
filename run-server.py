"""Base settings for all environments
"""
import os, sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

def get_path(*args):
    return os.path.join(PROJECT_PATH, *args)
sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, get_path("libs"))
sys.path.insert(0, get_path("apps"))


from lighty.wsgi import run_server
run_server()
