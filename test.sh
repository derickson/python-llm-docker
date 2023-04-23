 echo "DAVEPC STABLELM"
 question="What is the capital of France?"
 curl -X POST http://davepc:8090/question -H "Content-Type: application/json" -d "{\"question\": \"$question\"}"

echo "\n"
echo "NUC FLAN"
curl -X POST http://nuc:8090/question -H "Content-Type: application/json" -d "{\"question\": \"$question\"}"