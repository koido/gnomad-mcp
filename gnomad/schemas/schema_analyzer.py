#!/usr/bin/env python
"""
gnomAD GraphQL schema analysis utility.

This script provides tools to analyze the gnomAD API GraphQL schema and extract available fields for each query.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Set


class SchemaAnalyzer:
    """
    Class for analyzing GraphQL schemas.
    """
    
    def __init__(self, schema_path: str):
        """
        Initialize the schema analyzer class.
        
        Args:
            schema_path (str): Path to the schema JSON file
        """
        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.types_map = self._build_types_map()
        
    def _load_schema(self) -> Dict[str, Any]:
        """
        Load the schema JSON file.
        
        Returns:
            Dict[str, Any]: Schema data
        """
        with open(self.schema_path, "r") as f:
            return json.load(f)
    
    def _build_types_map(self) -> Dict[str, Any]:
        """
        Build a mapping from type names to type definitions.
        
        Returns:
            Dict[str, Any]: Dictionary mapping type names to type definitions
        """
        types_map = {}
        for type_def in self.schema["__schema"]["types"]:
            types_map[type_def["name"]] = type_def
        return types_map
    
    def get_query_fields(self) -> List[Dict[str, Any]]:
        """
        Get all query fields from the schema.
        
        Returns:
            List[Dict[str, Any]]: List of query fields
        """
        query_type = None
        for type_def in self.schema["__schema"]["types"]:
            if type_def["name"] == "Query":
                query_type = type_def
                break
        
        if query_type and "fields" in query_type:
            return query_type["fields"]
        return []
    
    def get_query_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a query definition by name.
        
        Args:
            name (str): Query name
            
        Returns:
            Optional[Dict[str, Any]]: Query definition, or None if not found
        """
        for field in self.get_query_fields():
            if field["name"] == name:
                return field
        return None
    
    def get_type_fields(self, type_name: str) -> List[Dict[str, Any]]:
        """
        Get fields for a type by name.
        
        Args:
            type_name (str): Type name
            
        Returns:
            List[Dict[str, Any]]: List of fields
        """
        if type_name in self.types_map and "fields" in self.types_map[type_name]:
            return self.types_map[type_name]["fields"]
        return []
    
    def get_query_return_type(self, query_name: str) -> Optional[str]:
        """
        Get the return type name of a query.
        
        Args:
            query_name (str): Query name
            
        Returns:
            Optional[str]: Return type name, or None if not found
        """
        query = self.get_query_by_name(query_name)
        if not query:
            return None
        
        # Get type info (handle optional, list, non-null)
        type_info = query["type"]
        while "ofType" in type_info and type_info["ofType"]:
            type_info = type_info["ofType"]
        
        return type_info.get("name")
    
    def get_required_fields_for_type(self, type_name: str, visited: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        Recursively get required fields and their type info for a type.
        
        Args:
            type_name (str): Type name
            visited (Set[str], optional): Set of visited types for cycle detection
            
        Returns:
            Dict[str, Any]: Mapping of field names to type info
        """
        if visited is None:
            visited = set()
            
        # Cycle detection: do not revisit types
        if type_name in visited:
            return {}
            
        visited.add(type_name)
        
        fields = {}
        
        # Return empty dict for scalar types
        if type_name in ["String", "Int", "Float", "Boolean", "ID"] or not type_name:
            return fields
            
        # Get type definition
        type_def = self.types_map.get(type_name)
        if not type_def:
            logging.warning(f"Type definition not found: {type_name}")
            return fields
        
        # Check for missing or None fields key
        if "fields" not in type_def or type_def["fields"] is None:
            logging.warning(f"Type {type_name} has no 'fields' key")
            return fields
            
        # Collect field info
        for field in type_def["fields"]:
            field_name = field["name"]
            field_type_info = field["type"]
            
            # Parse type info (handle optional, list, non-null)
            inner_type = self._extract_inner_type(field_type_info)
            
            # Add field info
            fields[field_name] = {
                "type": self._type_to_string(field_type_info),
                "description": field.get("description", ""),
                "args": field.get("args", []),
            }
            
            # Recursively collect subfields for non-scalar types
            if inner_type not in ["String", "Int", "Float", "Boolean", "ID"]:
                subfields = self.get_required_fields_for_type(inner_type, visited)
                if subfields:
                    fields[field_name]["subfields"] = subfields
                    
        return fields
                
    def _extract_inner_type(self, type_info: Dict[str, Any]) -> Optional[str]:
        """
        Extract the inner type name from type info.
        
        Args:
            type_info (Dict[str, Any]): Type info
            
        Returns:
            Optional[str]: Inner type name
        """
        if "name" in type_info and type_info["name"]:
            return type_info["name"]
            
        if "ofType" in type_info and type_info["ofType"]:
            return self._extract_inner_type(type_info["ofType"])
            
        return None
        
    def _type_to_string(self, type_info: Dict[str, Any]) -> str:
        """
        Convert type info to string representation.
        
        Args:
            type_info (Dict[str, Any]): Type info
            
        Returns:
            str: String representation of the type
        """
        if not type_info:
            return "unknown"
        kind = type_info.get("kind")
        if kind == "NON_NULL":
            return f"{self._type_to_string(type_info.get('ofType'))}!"
        elif kind == "LIST":
            return f"[{self._type_to_string(type_info.get('ofType'))}]"
        elif "name" in type_info and type_info["name"]:
            return type_info["name"]
        return kind or "unknown"
        
    def generate_query_field_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate a mapping of all queries and their field info.
        
        Returns:
            Dict[str, Dict[str, Any]]: Mapping of query names to required field info
        """
        query_field_map = {}
        
        for query_field in self.get_query_fields():
            query_name = query_field["name"]
            return_type = self.get_query_return_type(query_name)
            
            if return_type:
                fields = self.get_required_fields_for_type(return_type)
                query_field_map[query_name] = {
                    "return_type": return_type,
                    "description": query_field.get("description", ""),
                    "args": query_field.get("args", []),
                    "fields": fields
                }
                
        return query_field_map
        
    def save_query_field_map(self, output_path: str):
        """
        Save the query field map as a JSON file.
        
        Args:
            output_path (str): Output file path
        """
        query_field_map = self.generate_query_field_map()
        
        with open(output_path, "w") as f:
            json.dump(query_field_map, f, indent=2)
            
        print(f"Query field map saved to: {output_path}")

    def print_query_info(self, query_name: str):
        """
        Print information for a specific query.
        
        Args:
            query_name (str): Query name
        """
        query = self.get_query_by_name(query_name)
        if not query:
            print(f"Query '{query_name}' not found.")
            return
            
        print(f"Query: {query_name}")
        print(f"Description: {query.get('description', 'No description')}")
        
        # Print arguments
        print("\nArguments:")
        for arg in query.get("args", []):
            arg_type = self._type_to_string(arg["type"])
            print(f"  {arg['name']}: {arg_type}")
            if arg.get("description"):
                print(f"    Description: {arg['description']}")
                
        # Return type
        return_type = self.get_query_return_type(query_name)
        print(f"\nReturn type: {return_type}")
        
        # Field info
        if return_type:
            fields = self.get_required_fields_for_type(return_type)
            print("\nFields:")
            self._print_fields(fields, indent=2)
            
    def _print_fields(self, fields: Dict[str, Any], indent: int = 0):
        """
        Recursively print field information.
        
        Args:
            fields (Dict[str, Any]): Field information
            indent (int, optional): Indentation level
        """
        indent_str = " " * indent
        
        for field_name, field_info in fields.items():
            print(f"{indent_str}{field_name}: {field_info['type']}")
            
            if "description" in field_info and field_info["description"]:
                print(f"{indent_str}  Description: {field_info['description']}")
                
            if "args" in field_info and field_info["args"]:
                print(f"{indent_str}  Arguments:")
                for arg in field_info["args"]:
                    arg_type = self._type_to_string(arg["type"])
                    print(f"{indent_str}    {arg['name']}: {arg_type}")
                    
            if "subfields" in field_info:
                print(f"{indent_str}  Subfields:")
                self._print_fields(field_info["subfields"], indent + 4)


def main():
    """
    Main execution function.
    """
    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Set schema path
    schema_path = "tests/input/gnomad_schema.json"
    
    # Ensure output directory exists
    output_dir = "tests/input"
    os.makedirs(output_dir, exist_ok=True)
    
    # Output file path
    output_path = os.path.join(output_dir, "query_field_map.json")
    
    # Run schema analysis
    analyzer = SchemaAnalyzer(schema_path)
    
    # Generate and save query field map
    analyzer.save_query_field_map(output_path)
    
    # Example: print query info
    # analyzer.print_query_info("gene")
    
    print("\nQuery list:")
    for query in analyzer.get_query_fields():
        print(f"- {query['name']}")


if __name__ == "__main__":
    main() 