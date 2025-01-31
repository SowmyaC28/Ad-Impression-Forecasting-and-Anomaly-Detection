from pathlib import Path

def read_query(query_file_path: str) -> str:
    """
    Reads an SQL query from a file.

    Args:
        query_file_path (str): Path to the query file.

    Returns:
        str: The SQL query as a string.

    Raises:
        FileNotFoundError: If the query file does not exist.
        IOError: If there's an issue reading the file.
    """
    file_path = Path(query_file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_file_path}")

    try:
        return file_path.read_text(encoding="utf-8").strip()
    except IOError as e:
        raise IOError(f"Error reading file {query_file_path}: {e}")
