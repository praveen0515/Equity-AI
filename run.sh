#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Indian AI Advisor...${NC}"

# Start Backend in the background
echo -e "${GREEN}Starting FastAPI Backend on port 8000...${NC}"
cd backend
# Check if Anthropic key is set
if grep -q "your-api-key-here" .env; then
  echo -e "\n⚠️  WARNING: You have not set your Anthropic API Key in backend/.env."
  echo "The AI analysis will return an error until you provide a valid key."
  echo "You can edit backend/.env to add it."
fi

# Run backend using uvicorn
venv/bin/python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend in the background
echo -e "${GREEN}Starting React Frontend on port 5173...${NC}"
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo -e "\n${BLUE}Both servers are running!${NC}"
echo "Frontend URL: http://localhost:5173"
echo "Backend API:  http://localhost:8000"
echo "Press Ctrl+C to stop both servers."

# Trap Ctrl+C and kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

# Wait for processes
wait
