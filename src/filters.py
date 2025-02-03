import logging

logger = logging.getLogger(__name__)

def token_meets_conditions(token_data, details_data, config):
    """
    Applique les règles de filtrage sur les données du token.
    
    Les règles :
      - Supply maximum
      - MarketCap minimum
      - Liquidity minimum
      - Liquidity locked/burned doit être 99 ou 100%
      - Top 10 holders : max 40%
      - Marker minimum
      - Holders minimum
      - Volume minimum
      - Présence des réseaux sociaux requis (twitter et website)
      - Etc.
    
    Les indicateurs dex paid, token boosted, token ads seront renvoyés sous forme de booléens.
    """
    filters = config['filters']
    try:
        # Exemple d'extraction de données (les clés réelles dépendent de la réponse API)
        supply = token_data.get("supply", 0)
        marketcap = token_data.get("marketCap", 0)
        liquidity = token_data.get("liquidity", 0)
        locked_percent = token_data.get("liquidityLockedPercent", 0)
        top10_holder = token_data.get("top10HolderPercent", 0)
        marker = token_data.get("marker", 0)
        holders = token_data.get("holders", 0)
        volume = token_data.get("volume", 0)
        
        social = token_data.get("social", {})

        if supply > filters["supply_max"]:
            return False
        if marketcap < filters["marketcap_min"]:
            return False
        if liquidity < filters["liquidity_min"]:
            return False
        if locked_percent not in filters["liquidity_locked_percent"]:
            return False
        if top10_holder > filters["top10_holder_max"]:
            return False
        if marker < filters["marker_min"]:
            return False
        if holders < filters["holders_min"]:
            return False
        if volume < filters["volume_min"]:
            return False

        # Vérification des réseaux sociaux requis
        for soc in filters.get("social", {}).get("required", []):
            if soc not in social or not social[soc]:
                return False

        # Récupérer les indicateurs spécifiques à afficher (dex paid, token boosted, token ads)
        # Ici nous supposons que ces informations sont disponibles dans details_data
        token_boosted = details_data.get("tokenBoosted", False)
        token_ads = details_data.get("tokenAds", False)
        dex_paid = details_data.get("dexPaid", False)

        # Vous pouvez ajouter ces infos au token_data pour l'envoi de l'alerte
        token_data["token_boosted"] = token_boosted
        token_data["token_ads"] = token_ads
        token_data["dex_paid"] = dex_paid

        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'application des filtres: {e}")
        return False
