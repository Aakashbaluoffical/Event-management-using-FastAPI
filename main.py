from fastapi import FastAPI
import uvicorn




app = FastAPI(title='Event Management API',description='FastAPI and PostgreSQL',version='0.1')



@app.get("/")
def about():
     return {'data':{'name': "System API for Enterprise app.","version":"0.1" }}





if __name__ == "__main__":
    print("Start Project")
    # uvicorn.run(app,host="localhost",port='5200')
    