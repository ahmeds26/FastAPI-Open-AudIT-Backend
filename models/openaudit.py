from pydantic import BaseModel, Field
from pydantic import EmailStr
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

class DiscoveryAttributes(BaseModel):
    name: Optional[str]
    org_id: Optional[int]
    type: Optional[str]
    subnet: Optional[str]

class CreateDiscovery(BaseModel):
    name: str = Field(...)
    org_id: int = Field(...)
    type: str = Field(...)
    subnet: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "My test discovery",
                "org_id": 1,
                "type": "Subnet",
                "subnet": "192.168.1.0/24"
            }
        }

class UpdateDiscovery(BaseModel):
    id: int = Field(...)
    attributes: DiscoveryAttributes
    

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1", 
                "attributes": {
                    "name": "My test discovery",
                    "org_id": 1,
                    "type": "subnet",
                    "subnet": "192.168.1.0/24"
                }
            }
        }

class DeviceAttributes(BaseModel):
    type: str = Field(...)
    name: Optional[str]
    host_name: Optional[str]
    ip: Optional[str]
    netmask: Optional[str]
    subnet: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    serial: Optional[str]
    asset_number: Optional[int]
    owner: Optional[str]
    status: Optional[str]
    environment: Optional[str]
    
    subnet: Optional[str]

class CreateDevice(BaseModel):
    input_type: str = Field(...)
    upload_input: Optional[str]
    upload_file: Optional[bool]
    attributes: DeviceAttributes

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "input_type": "manual_input", 
                "upload_input": "", 
                "upload_file": "false", 
                "attributes": {
                    "type": "computer", 
                    "name": "My test computer",
                    "host_name": "test hostname",
                    "ip": "192.168.1.1",
                    "subnet": "192.168.1.0/24", 
                    "netmask": "192.168.1.0/24", 
                    "manufacturer": "my vendor", 
                    "model": "test", 
                    "serial": "test", 
                    "asset_number":  1, 
                    "owner": "my company", 
                    "status": "production", 
                    "environment": "production"
                }
            }
        }

class UpdateDevice(BaseModel):
    id: int = Field(...)
    attributes: DeviceAttributes
    

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1", 
                "attributes": {
                    "type": "computer", 
                    "name": "My test computer",
                    "host_name": "test hostname",
                    "ip": "192.168.1.1", 
                    "subnet": "192.168.1.0/24", 
                    "netmask": "192.168.1.0/24", 
                    "manufacturer": "my vendor", 
                    "model": "test", 
                    "serial": "test", 
                    "asset_number":  1, 
                    "owner": "my company", 
                    "status": "production", 
                    "environment": "production"

                }
            }
        }
