from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from google.oauth2 import service_account
from google.auth.transport import requests as google_requests
import httpx
from typing import Annotated
from fastapi import Header
from pydantic import BaseModel
from configs import settings


class InputHeader(BaseModel):
    range: str | None = None
    


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


# Authenticate service account.
creds = service_account.Credentials.from_service_account_info( 
    settings.google_credentials.model_dump(),  
    scopes = SCOPES
)

auth_request = google_requests.Request()
creds.refresh(auth_request)
ACCESS_TOKEN = creds.token


video_streaming_router = APIRouter(
    prefix = "/video/stream",
    tags = ["Video Streaming"]
)


@video_streaming_router.get("/{file_id}")
async def stream_video(
    file_id: str, 
    request_header: Annotated[InputHeader, Header()] 
):
    
    print(f"Range Header is {request_header.range}")

    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    
    # Prepare request header to fetch video from Drive.
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    if request_header.range:
        headers["Range"] = request_header.range

    # Initiate the request object and send to the server.
    # Request for a streamable object.
    client = httpx.AsyncClient(timeout = None)
    request = httpx.Request("GET", url, headers = headers)
    response: httpx.Response = await client.send(request, stream = True)  # Sending the request to the Server.

    print(response)
    
    if response.status_code not in (200, 206):
        await response.aclose()
        raise HTTPException(status_code = response.status_code, detail = "Error fetching video from Drive")


    content_length = response.headers.get("Content-Length")
    content_range = response.headers.get("Content-Range")

    async def iterfile():
        try:
            async for chunk in response.aiter_bytes(chunk_size = 1024 * 256):  # 256 KB
                yield chunk
        finally:
            await response.aclose()
            await client.aclose()

    return StreamingResponse(
        iterfile(),
        media_type = "video/mp4",
        status_code = response.status_code,
        headers = {
            "Content-Length": content_length or "",
            "Content-Range": content_range or "",
            "Accept-Ranges": "bytes",
        },
    )


    


        
    
    
    