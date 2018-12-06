import pandas as pd


def transform(dfs):

    # Person
    persons = dfs['person']

    # Specimens
    specimens = dfs['specimen']

    # Diagnoses - condition occurrence
    diagnoses = dfs['diagnosis']

    # Outcomes
    outcomes = dfs['outcome']

    # Radiations
    radiations = dfs['radiation']

    # Chemotherapies
    chemos = dfs['chemotherapy']

    procedure_occurs = pd.concat([radiations, chemos], ignore_index=True)

    df_out = {
        'Person': persons,
        'ConditionOccurrence': diagnoses,
        'Speciman': specimens,
        'Observation': outcomes,
        'ProcedureOccurrence': procedure_occurs
    }

    return df_out
