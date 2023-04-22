 question="What is the capital of France?"
 curl -X POST http://localhost:8000/question -H "Content-Type: application/json" -d "{\"question\": \"$question\"}"