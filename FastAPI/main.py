from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from s3_client import S3Client
from config import MINIO_CONFIG

app = FastAPI()

s3_client = S3Client(
    endpoint=MINIO_CONFIG["endpoint"],
    access_key=MINIO_CONFIG["access_key"],
    secret_key=MINIO_CONFIG["secret_key"],
    bucket_name=MINIO_CONFIG["bucket_name"],
)

@app.get("/video/{filename}")
async def stream_video(filename: str, request: Request):
    file_size = s3_client.get_file_size(filename)
    if file_size is None:
        raise HTTPException(status_code=404, detail="File not found")

    range_header = request.headers.get("Range")
    start, end = 0, file_size - 1

    if range_header:
        range_values = range_header.replace("bytes=", "").split("-")
        start = int(range_values[0]) if range_values[0] else 0
        end = int(range_values[1]) if len(range_values) > 1 and range_values[1] else file_size - 1

    file_stream = s3_client.stream_file(filename, start, end)
    if file_stream is None:
        raise HTTPException(status_code=500, detail="Error reading file")

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": "video/mp4",
    }

    return StreamingResponse(file_stream, headers=headers, status_code=206)
