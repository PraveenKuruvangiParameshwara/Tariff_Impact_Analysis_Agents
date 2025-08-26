"""MCP-style server using FastAPI (better for production than Flask).
Endpoints:
- /health
- /run_agent_task -> route a task to a local agent manager
- /ingest -> accept CSV upload and run pipeline ingest
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn, os, io, pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent_core import Agent, AgentManager

app = FastAPI()
manager = AgentManager()
# Register demo agents
manager.register(Agent('DataAgent'))
manager.register(Agent('ReasoningAgent'))

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/run_agent_task')
async def run_agent_task(payload: dict):
    # Very simple: DataAgent sends a message to ReasoningAgent
    data_agent = manager.agents.get('DataAgent')
    if not data_agent:
        raise HTTPException(status_code=500, detail='DataAgent not registered')
    data_agent.inbox.put({'to':'ReasoningAgent','from':'DataAgent','message':payload})
    manager.route_all()
    return JSONResponse({'status':'task_submitted'})

@app.post('/ingest')
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='Only CSV allowed')
    data = await file.read()
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))
    # For demo, make DataAgent send a summary
    summary = df.groupby('product_code')['import_value_usd'].sum().reset_index().to_dict(orient='records')
    manager.agents['DataAgent'].inbox.put({'to':'ReasoningAgent','from':'DataAgent','message':{'type':'tariff_summary','payload':summary}})
    manager.route_all()
    return JSONResponse({'status':'ingested','rows': len(df)})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('MCP_PORT', '8081')))
