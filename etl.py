import argparse
import os

from kf_lib_data_ingest.etl.configuration.log import setup_logger

from common import extract
from common import transform
from common import load


def main(study_dir):
    # Create output directory for caching stage outputs
    output_dir = os.path.join(study_dir, 'output')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Logger
    setup_logger(output_dir, overwrite_log=True)

    # Extract stage
    config_dir = os.path.join(study_dir, 'extract_configs')
    extract_configs = [os.path.join(config_dir, fname)
                       for fname in os.listdir(config_dir)
                       if os.path.isfile(os.path.join(config_dir, fname))]
    data_dict = extract.run(output_dir, extract_configs)

    # Transform
    df_dict = transform.run(output_dir, data_dict)

    # Load
    id_cache_file = os.path.join(study_dir, 'id_cache.json')
    load.run(df_dict, id_cache_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('study_dir', help='Path to study directory containing '
                        'extract_configs dir')

    args = parser.parse_args()
    main(args.study_dir)
