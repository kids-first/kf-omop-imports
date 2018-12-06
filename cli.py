import os

import click

from kf_lib_data_ingest.etl.configuration.log import setup_logger
from kf_lib_data_ingest.common.misc import import_module_from_file
from kf_model_omop.utils.misc import time_it


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Simple CLI for ingesting data into the Kids First OMOP db
    """
    pass


@click.command(name='ingest')
@click.argument('study_dir',
                type=click.Path(file_okay=False, dir_okay=True))
@click.option('--log_level', type=click.Choice(['debug', 'info',
                                                'warning', 'error']))
@time_it
def ingest(study_dir, log_level):
    """
    Ingest a study into the Kids First OMOP db

    \b
    Arguments:
        \b
        study_dir - Path to study directory containing extract_configs dir
    """
    from common import etl

    # Setup logging
    output_dir = _setup_output_and_logging(study_dir, log_level)

    # Get transformer
    study_transform = import_module_from_file(os.path.join(
        os.path.abspath(study_dir), 'transform.py'))

    # Run etl
    etl.run(study_dir, output_dir, study_transform.transform)


@click.command(name='drop')
@click.argument('study_dir',
                type=click.Path(file_okay=False, dir_okay=True))
@time_it
def drop(study_dir):
    """
    Drop a study in the Kids First OMOP db

    \b
    Arguments:
        \b
        study_dir - Path to study directory containing the id_cache.json file
        for the study
    """
    from common import delete

    # Setup logging
    _setup_output_and_logging(study_dir)

    # Drop
    delete.run(os.path.abspath(study_dir))


def _setup_output_and_logging(study_dir, log_level=None):
    # Create output directory for caching stage outputs
    output_dir = os.path.join(study_dir, 'output')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Logger
    kwargs = {
        'overwrite_log': True
    }
    if log_level:
        import logging
        log_level = getattr(logging, log_level.upper())
        kwargs.update({'log_level': log_level})

    setup_logger(output_dir, **kwargs)

    return output_dir


cli.add_command(ingest)
cli.add_command(drop)
