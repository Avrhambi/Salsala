from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from server.controllers.receipt import handle_upload
from server.db.client import get_db_session

router = APIRouter(prefix="/receipt", tags=["Receipt"])


@router.post("/upload")
async def upload_receipt(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
):
    return await handle_upload(file, db)
