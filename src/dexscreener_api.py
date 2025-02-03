import requests
import logging
from src.utils import format_url

logger = logging.getLogger(__name__)

def get_latest_tokens(config):
    """
    Récupère la liste des nouveaux tokens depuis l'API Dexscreener.
    Gère le cas où l'API renvoie directement une liste.
    """
    url = config['dexscreener']['latest_endpoint']
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Si data est une liste, on la retourne directement
        if isinstance(data, list):
            return data
        
        # Sinon, on essaie de récupérer les tokens depuis une clé "tokens"
        return data.get("tokens", [])
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des derniers tokens: {e}")
        return [] 

def get_token_details(chain_id, token_address, config):
    """
    Récupère les détails d'un token via l'API Dexscreener.
    """
    url_template = config['dexscreener']['pair_endpoint']
    url = format_url(url_template, chainId=chain_id, tokenAddress=token_address)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des détails du token: {e}")
        return None
