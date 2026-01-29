def read_log_file(content):
    """
    Log içeriğini (string) alır ve satır listesi olarak döndürür.
    """
    if not content:
        return []
    
    if isinstance(content, str):
        return content.splitlines()
    
    return []