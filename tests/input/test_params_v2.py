"""
Parameter file for gnomAD API tests (for v2.1.1 only)

Supported versions:
- v2.1.1 (gnomad_r2_1)
"""

ALL_V2_TEST_PARAMS = [
    # get_variant_info
    {
        "query_name": "variant",
        "variantId": "12-112241766-G-A",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "variant.json"
    },
    # search_for_genes
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "search_for_genes_by_symbol.json"
    },
    # get_clinvar_variant_info
    {
        "query_name": "clinvar_variant",
        "variant_id": "12-112241766-G-A",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "clinvar_variant.json"
    },
    # get_structural_variant_info
    {
        "query_name": "structural_variant",
        "variantId": "DEL_19_169804",
        "dataset": "gnomad_sv_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "structural_variant.json"
    },
    # get_variant_liftover patterns
    {
        "query_name": "liftover",
        "source_variant_id": "12-112241766-G-A",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "get_variant_liftover_source_variant_id.json"
    },
    {
        "query_name": "liftover",
        "liftover_variant_id": "12-111803962-G-A",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh38",
        "_output_file": "get_variant_liftover_liftover_variant_id.json"
    },
    # search_for_variants
    {
        "query_name": "variant_search",
        "query": "12-112241766-G-A",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "variant_search.json"
    },
    # get_metadata
    {
        "query_name": "meta",
        "dataset": "gnomad_r2_1",
        "reference_genome": "GRCh37",
        "_output_file": "meta.json"
    },
] 