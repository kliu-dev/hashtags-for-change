from .filepaths import *
from .pipeline import *
import pandas as pd

def main():
    # initialize dictionary for file paths and reaad in acled data
    tier1, tier2, tier3 = create_paths_dict()
    acled = read_acled()

    # check that paths are valid
    validate_paths(tier1)
    validate_paths(tier2)
    validate_paths_tier3(tier3)

    # run analysis & make graphs
    tier1_integration(tier1, acled)
    tier2_integration(tier2, acled)
    tier3_integration(tier3, acled)


if __name__ == "__main__":
    main()