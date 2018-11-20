import os
import logging

from kf_model_omop.model.models import Person

logger = logging.getLogger(__name__)


def run(data_dict):
    logger.info('BEGIN TransformStage')

    # Dict (key=filename, value=df)
    dfs = {os.path.split(k)[1].split('.')[0]: df
           for k, (_, df) in data_dict.items()
           }

    # Dict (keys=model class, value=df)
    df_out = {}

    # Make dataframes
    df_out[Person] = dfs['NICHD_GMKF_DSD']

    logger.info('END TransformStage')

    return df_out
