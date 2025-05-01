# gnomAD MCP Server

## Overview

This MCP server provides a programmatic interface to the Genome Aggregation Database ([gnomAD](https://gnomad.broadinstitute.org/)) API, supporting multiple API versions (**v2.1.1**, **v3.1.2**, **v4.1.0**).  
It abstracts version-specific field and schema differences, exposing a unified API for downstream tools and users.

## Status

🚧 **Under Active Development** 🚧

This project is under active development. APIs and features may change without notice.

## Supported gnomAD API Versions

- **v4.1.0** (`gnomad_r4`)
- **v3.1.2** (`gnomad_r3`)
- **v2.1.1** (`gnomad_r2_1`)

## Supported Queries by Version

The following table summarizes which queries are available for each gnomAD API version:

| Query Type                    | Description                                                      | v2  | v3  | v4  |
|-------------------------------|------------------------------------------------------------------|-----|-----|-----|
| get_gene_info                 | Retrieve gene metadata and constraint metrics (direct lookup by gene_id/gene_symbol) | ❌  | ❌  | ✅  |
| get_region_info               | Retrieve variant and summary information for a genomic region    | ❌  | ❌  | ✅  |
| get_variant_info              | Retrieve variant metadata and population frequency data (by variantId) | ✅  | ✅  | ✅  |
| get_clinvar_variant_info      | Retrieve ClinVar variant data and clinical significance          | ✅  | ✅  | ✅  |
| get_mitochondrial_variant_info| Retrieve mitochondrial variant data and population frequencies   | ❌  | ❌  | ✅  |
| get_structural_variant_info   | Retrieve structural variant (SV) data and population frequencies | ✅  | ❌  | ✅  |
| get_copy_number_variant_info  | Retrieve copy number variant (CNV) data and population frequencies| ❌  | ❌  | ✅  |
| search_for_genes              | Search for genes by symbol or name (no direct gene_id lookup in v2/v3) | ✅  | ✅  | ✅  |
| search_for_variants           | Search for variants by ID, gene, or region                      | ✅  | ✅  | ✅  |
| get_str_info                  | Retrieve short tandem repeat (STR) data and population frequencies| ❌  | ❌  | ✅  |
| get_all_strs                  | Retrieve all STRs in the dataset                                 | ❌  | ❌  | ✅  |
| get_variant_liftover          | Retrieve liftover mapping for a variant between genomes          | ✅  | ❌  | ❌  |
| get_metadata                  | Retrieve gnomAD browser metadata and API version info            | ✅  | ✅  | ✅  |

- ✅ = Supported in this version
- ❌ = Not supported in this version

## Dependencies

- Python >= 3.13
- `aiohttp >= 3.11.18`
- `fastmcp >= 2.2.1`
- `gql >= 3.5.2`
- `httpx >= 0.28.1`
- `mcp[cli] >= 1.6.0`
- `nest-asyncio >= 1.6.0`
- `pytest >= 8.3.5`
- `pytest-asyncio >= 0.26.0`

## Directory Structure

```
.
├── gnomad/              # Main package
│   ├── __init__.py
│   ├── types.py         # Type definitions
│   ├── queries/         # GraphQL query templates
│   │   ├── v2/         # v2.1 specific queries
│   │   ├── v3/         # v3 specific queries
│   │   └── v4/         # v4 specific queries
│   └── schemas/         # Versioned schema files
├── tests/               # Test code and data
│   ├── input/          # Test input data
│   │   ├── analyzed_schemas/  # Analyzed schema data
│   │   ├── schema2query/     # Schema to query conversion
│   │   └── schemas/          # Raw schema files
│   ├── output/         # Test output data
│   │   ├── server/     # Server test outputs
│   │   ├── v2/         # v2.1 test outputs
│   │   ├── v3/         # v3 test outputs
│   │   └── v4/         # v4 test outputs
│   ├── scripts/        # Test utility scripts
│   └── tests/          # Additional test modules
├── server.py           # FastMCP server entrypoint
├── pyproject.toml      # Project metadata
├── README.md           # This file
└── README_tests.md     # Testing documentation
```

## Setup

### Install dependencies

```bash
uv sync
```

### Activate the virtual environment

```bash
. .venv/bin/activate
```

### Test the server

```bash
uv --directory ./ run mcp dev server.py
```

### Add the MCP server to your MCP server list (Claude, Cursor, etc.)

```json
{
    "mcpServers": {
      "gnomad": {
        "command": "uv",
        "args": ["--directory", "where you cloned the repo", "run", "server.py"],
        "env": {}
      }
    }
}
```


### Run tests

Please see [README_tests.md](./README_tests.md)

## Query & API Design

- Uses the **QueryTemplateEngine** pattern to manage version-specific GraphQL query templates.
- Currently, queries are fixed; see (`./gnomad/queries`)
   - The queries were obtained using [schema_fetcher.py](gnomad/schemas/schema_fetcher.py) and [schema_analyzer.py](gnomad/schemas/schema_analyzer.py)
   - [ ] TODO: Dynamic queries
- MCP tool endpoints are documented with detailed parameter and output descriptions.


## License

This MCP server itself is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

This project uses the gnomAD API. Please ensure you cite gnomAD when using this tool or its outputs.

## Acknowledgements

- [gnomAD](https://gnomad.broadinstitute.org/)
- [FastMCP](https://github.com/jlowin/fastmcp)
