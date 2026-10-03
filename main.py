from pyexpat.errors import messages

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
# from starlette.responses import JSONResponse
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

conversation_history = {}  # Dictionary to store conversation history for each session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


class QueryRequest(BaseModel):
    session_id: str
    question: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()


        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png",'wb') as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like {"question": "your text"}
        history = conversation_history.get(query.session_id, [])

        mesmessages = {
        "messages": history + [
            {
                "role": "user",
                "content": query.question
            }
        ]
    
}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output['messages'][-1].content # Last AI response
            conversation_history.setdefault(query.session_id, [])
            conversation_history[query.session_id].append({"role": "user", "contents": query.question})
            conversation_history[query.session_id].append({"role": "assistant", "contents": final_output})
        else:
            final_output = str(output)

        return {'answer':final_output}
    except Exception as e:
        print("Using google model due to error:", e)
        try:
                print(query)
                graph = GraphBuilder(model_provider="google")
                react_app = graph()
        
        
                png_graph = react_app.get_graph().draw_mermaid_png()
                with open("my_graph.png",'wb') as f:
                    f.write(png_graph)
        
                print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
                # Assuming request is a pydantic object like {"question": "your text"}
                history = conversation_history.get(query.session_id, [])
        
                mesmessages = {
                "messages": history + [
                    {
                        "role": "user",
                        "content": query.question
                    }
                ]
            
        }
                output = react_app.invoke(messages)
        
                # If result is dict with messages:
                if isinstance(output, dict) and "messages" in output:
                    final_output = output.content[0].get("text")                   
                    conversation_history.setdefault(query.session_id, [])
                    conversation_history[query.session_id].append({"role": "user", "contents": query.question})
                    conversation_history[query.session_id].append({"role": "assistant", "contents": final_output})
                else:
                    final_output = str(output)
        
                return {'answer':final_output}
        except Exception as e:

            return JSONResponse(status_code=500, content={"error": str(e)})    

