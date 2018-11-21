import os
import logging


from concept_schema import OMOP
from utils import merge_without_duplicates

logger = logging.getLogger(__name__)


def write_output(output_dir, df_out):
    """
    Write transform stage output
    """
    # Make stage output dir
    output_dir = os.path.join(output_dir, 'transform')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Write dfs to files
    for model_cls_name, df in df_out.items():
        fp = os.path.join(output_dir, model_cls_name + '.tsv')
        df.to_csv(fp, sep='\t')


def run(output_dir, data_dict):
    logger.info('BEGIN TransformStage')

    # Reorganize data - Dict (key=filename, value=df)
    dfs = {os.path.split(k)[1].split('.')[0]: df
           for k, (_, df) in data_dict.items()
           }

    # Make dataframes
    # Person
    persons = dfs['NICHD_GMKF_DSD']

    # Specimens
    specimens = dfs['3a_sample_attributes']
    specimens = merge_without_duplicates(persons, specimens,
                                         on=OMOP.SPECIMEN.ID)
    specimens = specimens.drop_duplicates(OMOP.SPECIMEN.ID)

    df_out = {
        'Person': persons,
        'Speciman': specimens
    }

    write_output(output_dir, df_out)

    logger.info('END TransformStage')

    return df_out
