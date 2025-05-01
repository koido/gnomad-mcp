"""
Parameter file for gnomAD API tests (for v4.1.0 only)

Supported version:
- v4.1.0 (gnomad_r4)
"""

ALL_V4_TEST_PARAMS = [
    # get_gene_info by symbol
    {
        "query_name": "gene",
        "gene_symbol": "PCSK9",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "get_gene_info_by_symbol.json"
    },
    # get_gene_info by id
    {
        "query_name": "gene",
        "gene_id": "ENSG00000139618",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "get_gene_info_by_id.json"
    },
    # search_for_genes patterns
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_only.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_reference_genome.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_dataset.json"
    },
    {
        "query_name": "gene_search",
        "query": "PCSK9",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "search_for_genes_query_reference_genome_dataset.json"
    },
    # get_region_info
    {
        "query_name": "region",
        "chrom": "1",
        "start": 55051000,
        "stop": 55052000,
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "region.json"
    },
    # get_variant_info patterns
    {
        "query_name": "variant",
        "variantId": "1-55051215-G-GA",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "get_variant_info_variant_id.json"
    },
    # get_clinvar_variant_info
    {
        "query_name": "clinvar_variant",
        "variant_id": "19-11105588-G-T",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "clinvar_variant.json"
    },
    # get_mitochondrial_variant_info
    {
        "query_name": "mitochondrial_variant",
        "variant_id": "M-8602-T-C",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "mitochondrial_variant.json"
    },
    # get_structural_variant_info
    {
        "query_name": "structural_variant",
        "variantId": "DEL_CHR19_354EAFA6",
        "dataset": "gnomad_sv_r4",
        "reference_genome": "GRCh38",
        "_output_file": "structural_variant.json"
    },
    # get_copy_number_variant_info
    {
        "query_name": "copy_number_variant",
        "variantId": "18714__DUP",
        "dataset": "gnomad_cnv_r4",
        "reference_genome": "GRCh38",
        "_output_file": "copy_number_variant.json"
    },
    # search_for_variants
    {
        "query_name": "variant_search",
        "query": "1-55051215-G-GA",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "variant_search.json"
    },
    # get_str_info
    {
        "query_name": "short_tandem_repeat",
        "id": "ATXN1",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "short_tandem_repeat.json"
    },
    # get_metadata
    {
        "query_name": "meta",
        "dataset": "gnomad_r4",
        "reference_genome": "GRCh38",
        "_output_file": "meta.json"
    },
] 