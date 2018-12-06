
from common.concept_schema import OMOP
from common.utils import merge_without_duplicates


def transform(dfs):
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

    return df_out
