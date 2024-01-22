import math
import zlib

def calculate_entropy(data: str) -> float:
    """Calculate the information entropy of data.

    Args:
        data: The data to calculate the information entropy.

    Returns:
        The information entropy.
    """
    if not data:
        return 0
    entropy = 0
    stripped_data = data.replace(' ', '')
    for x in range(256):
        p_x = float(stripped_data.count(chr(x))) / len(stripped_data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def calculate_entropy_from_file(file_path: str) -> float:
    """Calculate the information entropy of a file.

    Args:
        file_path: The path of the file to calculate the information entropy.

    Returns:
        The information entropy.

    Throws:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, 'r') as f:
        data = f.read()
    return calculate_entropy(data)

def calculate_compression_ratio(data: bytes) -> float:
    """Calculate the compression ratio of data.

    Args:
        data: The data to calculate the compression ratio.

    Returns:
        The compression ratio.
    """
    if not data:
        return 0
    compressed = zlib.compress(data)
    ratio =  float(len(data)) / float(len(compressed))
    return ratio

def calculate_compression_ratio_from_file(file_path: str) -> float:
    """Calculate the compression ratio of a file.

    Args:
        file_path: The path of the file to calculate the compression ratio.

    Returns:
        The compression ratio.

    Throws:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    return calculate_compression_ratio(data)