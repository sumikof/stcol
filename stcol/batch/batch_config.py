import os
import yaml

import settings

with open(os.path.join(settings.TOP_DIR, 'stcol', 'batch', f'batch_properties.yaml')) as yaml_file:
    batch_config = yaml.safe_load(yaml_file)
