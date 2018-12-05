"""
OMOP Loader
"""
import os
import logging
from pprint import pformat, pprint
from copy import deepcopy

from kf_lib_data_ingest.common.misc import read_json, write_json
from kf_model_omop.factory import scoped_session
from kf_model_omop.model import models

from common.target_api_config import schema

logger = logging.getLogger(__name__)

id_model_map = {
    'person_id': 'Person',
    'specimen_id': 'Speciman',
    'condition_occurrence': 'ConditionOccurrence',
    'observation_id': 'Observation'
}


def _resolve_links(params, id_cache):
    """
    Look up the value of foreign key properties in the id_cache by the source
    ID or the value used to uniquely identify instances of model_name in the
    source data

    :param model_name: the SQLAlchemy model class name
    :param params: the dict of properties and values needed to create an
    instance of model
    :param id_cache: a dict storing the mapping of source IDs to primary keys
    """
    key = '_links'
    for property, value in params[key].items():
        foreign_model = id_model_map.get(property)
        id_fk_map = id_cache.get(foreign_model)
        if id_fk_map:
            params[key][property] = id_fk_map.get(value, value)

    params.update(params.pop('_links', None))

    return params


def _resolve_primary_key(model_name, params, id_cache):
    """
    Look up the value of the primary key in the id_cache by its source ID
    or the value used to uniquely identify instances of model_name in the
    source data

    :param model_name: the SQLAlchemy model class name
    :param params: the dict of properties and values needed to create an
    instance of model
    :param id_cache: a dict storing the mapping of source IDs to primary keys
    """
    for k, v in params['_primary_key'].items():
        primary_key = k
        source_id = str(v)
        primary_key_value = id_cache[model_name].get(source_id)

    params.pop('_primary_key', None)

    return primary_key, source_id, primary_key_value,


def _fill_values(target_schema, row):
    """
    Helper for load. Fills values of properties in the target schema given
    values from a row in the mapped dataframe
    """
    params = deepcopy(target_schema)

    for key, value in params.items():
        if key not in {'_links', '_primary_key'}:
            params[key] = row.get(value)

    for key in {'_links', '_primary_key'}:
        if params.get(key) is None:
            continue
        for property, value in params[key].items():
            params[key][property] = row.get(value)

    return params


def load(session, df_dict, id_cache, include_set):
    """
    Create instances of SQLAlchemy models populated with data from df_dict
    and update or insert them in the OMOP database

    :param session: the current db session
    :param df_dict: dict of dataframes keyed by model_name
    :param id_cache: dict storing source ID to primary key mapping
    """
    for model_cls_name, df in df_dict.items():
        if (include_set is not None) and model_cls_name not in include_set:
            continue
        # Lookup model class by name
        model_cls = getattr(models, model_cls_name)

        # Init id cache if needed
        if model_cls_name not in id_cache:
            id_cache[model_cls_name] = {}

        total = df.shape[0]
        logger.info(f'Loading {total} {model_cls_name} instances ...')

        # Get schema for target model
        target_schema = deepcopy(schema.get(model_cls_name))

        # Make model instances
        for i, row in df.iterrows():
            # Fill property values
            params = _fill_values(target_schema, row)
            # Translate values of link properties to db IDs
            result = _resolve_links(params, id_cache)

            (primary_key,
             source_id,
             primary_key_value) = _resolve_primary_key(model_cls_name,
                                                       result,
                                                       id_cache)
            logger.debug(f'\tAttempt load {i} of {total} {model_cls_name}: '
                         f'\n{pformat(result)}')
            logger.debug(f'{source_id} has pk {primary_key} = {primary_key_value}')

            # Create or update model instance
            instance = None
            if primary_key_value:
                instance = session.query(model_cls).get(primary_key_value)

            if instance:
                operation = 'Updated'
                for property, value in result.items():
                    setattr(instance, property, value)
                session.flush()
            else:
                operation = 'Created'
                # Reuse previously generated primary keys
                if primary_key_value:
                    result[primary_key] = primary_key_value
                instance = model_cls(**result)
                session.add(instance)
                session.flush()

                # Update id cache
                primary_key_value = getattr(instance, primary_key)
                id_cache[model_cls_name][source_id] = primary_key_value

            logger.info(f'\t{operation} {i} of {total} {model_cls_name}: '
                        f'\n{pformat(result)}')

        session.commit()


def run(df_dict, id_cache_filepath, include_set=None):
    """
    Entry point into the loader
    """
    logger.info('BEGIN LoadStage ...')

    # Read id cache
    id_cache = {}
    if os.path.isfile(id_cache_filepath):
        id_cache = read_json(id_cache_filepath)

    # Use the context managed session to interact with DB
    with scoped_session() as session:
        load(session, df_dict, id_cache, include_set)

    # Write id cache
    write_json(id_cache, id_cache_filepath)

    logger.info('END LoadStage ...')
