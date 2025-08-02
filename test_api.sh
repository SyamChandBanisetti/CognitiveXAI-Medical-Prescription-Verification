#!/bin/bash

echo "🧪 Testing Medical Prescription Verification API..."

# Wait for server to start
sleep 3

echo "📍 Testing root endpoint:"
curl -s http://localhost:8000/ | python3 -m json.tool

echo -e "\n❤️ Testing health check:"
curl -s http://localhost:8000/health | python3 -m json.tool

echo -e "\n💊 Testing text analysis:"
curl -s -X POST "http://localhost:8000/analyze-text" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Patient should take Aspirin 100mg twice daily for heart condition." | python3 -m json.tool

echo -e "\n🔍 Testing drug extraction:"
curl -s -X POST "http://localhost:8000/extract-drug-info" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Prescription: Ibuprofen 400mg three times daily, Amoxicillin 250mg twice daily" | python3 -m json.tool

echo -e "\n📚 Opening API documentation..."
"$BROWSER" "http://localhost:8000/docs" &

echo -e "\n✅ API is running at: http://localhost:8000"
echo "📖 Documentation at: http://localhost:8000/docs"
echo "🩺 Health check at: http://localhost:8000/health"
