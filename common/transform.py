import os
import logging

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


def run(output_dir, data_dict, transform_func):
    """
    Transform mapped data tables into merged dataframes, one df for each
    target entity type. transform_func must return a dict where keys are names
    of OMOP SQLAlchemy models:

        df_out = {
            'Person': person_df,
            'Speciman': specimen_df
        }

    :param output_dir: Study directory's output dir
    :param data_dict: Dict of mapped dfs from extract stage
    :transform_funct: function pointer to a method that merges dfs from
    data_dict into the form described above.
    """
    logger.info('BEGIN TransformStage')

    # Reorganize data - Dict (key=filename, value=df)
    dfs = {os.path.split(k)[1].split('.')[0]: df
           for k, (_, df) in data_dict.items()
           }

    # Make dataframes
    df_out = transform_func(dfs)

    write_output(output_dir, df_out)

    logger.info('END TransformStage')

    return df_out
