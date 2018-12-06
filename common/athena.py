import os
import logging

import requests
import pandas as pd
from urllib.parse import urlencode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from kf_lib_data_ingest.common.misc import (
    read_json,
    write_json
)
from common.constants import CONCEPT

API_URL = 'http://athena.ohdsi.org/api/v1/concepts'
ATHENA_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'athena_cache.json')

logger = logging.getLogger(__name__)


class AthenaCache(object):

    def __init__(self):
        self.athena_cache = {}
        if os.path.isfile(ATHENA_CACHE_FILE):
            self.athena_cache = read_json(ATHENA_CACHE_FILE)

    def lookup(self, source_value, use_cache=True, query_params={}):
        """
        Lookup a concept by name via the Athena standard vocabulary API. First
        check local term cache stored in a JSON file.
        """
        concept = None

        logger.debug(f'Looking up standard concept for {source_value} ...')

        # Check local cache first
        if (use_cache and
            self.athena_cache and
                (source_value in self.athena_cache)):
            concept = self.athena_cache.get(source_value)
            logger.debug(f'Found concept_id {concept} for {source_value}'
                         ' in local cache')

        # Lookup term via Athena API
        else:
            query_params.update({'query': source_value.lower()})
            query_string = urlencode(query_params)

            response = requests.get(f'{API_URL}?{query_string}')

            if response.status_code == 200:
                result = response.json()

                # Apply fuzzy string match and filters
                athena_results = result['content']
                if athena_results:
                    concept = self._choose_best(source_value, athena_results)
                    logger.debug(
                        f'Found concept_id {concept} for {source_value}'
                        f' via Athena API {API_URL}')
            else:
                logger.info(response.text())

        if concept:
            concept['id'] = int(concept['id'])
            concept_id = concept['id']
            self.athena_cache[source_value] = concept
        else:
            concept_id = CONCEPT.COMMON.NO_MATCH
            logger.info(
                f'Could not find standard concept for {source_value}'
                f' via Athena API {API_URL}')

        return int(concept_id)

    def write_cache(self):
        """
        Write the cache which stores the mappings of source value to standard
        concepts to a JSON file
        """
        if self.athena_cache:
            write_json(self.athena_cache, ATHENA_CACHE_FILE)

    def _choose_best(self, source_value, athena_results,
                     use_standard_concept=False):
        """
        Apply fuzzy text search to Athena standard concept results. Athena API
        seems to use ILIKE and not fuzzy text string matching when searching
        for standard concepts that match the search term.

        Apply additional optional filters (i.e domain == Condition). Filters
        are ANDed together.

        :param athena_results: list of dicts containing standard concepts
        returned by Athena concept search API
        """
        concept = athena_results[0]

        # Fuzzy text search
        fuzzy_results = process.extract(source_value, athena_results,
                                        scorer=fuzz.token_sort_ratio)
        fuzzy_results_df = pd.DataFrame([r[0] for r in fuzzy_results])

        # Apply filters
        filtered_df = fuzzy_results_df[
            fuzzy_results_df['invalidReason'] == 'Valid']
        if use_standard_concept:
            filters = [('standardConcept', 'Standard')]
            for f in filters:
                if not filtered_df.empty:
                    filtered_df = filtered_df[filtered_df[f[0]] == f[1]]

        # Choose best result
        if not filtered_df.empty:
            concept = filtered_df.iloc[0].to_dict()
        elif not fuzzy_results_df.empty:
            concept = fuzzy_results_df.iloc[0].to_dict()

        return concept


athena_cache = AthenaCache()
