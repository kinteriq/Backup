import os

# This is the path to .json file where all shortcuts will be saved
custom_datapath = ''

# Default path to .json file is the directory with this config file
__default_datapath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'shortcuts.json'))

DATAPATH = custom_datapath or __default_datapath
