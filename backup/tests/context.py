import os
import sys

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backup
import backup.backup # test imports from backup/backup.py
