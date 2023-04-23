@echo off
set "OPTION_CUDA_USE_GPU=False"
set "OPTION_MODEL_SIMPLE_NAME=stablelm"
uvicorn.exe app:app --port 8090 --host 192.168.2.103 
REM --reload 