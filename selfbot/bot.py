from os import listdir, path
from discord.ext import commands

from .config import Config


class SelfBot(commands.Bot):
    def __init__(self):
        self.config = Config()

        super().__init__(command_prefix=self.config['bot']['prefix'],
                         self_bot=True)

        self.load_extensions_from_path('selfbot/plugins')

    def run(self):
        if self.config['cred']['token'] is None:
            print('Add your token to "config/cred.yml".')
        else:
            super().run(self.config['cred']['token'], bot=False)

    def load_extensions_from_path(self, plugpath):
        for f in listdir(plugpath):
            file_path = path.join(plugpath, f)

            if path.isfile(file_path):
                filename, _ = path.splitext(file_path)
                modname = filename.replace('/', '.')
                print("loading:", modname)
                self.load_extension(modname)
