from fastapi import FastAPI
from pydantic import BaseModel
from configs.config import settings
app = FastAPI()

print(settings.supabase_service_role_key)
