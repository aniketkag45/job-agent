import os
import time
import html
import logging
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def is_configured() -> bool:
    return bool(BOT_TOKEN and (DEFAULT_CHAT_ID or True))  # BOT_TOKEN enough for per-user

def _escape(text: str) -> str:
    if not text:
        return "N/A"
    return html.escape(str(text), quote=False)

def _build_job_keyboard(apply_link: str) -> Optional[Dict]:
    if not apply_link:
        return None
    return {"inline_keyboard": [[{"text": "🔗 Apply Now", "url": apply_link}]]}

def send_telegram_message(
    message: str,
    chat_id: Optional[str] = None,
    parse_mode: str = "HTML",
    reply_markup: Optional[Dict] = None,
    disable_preview: bool = True,
    retries: int = 3,
) -> bool:
    """
    Production-grade. Backward compat: send_telegram_message("hi") uses env CHAT_ID.
    New: send_telegram_message("hi", chat_id="12345")
    """
    if not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set")
        return False

    target_chat = chat_id or DEFAULT_CHAT_ID
    if not target_chat:
        logger.warning("No chat_id provided and TELEGRAM_CHAT_ID not set")
        return False

    if len(message) > 4096:
        message = message[:4000] + "\n\n...[truncated]"

    payload = {
        "chat_id": target_chat,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_preview,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for attempt in range(1, retries+1):
        try:
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 429:
                retry_after = resp.json().get("parameters", {}).get("retry_after", 2)
                logger.warning(f"Flood control, sleep {retry_after}s attempt {attempt}")
                time.sleep(retry_after)
                continue
            resp.raise_for_status()
            logger.info(f"Telegram sent to {target_chat}")
            time.sleep(0.7)  # rate-limit friendly
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(2*attempt)
            else:
                return False
    return False

def send_job_alert(job: Dict[str, Any], chat_id: Optional[str] = None) -> bool:
    title = _escape(job.get("title"))
    company = _escape(job.get("company"))
    location = _escape(job.get("location"))
    score = job.get("score", 0)
    hybrid = job.get("hybrid_score")
    source = _escape(job.get("source",""))

    text = (
        f"🚀 <b>New Job Match For You!</b>\n\n"
        f"💼 <b>{title}</b>\n"
        f"🏢 {company}\n"
        f"📍 {location}\n"
        f"⭐ Score: <b>{score}</b> | 🌐 {source}\n"
    )
    if hybrid:
        text += f"🤖 AI Match: <b>{hybrid*100:.1f}%</b>\n"

    text += f"\n<i>Matched your resume & preferences</i>"

    keyboard = _build_job_keyboard(job.get("apply_link",""))
    return send_telegram_message(text, chat_id=chat_id, reply_markup=keyboard)

def send_daily_digest(jobs: list, chat_id: Optional[str] = None, header: str = "New Matches For You") -> bool:
    if not jobs:
        return True

    summary = f"📊 <b>{_escape(header)}</b>\n\nFound <b>{len(jobs)} new</b> jobs matching your profile:\n\n"
    for i, job in enumerate(jobs[:5], 1):
        summary += f"{i}. <b>{_escape(job.get('title'))}</b> at {_escape(job.get('company'))} — {job.get('hybrid_score',0)*100:.0f}%\n"
    if len(jobs) > 5:
        summary += f"\n...and {len(jobs)-5} more. Check dashboard for all.\n"
    summary += "\nSending detailed cards 👇"

    if not send_telegram_message(summary, chat_id=chat_id):
        return False

    success = 0
    for job in jobs[:5]:  # Send only top 5 detailed to avoid spam, rest in bell
        if send_job_alert(job, chat_id=chat_id):
            success += 1
    return success > 0