# Minimal JSON API

A lightweight, two-endpoint backend server built entirely with the native Node.js http module. This project demonstrates the core request-response loop without relying on external frameworks like Express.

## Endpoints

1. Hello Route
URL: /hello
Method: GET
Response:

JSON

{
  "message": "Hello, world!"
}

2. Status Route
URL: /status
Method: GET
Response:

JSON

{
  "status": "online",
  "timestamp": "2026-07-10T17:25:12.920Z"
}
How to Run Locally
Ensure Node.js is installed.
Clone this repository and open the folder in your terminal.
Start the server:

Bash

node server.js
The server will listen on http://localhost:3000.
Testing
You can test the endpoints in your browser by navigating to http://localhost:3000/hello, or via the command line.
For Windows PowerShell users:
Use curl.exe or irm to get a clean JSON response without triggering PowerShell's HTML parsing warnings:

PowerShell

curl.exe http://localhost:3000/status