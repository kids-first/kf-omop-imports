import os

from kf_lib_data_ingest.etl.configuration.log import setup_logger

from config import CONFIG_DIR, OUTPUT_DIR
from common import extract
from common import transform
from common import load


def main():
    # Out directory for caching stage outputs
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # Logger
    setup_logger(OUTPUT_DIR, overwrite_log=True)

    # Extract stage
    extract_configs = [os.path.join(CONFIG_DIR, fname)
                       for fname in os.listdir(CONFIG_DIR)
                       if os.path.isfile(os.path.join(CONFIG_DIR, fname))]
    data_dict = extract.run(OUTPUT_DIR, extract_configs)

    # Transform
    df_dict = transform.run(OUTPUT_DIR, data_dict)

    # Load
    load.run(df_dict)


if __name__ == '__main__':
    main()
