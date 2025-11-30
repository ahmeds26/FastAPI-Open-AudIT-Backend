from server.config import OPEN_AUDIT_BASE_URL, OPEN_AUDIT_USERNAME, OPEN_AUDIT_PASSWORD, SYNC_LOOKBACK_DAYS
from helpers.format_body import dict_to_data_binary_string, dict_to_encodedurl_string
import httpx
import uuid

class OpenAuditService:
    def __init__(self):
        self.base_url = OPEN_AUDIT_BASE_URL
        self.credentials = (OPEN_AUDIT_USERNAME, OPEN_AUDIT_PASSWORD)

    async def logon(self, endpoint: str):
        request_headers = {"Accept": "application/json"}
        request_body = {
            "username": OPEN_AUDIT_USERNAME, 
            "password": OPEN_AUDIT_PASSWORD
        }
        request_url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(auth=self.credentials, headers=request_headers, verify=False) as client:
                openaudit_response = await client.post(request_url, data=request_body)
                openaudit_response_cookie = openaudit_response.headers['Set-Cookie'].split(";")[0]
            return {"Cookie": openaudit_response_cookie}
        except:
            openaudit_response.raise_for_status()
        
    async def read(self, endpoint: str):

        request_cookie = await self.logon("/logon")

        request_headers = {
            "Accept": "application/json", 
            "Cookie": request_cookie['Cookie']
        }
        if "http" in endpoint:
            request_url = endpoint
        else:
            request_url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(auth=self.credentials, headers=request_headers, verify=False) as client:
                openaudit_response = await client.get(request_url)
            return {
                "data": openaudit_response.json()["data"], 
                "Cookie": request_cookie['Cookie'], 
                "access_token": openaudit_response.json()['meta']['access_token']
            }
        except:
            openaudit_response.raise_for_status()

    async def create(self, endpoint: str, payload):

        request_access_token = await self.read(endpoint)

        if "devices" in endpoint:

            boundary = str(uuid.uuid4())
            request_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.",
                "Content-Type": f"multipart/form-data; boundary={boundary}", 
                "Cookie": request_access_token['Cookie']
            }
        
            request_body = {
                "input_type": payload.input_type, 
                "upload_file": payload.upload_file, 
                "upload_input": payload.upload_input, 
                "data": {
                    "access_token": request_access_token["access_token"],
                    "attributes": payload.attributes.__dict__
                }
            }

            encoded_request_body = dict_to_data_binary_string(request_body, boundary)
        else:
            request_headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded", 
                "Cookie": request_access_token['Cookie']
            }

            request_body = {
                "data": {
                    "access_token": request_access_token["access_token"],
                    "attributes": payload.__dict__
                }
            }
            
            encoded_request_body = dict_to_encodedurl_string(request_body)
                
        request_url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(auth=self.credentials, headers=request_headers, verify=False, follow_redirects=True) as client:
                if "devices" in endpoint:
                    openaudit_post_response = await client.post(request_url, data=encoded_request_body, follow_redirects=False)
                    #openaudit_response = await client.get(openaudit_post_response.headers['Location'])
                    openaudit_response = await self.read(openaudit_post_response.headers['Location'])
                    return openaudit_response
                else:
                    openaudit_response = await client.post(request_url, data=encoded_request_body)
                    return openaudit_response.json()
        except:
            openaudit_response.raise_for_status()
          
    async def update(self, endpoint:str, payload: dict):

        request_cookie = await self.logon("/logon")

        request_headers = {
            "Accept": "application/json", 
            "Cookie": request_cookie['Cookie']
        }

        request_body = {
            "data": {
                "id": payload.id,
                #"type": "discoveries",
                "attributes": payload.attributes.__dict__
            }
        }

        request_url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(headers=request_headers, verify=False) as client:
                openaudit_response = await client.patch(request_url, json=request_body, headers=request_headers)
            return openaudit_response.json()
        except:
            openaudit_response.raise_for_status()

    async def delete(self, endpoint:str):

        request_cookie = await self.logon("/logon")

        request_headers = {
            "Accept": "application/json", 
            "Cookie": request_cookie['Cookie']
        }

        request_url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(headers=request_headers, verify=False) as client:
                openaudit_response = await client.delete(request_url)
                print(openaudit_response.status_code)
                print(openaudit_response.json())
            return openaudit_response.json()
        except:
            openaudit_response.raise_for_status()
