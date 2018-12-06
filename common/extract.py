import os

from kf_lib_data_ingest.etl.extract.extract import ExtractStage
from common.athena import athena_cache


def run(output_dir, extract_configs):
    # Make output dir
    output_dir = os.path.join(output_dir, 'extract')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Run
    es = ExtractStage(output_dir, extract_configs)
    df_out = es.run()

    # Write output files
    for url, (_, df) in df_out.items():
        fname = os.path.split(url)[1].split('.')[0]
        output_path = os.path.join(output_dir, (fname + '.tsv'))
        df.to_csv(output_path, sep='\t')

    # Write athena cache to file
    athena_cache.write_cache()

    return df_out
