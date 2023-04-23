@echo off

curl -X POST http://192.168.2.103:8090/question -H "Content-Type: application/json" -d "{\"question\": \"What is the capital of France?\"}"