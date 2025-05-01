"""
Parameter file for gnomAD API tests (for v3.1.2 only)

Supported version:
- v3.1.2 (gnomad_r3)
"""

# Test parameters for v3.1.2 are not implemented

ALL_V3_TEST_PARAMS = [
    # search_for_genes patterns
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_only.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_reference_genome.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_dataset.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_reference_genome_dataset.json"
    },
    # get_variant_info patterns
    {
        "query_name": "variant",
        "variantId": "1-55051215-G-GA",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "get_variant_info_variant_id.json"
    },
    # get_clinvar_variant_info
    {
        "query_name": "clinvar_variant",
        "variant_id": "19-11105588-G-T",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "clinvar_variant.json"
    },
    # search_for_variants
    {
        "query_name": "variant_search",
        "query": "1-55051215-G-GA",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "variant_search.json"
    },
    # get_metadata
    {
        "query_name": "meta",
        "dataset": "gnomad_r3",
        "reference_genome": "GRCh38",
        "_output_file": "meta.json"
    },
] 