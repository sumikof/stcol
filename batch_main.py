import sys
from logging import getLogger
import batch.properties
from importlib import import_module

logger = getLogger(__name__)


def main(app_main, *param):
    from logging import basicConfig, INFO
    basicConfig(level=INFO)
    # main(**settings.config)
    if app_main in batch.properties.module:
        module = import_module(batch.properties.module[app_main])
        module.main()


if __name__ == '__main__':
    main(*sys.argv[1:])
