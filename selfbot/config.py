from os import path, listdir, makedirs
import yaml


class Config(dict):
    def __init__(self):
        super().__init__()
        self.tmpdir = 'tmp'
        self.configdir = 'config'
        self.statedir = path.join(self.tmpdir, 'state')

        self.load_defaults()
        self.load_overrides()

        # self.load_states()

    def __repr__(self):
        return repr(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def load_defaults(self):
        config_path = path.join(self.configdir, 'defaults')
        self.load_yaml(config_path)

    def load_overrides(self):
        self.load_yaml(self.configdir)

    def load_yaml(self, config_path):
        for f in listdir(config_path):
            file_path = path.join(config_path, f)

            if path.isfile(file_path):
                with open(file_path) as config_file:
                    yml = yaml.safe_load(config_file)
                    filename, _ = path.splitext(f)
                    self.__dict__[filename] = yml

    # def load_states(self):
    #     if not path.exists(self.statedir):
    #         makedirs(self.statedir)
    #
    #     for root, dirs, files in walk(self.statedir):
    #         for f in files:
    #             self.load(f)

    def load(self, key):
        file_path = path.join(self.statedir, key)

        with open(file_path) as f:
            self.config['bot'][key] = f.read()

    def save(self, key, value):
        file_path = path.join(self.statedir, key)

        with open(file_path) as f:
            f.write(value)
