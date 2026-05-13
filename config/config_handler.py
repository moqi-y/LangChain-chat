import os

import yaml

DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(DIR, "config.yml")


def load_config(path: str = CONFIG_PATH, encoding="utf-8"):
    with open(path, 'r', encoding=encoding) as file:
        config = yaml.safe_load(file)
    return config


config = load_config()

__all__ = ["config"]

if __name__ == '__main__':
    print(config['dirs']['data'])
