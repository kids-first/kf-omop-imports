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


def condition_occur_id(row):
    external_id = ''
    components = ['research_id', 'sample_subject_name',
                  'diagnosis', 'diagnosis_type', 'age_of_initial_diagnosis',
                  'tumor_primary_location_in']

    external_id = '-'.join([f'{col}:{str(row[col])}' for col in components])

    return external_id


def condition_status(x):
    if 'initial' in x.lower():
        value = omop_constants.CONCEPT.DIAGNOSIS.PRELIMINARY
    elif 'progressive' in x.lower():
        value = omop_constants.CONCEPT.DIAGNOSIS.PROGRESSIVE
    elif 'recurrence' in x.lower():
        value = omop_constants.CONCEPT.DIAGNOSIS.RECURRENCE
    else:
        value = omop_constants.CONCEPT.COMMON.NO_MATCH

    return value


operations = [
    # condition_occurrence external_id
    row_map(
        m=lambda row: condition_occur_id(row),
        out_col=OMOP.CONDITION.ID
    ),
    # person external_id
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.ID
    ),
    # condition source value
    keep_map(
        in_col='diagnosis',
        out_col=OMOP.CONDITION.SOURCE_VALUE
    ),
    # condition concept id
    value_map(
        in_col='diagnosis',
        m=lambda x: int(athena_cache.lookup(
            x.split('/')[0].split('(')[0].strip(),
            query_params={'domain': 'Condition'})),
        out_col=OMOP.CONDITION.CONCEPT_ID
    ),
    # condition source concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.CONDITION.SOURCE_CONCEPT_ID
    ),
    # condition_start_datetime
    # consider epoch to be person's year of birth
    value_map(
        in_col='age_of_initial_diagnosis',
        m=lambda x: str(datetime.datetime.fromtimestamp(0) +
                        datetime.timedelta(float(x) - 1)),
        out_col=OMOP.CONDITION.DATETIME
    ),
    # condition_type_concept_id
    value_map(
        in_col='grade',
        m=lambda x: (omop_constants.CONCEPT.COMMON.UNAVAILABLE
                     if x.lower() == 'unavailable' else
                     int(athena_cache.lookup(x.split('/')[0]))
                     ),
        out_col=OMOP.CONDITION.TYPE.CONCEPT_ID
    ),
    # condition_status_source_value
    keep_map(
        in_col='diagnosis_type',
        out_col=OMOP.CONDITION.STATUS.SOURCE_VALUE
    ),
    # condition_status_concept_id
    value_map(
        in_col='diagnosis_type',
        m=lambda x: condition_status(x),
        out_col=OMOP.CONDITION.STATUS.CONCEPT_ID
    )
]
