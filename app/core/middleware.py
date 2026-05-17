import time
from fastapi import Request

async def log_request_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"{request.method} "
        f"{request.url.path} "
        f"completed in "
        
        f"{process_time:.4f}s "
        f"with status "
        f"{response.status_code}"
    )
    return response