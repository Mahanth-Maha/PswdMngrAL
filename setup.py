import os

class Install_dependencies:
    def __init__(self):
        self.pip_install()

    def pip_install(self):
        os.system("pip3 install selenium pynput PyCryptodome ")

Install_dependencies()
