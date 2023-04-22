from prometheus_client import Histogram

LOAN_CONTROLLER_TIME_LATENCY = Histogram("loan_list", 'Response latency')

LOAN_CONTROLLER_NUMBER_OF_OBSERVATION = Histogram("loan_list_observe", 'Request size')