import os
from pprint import pprint

from kf_lib_data_ingest.etl.extract.extract import ExtractStage


def run(output_dir, extract_configs):
    # Run extract
    es = ExtractStage(output_dir, extract_configs)
    df_out = es.run()

    # Write output files
    for url, (_, df) in df_out.items():
        fname = os.path.split(url)[1].split('.')[0]
        output_path = os.path.join(output_dir, (fname + '.tsv'))
        df.to_csv(output_path, sep='\t')

    return df_out
