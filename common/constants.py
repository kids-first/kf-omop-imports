"""
OMOP Constants
"""


class CONCEPT:

    class DIAGNOSIS:
        PRELIMINARY = 3046688
        RECURRENCE = 4082492
        PROGRESSIVE = 4114504

    class SPECIMEN:

        class ANATOMIC_SITE:
            pass

        class COMPOSITION:
            BLOOD = 4001225

        class TYPE:
            TUMOR = 4122248

    class COMMON:
        NO_MATCH = 0

    class GENDER:
        FEMALE = 8532
        MALE = 8507
        UNKNOWN = 8551

    class ETHNICITY:
        HISPANIC = 38003563
        NOT_HISPANIC = 38003564
        UNKNOWN = 759814

    class RACE:
        WHITE = 8527
        AFRICAN = 8516
        ASIAN = 8515
        PACIFIC_ISLANDER = 8557
        AMERICAN_INDIAN = 8657
        UNKNOWN = 8552
