import argparse as _argparse
import yaml as _yaml
from os import getenv as _getenv


class ArgEnvConfig:
    def __init__(self):
        self._environ = {}
        self._settings = {}
        self._arg = _argparse.ArgumentParser()

    def initialize_argparse(self,
                            prog=None,
                            usage=None,
                            description=None,
                            epilog=None,
                            parents=[],
                            formatter_class=_argparse.HelpFormatter,
                            prefix_chars='-',
                            fromfile_prefix_chars=None,
                            argument_default=None,
                            conflict_handler='error',
                            add_help=True,
                            allow_abbrev=True):

        self._arg = _argparse.ArgumentParser(prog,
                                             usage,
                                             description,
                                             epilog,
                                             parents,
                                             formatter_class,
                                             prefix_chars,
                                             fromfile_prefix_chars,
                                             argument_default,
                                             conflict_handler,
                                             add_help,
                                             allow_abbrev)

    def add_argument(self, *args, **kwargs):
        try:
            environ = kwargs.pop('environ')
        except KeyError:
            environ = None

        argument = self._arg.add_argument(*args, **kwargs)

        if environ:
            self._environ[argument.dest] = environ

    def get(self, value):
        args = self._arg.parse_args()
        try:
            result = getattr(args, value)
        except AttributeError:
            result = None
        if result is None:
            key = self._environ.get(value)
            if key:
                result = _getenv(key)
            else:
                result = self._settings.get(value)

        return result

    def get_args(self):
        return self._arg.parse_args()

    def load_settings(self, filepath):
        with open(filepath) as f:
            settings = _yaml.load(f)
        return settings

    def update_settings(self, filepath):
        with open(filepath) as f:
            settings = _yaml.load(f)

        self._settings.update(settings)
