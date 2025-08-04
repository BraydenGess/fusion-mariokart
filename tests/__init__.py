import warnings
from urllib3.exceptions import NotOpenSSLWarning

def pytest_load_initial_conftests(args):
    print('Running this function')
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)