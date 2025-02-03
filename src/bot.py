import json
import time
import logging
import threading
import schedule
from src.filters import token_meets_conditions
from src.alerts import send_alert
from src.dexscreener_api import get_latest_tokens, get_token_details

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def detection_job(config):
    """
    Tâche de détection : récupérer les nouveaux tokens et vérifier s'ils remplissent les conditions.
    """
    logger.info("Exécution du job de détection des tokens...")
    latest_tokens = get_latest_tokens(config)
    for token in latest_tokens:
        chain_id = token.get("chainId")
        token_address = token.get("address")
        details = get_token_details(chain_id, token_address, config)
        if details and token_meets_conditions(token, details, config):
            send_alert(token, details, config)
        else:
            logger.info(f"Token {token.get('name', token_address)} ne remplit pas les conditions.")

def update_job(config):
    """
    Tâche de mise à jour : rafraîchir les informations des tokens déjà détectés.
    Vous pouvez implémenter ici la logique d'update (ex. : réinterroger l'API et mettre à jour via Telegram si besoin).
    """
    logger.info("Exécution du job de mise à jour des tokens...")
    # Exemple : vous pouvez stocker les tokens déjà alertés et mettre à jour leur statut
    # Pour simplifier, nous nous contenterons d'un log ici.
    pass

def run_scheduler(config):
    # Planification des tâches selon les intervalles définis dans la config
    detection_interval = config.get("detection_interval_sec", 180)
    update_interval = config.get("update_interval_sec", 300)
    
    schedule.every(detection_interval).seconds.do(detection_job, config)
    schedule.every(update_interval).seconds.do(update_job, config)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    config = load_config()
    logger.info("Démarrage du bot Telegram ZZZ...")
    
    # Exécution du scheduler dans un thread séparé
    scheduler_thread = threading.Thread(target=run_scheduler, args=(config,))
    scheduler_thread.start()
    
    # Vous pouvez ajouter ici d'autres logiques ou un listener pour stopper proprement le bot
