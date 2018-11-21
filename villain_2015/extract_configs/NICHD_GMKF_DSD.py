# flake8: noqa

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map
)
from kf_lib_data_ingest.common import constants as kf_constants
import constants as omop_constants
from concept_schema import OMOP

source_data_url = (
    'file://~/Projects/kids_first/data/Vilain_2015/dbgap/NICHD_GMKF_DSD.xlsx'
)


source_data_loading_parameters = {}


def gender_map(x):
    m = {
        "female": omop_constants.CONCEPT.GENDER.FEMALE,
        "male": omop_constants.CONCEPT.GENDER.MALE,
        "default": omop_constants.CONCEPT.GENDER.UNKNOWN
    }
    return m.get(x, m.get('default'))


operations = [
    # person source value
    keep_map(
        in_col='submitted_subject_id_s',
        out_col=OMOP.PERSON.SOURCE_VALUE
    ),
    # person external_id
    keep_map(
        in_col='submitted_subject_id_s',
        out_col=OMOP.PERSON.ID
    ),
    # specimen source value
    keep_map(
        in_col='biospecimen_repository_sample_id_s',
        out_col=OMOP.SPECIMEN.ID
    ),
    # specimen datetime
    keep_map(
        in_col='LoadDate_s',
        out_col=OMOP.SPECIMEN.DATETIME
    ),
    # gender source value
    value_map(
        in_col="sex_s",
        m={
            "female": kf_constants.GENDER.FEMALE,
            "male": kf_constants.GENDER.MALE
        },
        out_col=OMOP.GENDER.SOURCE_VALUE
    ),
    # gender concept id
    value_map(
        in_col="sex_s",
        m=lambda x: gender_map(x),
        out_col=OMOP.GENDER.CONCEPT_ID
    ),
    # gender source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.GENDER.SOURCE_CONCEPT_ID
    ),
    # ethnicity source value
    constant_map(
        m=kf_constants.COMMON.NOT_REPORTED,
        out_col=OMOP.ETHNICITY.SOURCE_VALUE
    ),
    # ethnicity concept id
    constant_map(
        m=omop_constants.CONCEPT.ETHNICITY.UNKNOWN,
        out_col=OMOP.ETHNICITY.CONCEPT_ID
    ),
    # ethnicity source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.ETHNICITY.SOURCE_CONCEPT_ID
    ),
    # race source value
    constant_map(
        m=kf_constants.COMMON.NOT_REPORTED,
        out_col=OMOP.RACE.SOURCE_VALUE
    ),
    # race concept id
    constant_map(
        m=omop_constants.CONCEPT.RACE.UNKNOWN,
        out_col=OMOP.RACE.CONCEPT_ID
    ),
    # race source concept id (why??)
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.RACE.SOURCE_CONCEPT_ID
    ),
    # year of birth
    constant_map(
        m=0,
        out_col=OMOP.MEASUREMENT.YEAR_OF_BIRTH
    )


]
