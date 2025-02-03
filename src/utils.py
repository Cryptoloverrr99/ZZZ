def format_url(url_template, **kwargs):
    """
    Remplace les placeholders du template URL par les valeurs fournies.
    Exemple : format_url("https://api.example.com/{param}", param="value")
    """
    return url_template.format(**kwargs)
