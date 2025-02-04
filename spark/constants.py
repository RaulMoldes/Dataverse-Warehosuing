
DOI  = "10.7910/DVN/HG7NV7"

DATAVERSE = f"https://dataverse.harvard.edu/api/v1/datasets/:persistentId?persistentId=doi:{DOI}"
DOWNLOADS = "https://dataverse.harvard.edu/api/access/datafile/"

DATA_PATH = ""
PREPROCESSING_CONFIG = {
    "DepTime": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "ArrTime": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "CRSDepTime": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "CRSArrTime": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "ArrDelay": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "DepDelay": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "Distance": {
        "coalesce": [-1, "NA", ""],
        "coalesced_value": None
    },
    "ActualElapsedTime": {
         "coalesce": [-1, "NA", ""],
         "coalesced_value": None,
        "set_min_value": 0
    },
    "AirTime": {
         "coalesce": [-1, "NA", ""],
         "coalesced_value": None,
        "set_min_value": 0
    },
    "TaxiIn": {
         "coalesce": [-1, "NA", ""],
         "coalesced_value": None,
        "set_min_value": 0
    },
    "TaxiOut": {
         "coalesce": [-1, "NA", ""],
         "coalesced_value": None,
        "set_min_value": 0
    },
    "Diverted": {
        "set_min_value": 0,
        "set_max_value": 1
    },
    "Cancelled": {
        "set_min_value": 0,
        "set_max_value": 1
    },
    "Month": {
        "set_min_value": 1,
        "set_max_value": 12
    },
    "DayOfWeek": {
        "set_min_value": 1,
        "set_max_value": 7
    },
    "DayOfMonth": {
        "set_min_value": 1,
        "set_max_value": 31
    }
}