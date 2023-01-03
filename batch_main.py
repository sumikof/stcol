import sys
from logging import getLogger
from importlib import import_module

import  stcol.batch.batch_config

logger = getLogger(__name__)


def main(app_main, *param):
    from logging import basicConfig, INFO
    basicConfig(level=INFO)

    batch_config = stcol.batch.batch_config.batch_config
    # main(**settings.config)
    if app_main in batch_config and "command" in batch_config[app_main]:
        module = import_module(batch_config[app_main]["command"])
        module.main()


if __name__ == '__main__':
    main(*sys.argv[1:])
