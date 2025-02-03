import logging
from telegram import Bot, ParseMode

logger = logging.getLogger(__name__)

def send_alert(token_data, details_data, config):
    """
    Formate et envoie une alerte Telegram pour un token validé.
    """
    try:
        bot_token = config["telegram_token"]
        chat_id = config["chat_id"]
        bot = Bot(token=bot_token)

        message = format_alert_message(token_data, details_data)
        # Vous pouvez envoyer une photo si disponible
        photo_url = token_data.get("photo_url")
        if photo_url:
            bot.send_photo(chat_id=chat_id, photo=photo_url, caption=message, parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
        logger.info(f"Alerte envoyée pour le token {token_data.get('name', 'inconnu')}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'alerte: {e}")

def format_alert_message(token_data, details_data):
    """
    Construit le message d'alerte avec toutes les informations du token.
    """
    # Vous pouvez ajuster le format du message selon vos besoins
    message = f"<b>{token_data.get('name', 'Token')}</b>\n"
    message += f"Supply: {token_data.get('supply')}\n"
    message += f"MarketCap: {token_data.get('marketCap')}$\n"
    message += f"Liquidity: {token_data.get('liquidity')}$\n"
    message += f"Volume: {token_data.get('volume')}$\n"
    message += f"Token Boosted: {'Oui' if token_data.get('token_boosted') else 'Non'}\n"
    message += f"Token Ads: {'Oui' if token_data.get('token_ads') else 'Non'}\n"
    message += f"Dex Paid: {'Oui' if token_data.get('dex_paid') else 'Non'}\n"
    message += f"Pair Created Time: {details_data.get('pairCreatedTime', 'N/A')}\n"

    # Ajoutez d'autres informations pertinentes (réseaux sociaux, etc.)
    social = token_data.get("social", {})
    if social:
        message += "\nRéseaux sociaux:\n"
        for key, url in social.items():
            message += f"- {key.capitalize()}: {url}\n"
    return message
