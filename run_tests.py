import warnings
warnings.filterwarnings("ignore", module="urllib3")

import pytest
import sys

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "tests"]))