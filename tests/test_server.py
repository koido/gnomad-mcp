#!/usr/bin/env python3
"""
Tests for gnomAD MCP server.
"""

import os
import json
import pytest
from pathlib import Path

# Ensure tests run from project root so query files can be located
os.chdir(os.path.dirname(os.path.dirname(__file__)))

from tests.input.test_params import (
    ALL_V2_TEST_PARAMS,
    ALL_V3_TEST_PARAMS,
    ALL_V4_TEST_PARAMS,
)

from server import (
    get_gene_info,
    search_for_genes,
    get_region_info,
    get_variant_info,
    get_clinvar_variant_info,
    get_mitochondrial_variant_info,
    get_structural_variant_info,
    get_copy_number_variant_info,
    search_for_variants,
    get_variant_liftover,
    get_str_info,
    get_metadata,
)

OUTPUT_DIR = Path("tests/output/server")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

QUERY_NAME_TO_FUNC = {
    "gene": get_gene_info,
    "gene_search": search_for_genes,
    "region": get_region_info,
    "variant": get_variant_info,
    "clinvar_variant": get_clinvar_variant_info,
    "mitochondrial_variant": get_mitochondrial_variant_info,
    "structural_variant": get_structural_variant_info,
    "copy_number_variant": get_copy_number_variant_info,
    "variant_search": search_for_variants,
    "liftover": get_variant_liftover,
    "short_tandem_repeat": get_str_info,
    "meta": get_metadata,
}

def save_json_result(filename: str, result: dict):
    out_path = OUTPUT_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

@pytest.mark.parametrize("params", ALL_V4_TEST_PARAMS)
def test_mcp_server_v4(params):
    params = params.copy()
    query_name = params.pop("query_name")
    output_file = params.pop("_output_file", f"v4_{query_name}.json")
    func = QUERY_NAME_TO_FUNC[query_name]
    try:
        result = func(**params)
    except Exception as e:
        result = {"error": str(e)}
    save_json_result(f"v4_{output_file}", result)

@pytest.mark.parametrize("params", ALL_V3_TEST_PARAMS)
def test_mcp_server_v3(params):
    params = params.copy()
    query_name = params.pop("query_name")
    output_file = params.pop("_output_file", f"v3_{query_name}.json")
    func = QUERY_NAME_TO_FUNC[query_name]
    try:
        result = func(**params)
    except Exception as e:
        result = {"error": str(e)}
    save_json_result(f"v3_{output_file}", result)

@pytest.mark.parametrize("params", ALL_V2_TEST_PARAMS)
def test_mcp_server_v2(params):
    params = params.copy()
    query_name = params.pop("query_name")
    output_file = params.pop("_output_file", f"v2_{query_name}.json")
    func = QUERY_NAME_TO_FUNC[query_name]
    try:
        result = func(**params)
    except Exception as e:
        result = {"error": str(e)}
    save_json_result(f"v2_{output_file}", result)

if __name__ == "__main__":
    print("🧪 Running gnomAD MCP server output tests")
    print("=" * 50)
    pytest.main(["-xvs", __file__]) 