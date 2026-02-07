from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
import os
import json

app = FastAPI(title="Personal Insight Agent API", version="0.1.0")

DAILY_LOG_DIR = "data/daily_logs"
WISHLIST_DIR = "data/wishlists"

os.makedirs(DAILY_LOG_DIR, exist_ok=True)	
os.makedirs(WISHLIST_DIR, exist_ok=True)


class DailyLogEvent(BaseModel):
    category: str
    content: str
    raw_text: str


class WishlistItem(BaseModel):
	id: Optional[str] = None
	item: Optional[str] = None
	harga: Optional[int] = None
	target_bulan: Optional[int] = None
	prioritas: Optional[str] = None
	alasan: Optional[str] = None
	kebiasaan_terkait: Optional[str] = None
	created_at: Optional[datetime] = None


@app.get("/health")
def health():
	return {"status": "ok"}


@app.get("/daily_logs", response_model=List[Dict[str, Any]])
def list_daily_logs():
	items: List[dict] = []
	for fname in sorted(os.listdir(DAILY_LOG_DIR)):
		path = os.path.join(DAILY_LOG_DIR, fname)
		try:
			with open(path, "r", encoding="utf-8") as f:
				obj = json.load(f)
		except Exception:
			with open(path, "r", encoding="utf-8") as f:
				obj = {"id": fname, "content": f.read(), "created_at": datetime.fromtimestamp(os.path.getctime(path)).isoformat()}
		items.append(obj)
	return items


@app.post("/daily_logs")
def append_daily_log(event: DailyLogEvent):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")

    filename = f"{DAILY_LOG_DIR}/{date}.txt"

    entry = f"""
			[TIME: {time}]
			CATEGORY: {event.category}
			CONTENT: {event.content}
			RAW_TEXT: {event.raw_text}
			""".strip() + "\n\n"

    # kalau file belum ada, tulis header dulu
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"TYPE: daily_log\nDATE: {date}\n\n")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(entry)

    return {
        "status": "ok",
        "date": date,
        "category": event.category
    }


@app.get("/wishlists", response_model=List[WishlistItem])
def list_wishlists():
	items: List[dict] = []
	for fname in sorted(os.listdir(WISHLIST_DIR)):
		path = os.path.join(WISHLIST_DIR, fname)
		try:
			with open(path, "r", encoding="utf-8") as f:
				obj = json.load(f)
		except Exception:
			with open(path, "r", encoding="utf-8") as f:
				obj = {"id": fname, "title": f.read(), "created_at": datetime.fromtimestamp(os.path.getctime(path)).isoformat()}
		items.append(obj)
	return items


@app.post("/wishlists", response_model=WishlistItem)
def create_wishlist_item(payload: Dict[str, Any]):
	item = payload.get("item") or payload.get("title")
	if not item:
		raise HTTPException(status_code=422, detail="Field 'item' is required.")
	now = datetime.utcnow().isoformat()
	fname = f"{now.replace(':', '-')}.json"
	payload_dict = {
		"item": item,
		"harga": payload.get("harga"),
		"target_bulan": payload.get("target_bulan") or payload.get("target"),
		"prioritas": payload.get("prioritas"),
		"alasan": payload.get("alasan"),
		"kebiasaan_terkait": payload.get("kebiasaan_terkait") or payload.get("kebiasaan"),
		"created_at": payload.get("created_at") or now,
		"id": payload.get("id") or fname,
	}
	path = os.path.join(WISHLIST_DIR, fname)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(payload_dict, f, default=str)
	return payload_dict


