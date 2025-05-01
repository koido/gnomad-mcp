#!/usr/bin/env python3
"""
Unified GraphQL query runner for gnomAD API.
Usage:
  python -m gnomad.query --version v4 [--output-root <root>]

This script will:
- Dynamically load parameters from tests/input/test_params.py
- Discover available queries via generated query builder classes
- Fill in default variables (dataset, reference_genome) based on specified version
- Execute each GraphQL query against the gnomAD API
- Save each JSON response to tests/output/<version>/<query_name>.json
"""
import os
import sys
import json
import argparse
import asyncio
import re
from typing import Dict, Any
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Constants
GNOMAD_API_URL = "https://gnomad.broadinstitute.org/api"

# Version mappings
DATASET_MAP = {"v2": "gnomad_r2_1", "v3": "gnomad_r3", "v4": "gnomad_r4"}
ALL_DATASET_TO_VERSION = {
    "gnomad_r2_1": "v2",
    "gnomad_sv_r2_1": "v2",
    "gnomad_r3": "v3",
    "gnomad_r4": "v4",
    "gnomad_sv_r4": "v4",
    "gnomad_cnv_r4": "v4",
}
REF_GENOME_MAP = {"v2": "GRCh37", "v3": "GRCh38", "v4": "GRCh38"}

def get_client() -> Client:
    """
    Create and return a gnomAD GraphQL API client.

    Returns:
        Client: Configured gql Client instance for the gnomAD API.

    Example:
        >>> client = get_client()
    """
    transport = AIOHTTPTransport(url=GNOMAD_API_URL, ssl=True)
    return Client(transport=transport, fetch_schema_from_transport=False)

async def execute_query(query_string: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a GraphQL query asynchronously against the gnomAD API.

    Args:
        query_string (str): GraphQL query string.
        variables (Dict[str, Any]): Query variables.

    Returns:
        Dict[str, Any]: API response as a dictionary.

    Raises:
        Exception: For network or API errors.

    Example:
        >>> await execute_query('query { meta { apiVersion } }', {})
    """
    client = get_client()
    result = await client.execute_async(gql(query_string), variable_values=variables)
    return result

def execute_query_sync(query_string: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronous wrapper for execute_query. Handles event loop issues for Jupyter and other environments.

    Args:
        query_string (str): GraphQL query string.
        variables (Dict[str, Any]): Query variables.

    Returns:
        Dict[str, Any]: API response as a dictionary.

    Raises:
        RuntimeError: If the async query cannot be executed.
        Exception: For network or API errors.

    Example:
        >>> execute_query_sync('query { meta { apiVersion } }', {})
    """
    try:
        return asyncio.run(execute_query(query_string, variables))
    except RuntimeError:
        # If an event loop is already running (e.g., in Jupyter), use nest_asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(execute_query(query_string, variables))
        except Exception as e:
            raise RuntimeError(f"Failed to run async query: {e}")

def detect_version(dataset: str = None, reference_genome: str = None) -> str:
    """
    Detect gnomAD version string ("v2", "v3", "v4") from dataset or reference genome.

    Args:
        dataset (str, optional): gnomAD dataset ID (e.g., "gnomad_r2_1").
        reference_genome (str, optional): Reference genome (e.g., "GRCh37").

    Returns:
        str: Version string ("v2", "v3", or "v4").

    Raises:
        ValueError: If version cannot be determined.

    Example:
        >>> detect_version(dataset="gnomad_r4")
        'v4'
    """
    if dataset and dataset in ALL_DATASET_TO_VERSION:
        return ALL_DATASET_TO_VERSION[dataset]
    for ver, rg in REF_GENOME_MAP.items():
        if reference_genome and rg == reference_genome:
            return ver
    raise ValueError(f"Cannot detect version for dataset={dataset}, reference_genome={reference_genome}")

def run_query(query_name: str, variables: dict) -> dict:
    """
    Run a gnomAD GraphQL query with automatic version detection, default parameter completion, and query file loading.
    Checks if the query is supported for the detected version.

    Args:
        query_name (str): Query name (e.g., 'gene', 'region', etc.).
        variables (dict): Query variables (should include at least dataset or reference_genome if possible).

    Returns:
        dict: API response as a dictionary.

    Raises:
        ValueError: If version or query file cannot be determined, or if the query is not supported for the version.
        Exception: For network or API errors.

    Example:
        >>> run_query('gene', {'gene_symbol': 'BRCA2', 'reference_genome': 'GRCh38'})
    """
    version = variables.get('version')
    try:
        if not version:
            version = detect_version(variables.get('dataset'), variables.get('reference_genome'))
    except ValueError:
        return {"error": "Cannot determine version from dataset/reference_genome/version."}

    dataset = variables.get('dataset')
    try:
        if not dataset:
            dataset = DATASET_MAP[version]
    except ValueError:
        return {"error": "Cannot determine dataset from dataset/reference_genome/version."}

    reference_genome = variables.get('reference_genome')
    try:
        if not reference_genome:
            reference_genome = REF_GENOME_MAP[version]
    except ValueError:
        return {"error": "Cannot determine reference_genome from dataset/reference_genome/version."}

    # Import the version-specific query list
    if version == "v2":
        from gnomad.queries import v2 as version_queries
    elif version == "v3":
        from gnomad.queries import v3 as version_queries
    elif version == "v4":
        from gnomad.queries import v4 as version_queries
    else:
        raise ValueError(f"Unknown gnomAD version: {version}")
    if query_name not in version_queries.SUPPORTED_QUERIES:
        raise ValueError(f"Query '{query_name}' is not supported in gnomAD {version} (supported: {version_queries.SUPPORTED_QUERIES})")

    # Check consistency
    ## version
    if version != detect_version(dataset, reference_genome):
        raise ValueError(f"Inconsistent version: got {version}, expected {detect_version(dataset, reference_genome)}")

    query_path = os.path.join('gnomad', 'queries', version, f'{query_name}.graphql')
    if not os.path.exists(query_path):
        raise ValueError(f"Query file not found: {query_path}")
    with open(query_path) as f:
        query_str = f.read()
    return execute_query_sync(query_str, variables)

def run_query_with_metadata(query_name: str, variables: dict) -> dict:
    """
    Run a gnomAD query and return endpoint, request, variables, and response in a unified dict.
    Args:
        query_name (str): Query name
        variables (dict): Query variables
    Returns:
        dict: {endpoint, request_query, request_variables, response}
    """
    endpoint = GNOMAD_API_URL
    request_query = query_name
    request_variables = variables.copy()
    try:
        response = run_query(query_name, variables)
    except Exception as e:
        response = {"error": str(e)}
    return {
        "endpoint": endpoint,
        "request_query": request_query,
        "request_variables": request_variables,
        "response": response,
    }

def main() -> None:
    """
    Main entry point for running batch GraphQL queries against the gnomAD API.

    Loads version-specific parameters, discovers available queries, executes each query,
    and saves the response to the output directory.

    Raises:
        ValueError: If the specified version is not supported.
        Exception: For network or API errors or file I/O errors.

    Example:
        $ python -m gnomad.query --version v4 --output-root tests/output
    """
    parser = argparse.ArgumentParser(description="Run GraphQL queries against gnomAD API (introspection auto-expansion version).")
    parser.add_argument("--version", required=True, choices=list(DATASET_MAP.keys()), help="gnomAD version (e.g., v4)")
    parser.add_argument("--output-root", default="tests/output", help="Root output directory")
    args = parser.parse_args()

    version = args.version
    output_dir = os.path.join(args.output_root, version)
    os.makedirs(output_dir, exist_ok=True)

    import importlib
    # Import the unified test parameter list for the selected version
    if version == "v4":
        param_mod = importlib.import_module("tests.input.test_params_v4")
        all_params = getattr(param_mod, "ALL_V4_TEST_PARAMS")
    elif version == "v3":
        param_mod = importlib.import_module("tests.input.test_params_v3")
        all_params = getattr(param_mod, "ALL_V3_TEST_PARAMS")
    elif version == "v2":
        param_mod = importlib.import_module("tests.input.test_params_v2")
        all_params = getattr(param_mod, "ALL_V2_TEST_PARAMS")
    else:
        raise ValueError(f"Unsupported version: {version}")

    for param in all_params:
        params = param.copy()
        qname = params.pop("query_name")
        output_file = params.pop("_output_file", f"{qname}.json")
        out_path = os.path.join(output_dir, output_file)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        result = run_query_with_metadata(qname, params)
        with open(out_path, 'w') as outf:
            json.dump(result, outf, indent=2)
        print(f"Wrote response: {out_path}")

if __name__ == "__main__":
    main() 