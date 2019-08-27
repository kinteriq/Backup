import pytest
import os
import sqlite3

PATH = os.path.join(os.getcwd(), 'test.db')
SHORTCUT_NAMES = ('TEST_1', 'TEST_2')

testsource1 = os.path.join(os.getcwd(), 'TEST_BACKUP_SOURCE_001')
testdestination1 = os.path.join(os.getcwd(), 'TEST_BACKUP_DESTINATION_001')
testsource2 = os.path.join(os.getcwd(), 'TEST_BACKUP_SOURCE_002')
testdestination2 = os.path.join(os.getcwd(), 'TEST_BACKUP_DESTINATION_002')


DATA_1 = (SHORTCUT_NAMES[0], testsource1, testdestination1)
DATA_2 = (SHORTCUT_NAMES[1], testsource2, testdestination2)


# # TODO create fixture
# if __name__ == '__main__':
#     def main(create_db):
#         print(PATH)
#         connection = sqlite3.connect(PATH)
#         cursor = connection.cursor()
#         selection = cursor.execute('''SELECT * FROM shortcuts''')
#         for row in selection:
#             print(row)
#     main(create_db)
#     print(os.path.exists(PATH))
#     os.remove(PATH)
