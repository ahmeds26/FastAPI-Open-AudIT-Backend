from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from services.open_audit import OpenAuditService
from helpers.authenticate import get_current_active_user
from models.user import User
from server.config import FILE_UPLOAD_DIRECTORY, FILE_MAX_SIZE, FILES_NUMBER_LIMIT
from typing import Annotated, List
from datetime import datetime, timezone
from helpers.file_validator import FileValidator
from models.openaudit import CreateDiscovery, UpdateDiscovery, CreateDevice, UpdateDevice
from pathlib import Path
import shutil
import uuid

UPLOAD_DIR = Path(FILE_UPLOAD_DIRECTORY)
UPLOAD_DIR.mkdir(exist_ok=True)

file_validator = FileValidator(max_size=int(FILE_MAX_SIZE) * 1024 * 1024)

OPENAUDIT_SERVICE = OpenAuditService()
openaudit_router = APIRouter()

@openaudit_router.post("/logon", tags=["Logon"], response_description="Logon", status_code=status.HTTP_200_OK)
async def logon_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.logon("/logon")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@openaudit_router.get("/devices", tags=["Devices"], response_description="Get Devices List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/devices")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
      
@openaudit_router.get("/devices/{device_id}", tags=["Devices"], response_description="Get a Device by ID", status_code=status.HTTP_200_OK)
async def get_client(device_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read(f"/devices/{device_id}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.post("/devices", tags=["Devices"], response_description="Create Device", status_code=status.HTTP_201_CREATED)
async def create_client(current_user: Annotated[User, Depends(get_current_active_user)], device: CreateDevice = Body(...)) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.create("/devices", device)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.patch("/devices/{device_id}", tags=["Devices"], response_description="Update Device", status_code=status.HTTP_200_OK)
async def update_client(current_user: Annotated[User, Depends(get_current_active_user)], device: UpdateDevice = Body(...)) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.update(f"/devices/{device.id}", device)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.delete("/devices/{device_id}", tags=["Devices"], response_description="Delete Device", status_code=status.HTTP_200_OK)
async def delete_client(device_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.delete(f"/devices/{device_id}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/discoveries", tags=["Discoveries"], response_description="Get Discoveries List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/discoveries")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/discoveries/{discovery_id}", tags=["Discoveries"], response_description="Get Discovery Details", status_code=status.HTTP_200_OK)
async def get_client(discovery_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read(f"/discoveries/{discovery_id}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.post("/discoveries", tags=["Discoveries"], response_description="Create Discovery", status_code=status.HTTP_201_CREATED)
async def create_client(current_user: Annotated[User, Depends(get_current_active_user)], discovery: CreateDiscovery = Body(...)) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.create("/discoveries", discovery)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.patch("/discoveries/{discovery.id}", tags=["Discoveries"], response_description="Update Discovery", status_code=status.HTTP_200_OK)
async def update_client(current_user: Annotated[User, Depends(get_current_active_user)], discovery: UpdateDiscovery = Body(...)) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.update(f"/discoveries/{discovery.id}", discovery)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.delete("/discoveries/{discovery_id}", tags=["Discoveries"], response_description="Delete Discovery", status_code=status.HTTP_200_OK)
async def delete_client(discovery_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.delete(f"/discoveries/{discovery_id}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/credentials", tags=["Credentials"], response_description="Get Credentials List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/credentials")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/locations", tags=["Locations"], response_description="Get Locations List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/locations")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/orgs", tags=["Orgs"], response_description="Get Organizations List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/orgs")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@openaudit_router.get("/dashboards", tags=["Dashboards"], response_description="Get Dashboards List", status_code=status.HTTP_200_OK)
async def get_client(current_user: Annotated[User, Depends(get_current_active_user)]) -> JSONResponse:
    try:
        openaudit_response = await OPENAUDIT_SERVICE.read("/dashboards")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(openaudit_response))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@openaudit_router.post("/upload-files", tags=["Files"], response_description="Upload Files", status_code=status.HTTP_201_CREATED)
async def upload_files(current_user: Annotated[User, Depends(get_current_active_user)], files: List[UploadFile] = File(...)) -> JSONResponse:

    if len(files) > int(FILES_NUMBER_LIMIT):
        raise HTTPException(
            status_code=400,
            detail="Too many files. Maximum 10 files allowed."
        )

    results = []

    for file in files:

        validation = await file_validator.validate_file(file)

        if not validation["valid"]:
            results.append({
                "filename": file.filename,
                "success": False,
                "errors": validation["errors"]
            })
            continue
        
        # Create unique filename to prevent conflicts
        file_ext = Path(file.filename).suffix
        unique_filename = f"{Path(file.filename).stem}{"_"}{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            results.append({
                "success": True,
                "original_filename": file.filename,
                "stored_filename": unique_filename,
                "content_type": file.content_type,
                "size": file.size,
                "upload_time": datetime.now(timezone.utc).isoformat(),
                "location": str(file_path)
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "errors": [f"Failed to save: {str(e)}"]
            })
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    uploaded_files_obj = {
        "total_files": len(files),
        "successful": len(successful),
        "failed": len(failed),
        "upload_time": datetime.now(timezone.utc).isoformat(),
        "results": results
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(uploaded_files_obj))


