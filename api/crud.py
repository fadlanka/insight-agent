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


class DailyLog(BaseModel):
	id: Optional[str] = None
	content: Dict[str, Any]
	created_at: Optional[datetime] = None


class WishlistItem(BaseModel):
	id: Optional[str] = None
	title: str
	notes: Optional[str] = None
	created_at: Optional[datetime] = None


@app.get("/health")
def health():
	return {"status": "ok"}


@app.get("/daily_logs", response_model=List[DailyLog])
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


@app.post("/daily_logs", response_model=DailyLog)
def create_daily_log(payload: Dict[str, Any]):
	now = datetime.utcnow().isoformat()
	fname = f"{now.replace(':', '-')}.json"
	payload_dict: Dict[str, Any] = {"content": payload}
	payload_dict.setdefault("created_at", now)
	payload_dict.setdefault("id", fname)
	path = os.path.join(DAILY_LOG_DIR, fname)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(payload_dict, f, default=str)
	return payload_dict


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
def create_wishlist_item(payload: WishlistItem):
	now = datetime.utcnow().isoformat()
	fname = f"{now.replace(':', '-')}.json"
	payload_dict = payload.dict()
	payload_dict.setdefault("created_at", now)
	payload_dict.setdefault("id", fname)
	path = os.path.join(WISHLIST_DIR, fname)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(payload_dict, f, default=str)
	return payload_dict

