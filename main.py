from fastapi import FastAPI, Depends,Request 
from storage.database import get_db
from sqlalchemy.orm import Session
from routers import logins,event_activities,event_controls,bulk_insert
from starlette.middleware.base import BaseHTTPMiddleware


import uvicorn
from storage.database import Base, engine
from model import model
from storage import query_data





app = FastAPI(title='Event Management API',description='FastAPI and PostgreSQL',version='0.1')


app.include_router(logins.router,prefix='/api/v1')
app.include_router(event_activities.router,prefix='/api/v1')
app.include_router(event_controls.router,prefix='/api/v1')
app.include_router(bulk_insert.router,prefix='/api/v1')




class UpdateEventStatusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db: Session = next(get_db())  # Get DB session

        try:
            query_data.update_status(db)  # Call the function before request processing
        except Exception as e:
            print("Error updating event status:", e)

        response = await call_next(request)  # Proceed with request processing
        return response



# Add middleware to FastAPI
app.add_middleware(UpdateEventStatusMiddleware)




#automatically creates table and columns
model.Base.metadata.create_all(bind=engine) 

@app.get("/")
def about(db:Session = Depends(get_db)):
     
     return {'data':{'name': "System API for Enterprise app.","version":"0.1" }}





if __name__ == "__main__":
    print("Start Project")
    # uvicorn.run(app,host="localhost",port='5200')
    