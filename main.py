from fastapi import FastAPI, HTTPException
from db.supabase import supabase
from postgrest.exceptions import APIError

app = FastAPI()


@app.get("/")
def get_user():
    try:
        res = supabase.table("users").select("*").execute()
        return res.data
    except APIError as e:
        # PostgREST/Supabase ตอบ error กลับมา (เช่น PGRST002 = ต่อ database ไม่ได้)
        # ส่งต่อเป็น 503 พร้อมรายละเอียด แทนที่จะปล่อยเป็น 500 เปล่าๆ
        raise HTTPException(
            status_code=503,
            detail={
                "error": "database_unavailable",
                "code": e.code,
                "message": e.message,
            },
        )
    except Exception as e:
        # error อื่นๆ ที่คาดไม่ถึง (เช่น network/SSL)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": str(e)},
        )
