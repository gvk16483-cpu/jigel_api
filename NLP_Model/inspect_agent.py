from google.adk.agents import Agent
import inspect

with open("signature.txt", "w") as f:
    try:
        f.write("Model Fields:\n")
        f.write(str(list(Agent.model_fields.keys())))
    except Exception as e:
        f.write(f"Error: {e}")
