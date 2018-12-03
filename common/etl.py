import os

from common import extract
from common import transform
from common import load


def run(study_dir, output_dir, transform_func):

    # Extract stage
    config_dir = os.path.join(study_dir, 'extract_configs')
    extract_configs = [os.path.join(config_dir, fname)
                       for fname in os.listdir(config_dir)
                       if os.path.isfile(os.path.join(config_dir, fname))]
    data_dict = extract.run(output_dir, extract_configs)

    # Transform
    df_dict = transform.run(output_dir, data_dict, transform_func)

    # Load
    id_cache_file = os.path.join(study_dir, 'id_cache.json')
    load.run(df_dict, id_cache_file)
