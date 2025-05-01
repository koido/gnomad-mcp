#!/usr/bin/env python3
"""
Generate GraphQL queries from analyzed schema field map (query_field_map.json).
Output: <output_dir>/<query_name>.graphql
Also outputs a log file: <output_dir>/schema2query.log
"""
import os
import json
import argparse
from typing import Dict, Any, List

def build_args(args: List[Dict[str, Any]]) -> str:
    if not args:
        return ""
    return "(" + ", ".join(f"${a['name']}: {type_to_gql(a['type'])}" for a in args) + ")"

def build_arg_values(args: List[Dict[str, Any]]) -> str:
    if not args:
        return ""
    return "(" + ", ".join(f"{a['name']}: ${a['name']}" for a in args) + ")"

def type_to_gql(type_info: Dict[str, Any]) -> str:
    # Convert type info dict to GraphQL type string
    kind = type_info.get("kind")
    if kind == "NON_NULL":
        return f"{type_to_gql(type_info.get('ofType'))}!"
    elif kind == "LIST":
        return f"[{type_to_gql(type_info.get('ofType'))}]"
    elif "name" in type_info and type_info["name"]:
        return type_info["name"]
    return kind or "Unknown"

def build_fields(fields: Dict[str, Any], indent: int = 2) -> str:
    lines = []
    pad = " " * indent
    for fname, finfo in fields.items():
        if "subfields" in finfo and finfo["subfields"]:
            sub = build_fields(finfo["subfields"], indent + 2)
            lines.append(f"{pad}{fname} {{\n{sub}\n{pad}}}")
        else:
            lines.append(f"{pad}{fname}")
    return "\n".join(lines)

def generate_query(query_name: str, qinfo: Dict[str, Any]) -> str:
    args = qinfo.get("args", [])
    fields = qinfo.get("fields", {})
    arg_defs = build_args(args)
    arg_vals = build_arg_values(args)
    fields_str = build_fields(fields, indent=4)
    return f"query {query_name}{arg_defs} {{\n    {query_name}{arg_vals} {{\n{fields_str}\n    }}\n}}\n"

def main():
    parser = argparse.ArgumentParser(description="Generate GraphQL queries from analyzed schema field map.")
    parser.add_argument("--input", default="tests/input/analyzed_schemas/query_field_map.json", help="Input query_field_map.json path")
    parser.add_argument("--output-dir", default="tests/input/schema2query", help="Output directory for .graphql and log files")
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output_dir
    log_path = os.path.join(output_dir, "schema2query.log")

    os.makedirs(output_dir, exist_ok=True)

    with open(input_path) as f:
        qmap = json.load(f)
    log_lines = []
    for qname, qinfo in qmap.items():
        gql = generate_query(qname, qinfo)
        out_path = os.path.join(output_dir, f"{qname}.graphql")
        with open(out_path, "w") as outf:
            outf.write(gql)
        log_lines.append(f"Wrote: {out_path}\n{gql}\n{'-'*40}\n")
        print(f"Wrote: {out_path}")
    with open(log_path, "w") as logf:
        logf.writelines(log_lines)
    print(f"Log written to: {log_path}")

if __name__ == "__main__":
    main() 