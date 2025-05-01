# Testing Guide for gnomAD MCP

This document provides comprehensive instructions for running, organizing, and understanding the tests for the gnomAD MCP project. It covers test execution, directory structure, version-specific notes, and CI/test script usage.

## Test Organization

### Directory Structure

```
tests/
├── __init__.py
├── test_gnomad_api.py      # Integration tests for high-level API functions
├── test_server.py          # Output and server-level tests
├── input/                  # Test input data
│   ├── analyzed_schemas/   # Analyzed schema data
│   ├── schema2query/      # Schema to query conversion
│   └── schemas/           # Raw schema files for each version
├── output/                 # Test output data
│   ├── server/            # Server test outputs
│   ├── v2/                # v2.1 test outputs
│   ├── v3/                # v3 test outputs
│   └── v4/                # v4 test outputs
├── scripts/               # Test utility scripts
└── tests/                 # Additional test modules
```

## Running Tests

### Server Tests

To run server tests:

```bash
bash tests/run_test_server.sh
```

### Version-Specific Tests

To run tests for a specific gnomAD version:

```bash
# For v2.1
bash tests/run_test_queries.sh v2

# For v3
bash tests/run_test_queries.sh v3

# For v4
bash tests/run_test_queries.sh v4
```

### Test Output

- Test outputs are saved in `tests/output/<version>/`
- Server test outputs are saved in `tests/output/server/`
- Previous outputs are automatically cleared before new test runs

### Version-Specific Notes

- v2.1 tests include liftover queries (skipped in v3/v4)
- v4 tests include new features like STR and CNV queries
- Schema differences are handled automatically by the QueryTemplateEngine

## Version Compatibility and Test Coverage

- All test parameters for each version are now managed as a single list:
  - `ALL_V2_TEST_PARAMS`
  - `ALL_V3_TEST_PARAMS`
  - `ALL_V4_TEST_PARAMS`
- Each list contains dicts specifying the query name (`query_name`), input parameters, and output file name (`_output_file`).
- The batch query runner automatically iterates over these lists and executes all supported test patterns for each version.
- Only supported queries and patterns are included in these lists; unsupported queries are not present and are automatically skipped.
- See the Supported Queries by Version table in the main README for details.
