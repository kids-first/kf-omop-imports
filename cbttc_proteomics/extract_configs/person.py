# flake8: noqa

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map
)
from kf_lib_data_ingest.common import constants as kf_constants
from common import constants as omop_constants
from common.concept_schema import OMOP
from common.athena import athena_cache

source_data_url = (
    'file://~/Projects/kids_first/data/CBTTC/proteomics/cbttc-proteomics.xlsx'
)


source_data_loading_parameters = {
    'sheet_name': 'All Fields - Included - 11_05_2'
}


def ethnicity_map(x):
    value = x.lower()
    if x.startswith('unavailable'):
        value = omop_constants.CONCEPT.COMMON.UNAVAILABLE
    else:
        value = athena_cache.lookup(x, query_params={
            'standardConcept': 'Standard',
            'domain': 'Ethnicity'
        })
    return value


def race_map(x):
    value = x.lower()
    if x.startswith('other'):
        value = omop_constants.CONCEPT.RACE.UNKNOWN
    else:
        value = athena_cache.lookup(x, query_params={
            'standardConcept': 'Standard',
            'domain': 'Race'
        })

    return value


operations = [
    # person source value
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.SOURCE_VALUE
    ),
    # person external_id
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.ID
    ),
    # gender source value
    keep_map(
        in_col="gender",
        out_col=OMOP.GENDER.SOURCE_VALUE
    ),
    # gender concept id
    value_map(
        in_col="gender",
        m=lambda x: athena_cache.lookup(x.lower(), query_params={
            'standardConcept': 'Standard',
            'domain': 'Gender'
        }),
        out_col=OMOP.GENDER.CONCEPT_ID
    ),
    # gender source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.GENDER.SOURCE_CONCEPT_ID
    ),
    # ethnicity source value
    keep_map(
        in_col="subject_ethnicity",
        out_col=OMOP.ETHNICITY.SOURCE_VALUE
    ),
    # ethnicity concept id
    value_map(
        in_col="subject_ethnicity",
        m=lambda x: ethnicity_map(x),
        out_col=OMOP.ETHNICITY.CONCEPT_ID
    ),
    # ethnicity source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.ETHNICITY.SOURCE_CONCEPT_ID
    ),
    # race source value
    keep_map(
        in_col='race',
        out_col=OMOP.RACE.SOURCE_VALUE
    ),
    # race concept id
    value_map(
        in_col='race',
        m=lambda x: race_map(x),
        out_col=OMOP.RACE.CONCEPT_ID
    ),
    # race source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.RACE.SOURCE_CONCEPT_ID
    ),
    # year of birth
    constant_map(
        m=0,
        out_col=OMOP.MEASUREMENT.YEAR_OF_BIRTH
    )


]
