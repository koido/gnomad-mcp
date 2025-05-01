from fastmcp import FastMCP
from typing import List, Optional
from gnomad.query import run_query_with_metadata

mcp = FastMCP("gnomAD MCP Server")

# Gene queries
@mcp.tool()
def get_gene_info(
    gene_id: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    dataset = 'gnomad_r4',
    reference_genome = 'GRCh38'
) -> dict:
    """
    [gnomAD API] Retrieve gene information (v4 only)
    Args:
        gene_id (str, optional): Ensembl gene ID (e.g. ENSG00000139618)
        gene_symbol (str, optional): Gene symbol (e.g. PCSK9)
    Returns:
        dict: gene info
    Note:
        Not supported in v2/v3. Use search_for_genes instead.
    """

    if dataset != 'gnomad_r4':
        raise ValueError("Only v4 is supported for gene info.")
    if reference_genome != 'GRCh38':
        raise ValueError("Only GRCh38 is supported for gene info.")

    if not gene_id and not gene_symbol:
        raise ValueError("Either gene_id or gene_symbol must be provided.")
    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'gene_id': gene_id,
        'gene_symbol': gene_symbol,
    }
    return run_query_with_metadata('gene', variables)

@mcp.tool()
def search_for_genes(
    dataset: str,
    reference_genome: str,
    query: str
) -> dict:
    """
    [gnomAD API] Search for genes (v2/v3/v4)
    Args:
        dataset (str): gnomAD dataset ID (gnomad_r3/gnomad_r2_1)
        reference_genome (str, optional): Reference genome (GRCh37 or GRCh38)
        query (str): Search string
    Returns:
        dict: search results
    """
    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'query': query
    }
    return run_query_with_metadata('gene_search', variables)

# Region query
@mcp.tool()
def get_region_info(
    reference_genome: str,
    chrom: str,
    start: int,
    stop: int,
    dataset = 'gnomad_r4'
) -> dict:
    """
    [gnomAD API] Retrieve region information (v4 only)
    Args:
        reference_genome (str): Reference genome (GRCh38)
        chrom (str): Chromosome
        start (int): Start position. Build must be GRCh38.
        stop (int): End position. Build must be GRCh38. 
    Returns:
        dict: region info
    Note:
        Not supported in v2/v3.
    """

    if dataset != 'gnomad_r4':
        raise ValueError("Only v4 is supported for region info.")
    if reference_genome != 'GRCh38':
        raise ValueError("Only GRCh38 is supported for region info.")

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'chrom': chrom,
        'start': start,
        'stop': stop,
    }
    return run_query_with_metadata('region', variables)

# Variant queries
@mcp.tool()
def get_variant_info(
    dataset: str,
    reference_genome: str,
    variantId: str
) -> dict:
    """
    [gnomAD API] Retrieve variant information (v2/v3/v4)
    Args:
        dataset (str): gnomAD dataset ID (gnomad_r4/gnomad_r3/gnomad_r2_1)
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        variantId (str): Variant ID (e.g. 1-55051215-G-GA)
    Returns:
        dict: variant info
    """

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'variantId': variantId,
    }
    return run_query_with_metadata('variant', variables)

@mcp.tool()
def get_clinvar_variant_info(
    dataset: str,
    reference_genome: str,
    variant_id: str
) -> dict:
    """
    [gnomAD API] Retrieve ClinVar variant info (v2/v3/v4)
    Args:
        dataset (str): gnomAD dataset ID (gnomad_r4/gnomad_r3/gnomad_r2_1)
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        variant_id (str): Variant ID
    Returns:
        dict: ClinVar info
    """

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'variant_id': variant_id,
    }
    return run_query_with_metadata('clinvar_variant', variables)

@mcp.tool()
def get_mitochondrial_variant_info(
    reference_genome: str,
    variant_id: str,
    dataset = 'gnomad_r4'
) -> dict:
    """
    [gnomAD API] Retrieve mitochondrial variant info (v4 only)
    Args:
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        variant_id (str): Mitochondrial variant ID (e.g. M-8602-T-C). Build must be GRCh38.
    Returns:
        dict: mito variant info
    Note:
        Not supported in v2/v3.
    """

    if dataset != 'gnomad_r4':
        raise ValueError("Only v4 is supported for mitochondrial variant info.")
    if reference_genome != 'GRCh38':
        raise ValueError("Only GRCh38 is supported for mitochondrial variant info.")

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'variant_id': variant_id,
    }
    return run_query_with_metadata('mitochondrial_variant', variables)

@mcp.tool()
def get_structural_variant_info(
    dataset: str,
    reference_genome: str,
    variantId: str
) -> dict:
    """
    [gnomAD API] Retrieve structural variant info (v2/v4)
    Args:
        dataset (str): SV dataset ID (gnomad_sv_r4/gnomad_sv_r2_1)
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        variantId (str): Structural variant ID
    Returns:
        dict: SV info
    """

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'variantId': variantId,
        }
    return run_query_with_metadata('structural_variant', variables)

@mcp.tool()
def get_copy_number_variant_info(
    reference_genome: str,
    variantId: str,
    dataset = 'gnomad_cnv_r4'
) -> dict:
    """
    [gnomAD API] Retrieve copy number variant info (v4 only)
    Args:
        reference_genome (str): Reference genome (GRCh38)
        variantId (str): CNV ID (e.g. 18714__DUP)
    Returns:
        dict: CNV info
    Note:
        Not supported in v2/v3.
    """

    if dataset != 'gnomad_cnv_r4':
        raise ValueError("Only v4 is supported for copy number variant info.")
    if reference_genome != 'GRCh38':
        raise ValueError("Only GRCh38 is supported for copy number variant info.")

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'variantId': variantId,
    }
    return run_query_with_metadata('copy_number_variant', variables)

@mcp.tool()
def search_for_variants(
    dataset: str,
    reference_genome: str,
    query: str
) -> dict:
    """
    [gnomAD API] Search for variants (v2/v3/v4)
    Args:
        dataset (str): gnomAD dataset ID (gnomad_r4/gnomad_r3/gnomad_r2_1)
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        query (str): Search string (variant_id)
    Returns:
        dict: search results (variant_id)
    """
    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'query': query,
    }
    return run_query_with_metadata('variant_search', variables)

@mcp.tool()
def get_str_info(
    reference_genome: str,
    id: str,
    dataset = 'gnomad_r4'
) -> dict:
    """
    [gnomAD API] Retrieve STR info (v4 only)
    Args:
        reference_genome (str): Reference genome (GRCh38)
        id (str): STR ID (e.g. ATXN1)
    Returns:
        dict: STR info
    Note:
        Not supported in v2/v3.
    """

    if dataset != 'gnomad_r4':
        raise ValueError("Only v4 is supported for STR info.")

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'id': id,
    }
    return run_query_with_metadata('short_tandem_repeat', variables)

# Other genomic queries
@mcp.tool()
def get_variant_liftover(
    reference_genome: str,
    source_variant_id: Optional[str] = None,
    liftover_variant_id: Optional[str] = None,
    dataset = 'gnomad_r2_1'
) -> dict:
    """
    [gnomAD API] Retrieve liftover info (v2 only)
    Args:
        reference_genome (str): Reference genome (GRCh37 or GRCh38)
        source_variant_id (str, optional): Source variant ID (e.g. 12-112241766-G-A on GRCh37)
        liftover_variant_id (str, optional): Lifted over variant ID (e.g. 12-111803962-G-A on GRCh38)
    Returns:
        dict: liftover info
    Note:
        Not supported in v3/v4.
    """

    if dataset != 'gnomad_r2_1':
        raise ValueError("Only v2 is supported for liftover.")
    
    if source_variant_id and liftover_variant_id:
        raise ValueError("Only one of source_variant_id or liftover_variant_id must be provided.")
    
    # Build check
    if source_variant_id:
        if reference_genome != 'GRCh37':
            raise ValueError("Source variant ID must be on GRCh37.")
    elif liftover_variant_id:
        if reference_genome != 'GRCh38':
            raise ValueError("Lifted over variant ID must be on GRCh38.")
    else:
        raise ValueError("Either source_variant_id or liftover_variant_id must be provided.")

    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
        'source_variant_id': source_variant_id,
        'liftover_variant_id': liftover_variant_id,
    }
    return run_query_with_metadata('liftover', variables)

# Metadata query
@mcp.tool()
def get_metadata(
    dataset: str,
    reference_genome: str
) -> dict:
    """
    [gnomAD API] Retrieve metadata (v2/v3/v4)
    Args:
        dataset (str): gnomAD dataset ID (gnomad_r4/gnomad_r3/gnomad_r2_1)
    Returns:
        dict: metadata
    """
    variables = {
        'dataset': dataset,
        'reference_genome': reference_genome,
    }
    return run_query_with_metadata('meta', variables)

if __name__ == "__main__":
    mcp.run()
