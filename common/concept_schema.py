
"""
OMOP concept schema
"""

from kf_lib_data_ingest.etl.transform.standard_model.concept_schema import (
    PropertyMixin,
    _set_cls_attrs
)


class OmopMixin(PropertyMixin):
    SOURCE_VALUE = None
    SOURCE_CONCEPT_ID = None
    CONCEPT_ID = None


class OMOP:

    class PERSON(OmopMixin):
        pass

    class CONDITION(OmopMixin):
        DATETIME = None

        class STATUS(OmopMixin):
            pass

        class TYPE(OmopMixin):
            pass

    class SPECIMEN(OmopMixin):
        class DISEASE_STATUS(OmopMixin):
            pass

        class ANATOMIC_SITE(OmopMixin):
            pass

        class TYPE(OmopMixin):
            pass

        DATETIME = None

    class ETHNICITY(OmopMixin):
        pass

    class RACE(OmopMixin):
        pass

    class GENDER(OmopMixin):
        pass

    class MEASUREMENT:
        YEAR_OF_BIRTH = None


def compile_schema():
    """
    "Compile" the concept schema

    Populate every concept class attribute with a string that represents
    a path in the concept class hierarchy to reach that attribute.

    Store all the concept property strings in a set for later reference and
    validation.

    This approach eliminates the need to manually assign concept class
    attributes to a string.
    """

    property_path = []
    property_paths = set()
    _set_cls_attrs(OMOP, None, property_path, property_paths)

    return property_paths


compile_schema()
