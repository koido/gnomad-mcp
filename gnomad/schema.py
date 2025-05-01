#!/usr/bin/env python3
"""
Unified CLI for gnomAD schema management: fetch, analyze.
- fetch: Download and save the latest gnomAD GraphQL schema
- analyze: Analyze a schema and output field information
"""

import argparse
import sys
import asyncio
from gnomad.schemas.schema_fetcher import fetch_schema, save_schema
from gnomad.schemas import schema_analyzer

def main():
    parser = argparse.ArgumentParser(description="gnomAD schema utility CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch (latest only)
    fetch_parser = subparsers.add_parser("fetch", help="Fetch and save the latest gnomAD schema")
    fetch_parser.add_argument("--output-dir", default="tests/input", help="Directory to save the schema JSON file (default: tests/input)")

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a gnomAD schema file")
    analyze_parser.add_argument("--schema", required=True, help="Schema file to analyze (JSON)")
    analyze_parser.add_argument("--output", help="Output file for analysis result (JSON)")

    args = parser.parse_args()

    if args.command == "fetch":
        async def run_fetch():
            schema, _ = await fetch_schema()
            if schema:
                save_schema(schema, output_dir=args.output_dir)
                return 0
            else:
                print("Failed to fetch schema", file=sys.stderr)
                return 1
        sys.exit(asyncio.run(run_fetch()))

    elif args.command == "analyze":
        analyzer = schema_analyzer.SchemaAnalyzer(args.schema)
        if args.output:
            analyzer.save_query_field_map(args.output)
        else:
            import pprint
            pprint.pprint(analyzer.generate_query_field_map())

if __name__ == "__main__":
    main() 