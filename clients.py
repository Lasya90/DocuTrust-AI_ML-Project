from fastapi import APIRouter, HTTPException
from app.database import clients_collection

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("/")
async def create_client(profile: dict):
    existing = await clients_collection.find_one(
        {"client_id": profile.get("client_id")}
    )

    if existing:
        raise HTTPException(status_code=400, detail="Client already exists.")

    await clients_collection.insert_one(profile)
    return profile


@router.get("/{client_id}")
async def get_client(client_id: str):
    client = await clients_collection.find_one({"client_id": client_id})

    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")

    client["_id"] = str(client["_id"])
    return client