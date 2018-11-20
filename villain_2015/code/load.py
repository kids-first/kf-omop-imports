"""
OMOP Loader
"""
import logging
from pprint import pformat
from copy import deepcopy

from kf_model_omop.factory import scoped_session
from target_api_config import schema

logger = logging.getLogger(__name__)


def delete_all(session, df_dict):
    logger.info('Deleting all previously loaded OMOP instances')
    for model_cls in df_dict.keys():
        results = session.query(model_cls).all()
        logger.info(f'{len(results)} {model_cls.__name__} deleted')
        for r in results:
            session.delete(r)
        session.commit()


def load(session, df_dict):
    for model_cls, df in df_dict.items():
        total = df.shape[0]
        logger.info(f'Loading {total} {model_cls.__name__} instances ...')

        target_schema = deepcopy(schema.get(model_cls.__name__))

        for i, row in df.iterrows():
            result = {property: row.get(mapped_column)
                      for property, mapped_column in target_schema.items()
                      }
            logger.info(f'\t{i} of {total} {model_cls.__name__}: '
                        f'\n{pformat(result)}')

            session.add(model_cls(**result))
            session.commit()


def run(df_dict):
    logger.info('BEGIN LoadStage ...')

    # Use the context managed session to interact with DB
    with scoped_session() as session:
        delete_all(session, df_dict)
        load(session, df_dict)

    logger.info('END LoadStage ...')
