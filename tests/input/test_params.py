"""
Unified test parameter lists for gnomAD MCP server tests (by version)

Each version's test parameters are provided as a single list:
- ALL_V2_TEST_PARAMS
- ALL_V3_TEST_PARAMS
- ALL_V4_TEST_PARAMS

Each list contains dicts with 'query_name', input parameters, and '_output_file'.
"""

from .test_params_v2 import ALL_V2_TEST_PARAMS
from .test_params_v3 import ALL_V3_TEST_PARAMS
from .test_params_v4 import ALL_V4_TEST_PARAMS