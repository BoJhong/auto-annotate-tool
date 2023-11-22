import collections.abc
import os

import toml


class TOMLConfig:
    instance = None

    def __init__(self, file):
        TOMLConfig.instance = self
        with open(os.path.join(os.getcwd(), file), "r", encoding="utf-8") as f:
            self.env = toml.load(f)
        self.file = file

    def update(self, new_config):
        with open(self.file, "r") as f:
            existing_config = toml.load(f)

        for key, value in existing_config.items():
            if value in ["true", "false"]:
                existing_config[key] = True if value == "true" else False

        self._update_config(existing_config, new_config)

        with open(self.file, "w") as f:
            f.write(toml.dumps(existing_config))

    def _update_config(self, existing_config, new_config):
        for key, value in new_config.items():
            if isinstance(value, collections.abc.Mapping):
                self._update_config(existing_config.setdefault(key, {}), value)
            else:
                existing_config[key] = value
