# flake8: noqa
import datetime

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map,
    row_map
)
from kf_lib_data_ingest.common import constants as kf_constants
from common import constants as omop_constants
from common import athena
from common.concept_schema import OMOP
from common.athena import athena_cache

source_data_url = (
    'file://~/Projects/kids_first/data/CBTTC/proteomics/cbttc-proteomics.xlsx'
)


source_data_loading_parameters = {
    'sheet_name': 'All Fields - Included - 11_05_2'
}


def observation_id(row):
    external_id = ''
    components = ['research_id', 'age_of_last_known_status',
                  'last_known_status']

    external_id = '-'.join([f'{col}:{str(row[col])}' for col in components])

    return external_id


def vital_status(x):
    if 'alive' in x.lower():
        value = athena_cache.lookup(x.split('-')[0])
    else:
        value = omop_constants.CONCEPT.OUTCOME.VITAL_STATUS.DECEASED

    return value


operations = [
    # observation external_id
    row_map(
        m=lambda row: observation_id(row),
        out_col=OMOP.OBSERVATION.ID
    ),
    # person external_id
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.ID
    ),
    # observation source value
    keep_map(
        in_col='last_known_status',
        out_col=OMOP.OBSERVATION.SOURCE_VALUE
    ),
    # observation concept id
    value_map(
        in_col='last_known_status',
        m=lambda x: int(vital_status(x)),
        out_col=OMOP.OBSERVATION.CONCEPT_ID
    ),
    # observation_start_datetime
    # consider epoch to be person's year of birth
    value_map(
        in_col='age_of_last_known_status',
        m=lambda x: str(datetime.datetime.fromtimestamp(0) +
                        datetime.timedelta(float(x) - 1)),
        out_col=OMOP.OBSERVATION.DATETIME
    ),
    # observation_type_concept_id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.OBSERVATION.TYPE.CONCEPT_ID
    ),
    # observation source concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.OBSERVATION.SOURCE_CONCEPT_ID
    ),
    # obs_event_field_concept_id ?? what on earth is this
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.OBSERVATION.EVENT_FIELD.CONCEPT_ID
    )
]
