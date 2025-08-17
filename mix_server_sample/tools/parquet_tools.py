from server import mcp
from utils.file_reader import read_parquet_summary, get_row_value
@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions.
    """
    return read_parquet_summary(filename)

@mcp.tool()
def get_parquet_value(filename: str) -> str:
    """return the first row of parquet file"""

    return get_row_value(filename)