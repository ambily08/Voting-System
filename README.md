# Voting-System

 Blockchain Voting System

 Project Overview

This project implements a secure, transparent, and tamper-proof voting system using a custom-built blockchain in Python. It aims to demonstrate how distributed ledger technology can be used to store and verify votes, reducing the risks of fraud or data tampering typically associated with electronic voting systems.

 Features

📦 Lightweight blockchain implementation (stored as JSON).

✅ Vote validation to ensure one vote per user.

🗂️ Real-time block addition to the chain.

🖼️ Image-based candidate representation.

🔐 Cryptographically hashed blocks for immutability.

How It Works

1. Vote Submission: Users cast a vote via a UI (not included here, assumed frontend or command-line).

2. Block Creation: Each vote is wrapped in a block structure with metadata (timestamp, index, previous hash, etc.).

3. Blockchain Integrity: Before being added, the new block undergoes validation including hash verification.

4. Persistence: The entire blockchain is saved to a JSON file (blockchain.json) ensuring data is not lost between sessions.

 File Structure

blockchain-voting-system/

├── app.py               
├── blockchain.json       
├── requirements.txt      
└── images/

Dependencies

Listed in requirements.txt:

* hashlib (standard library) – for SHA-256 hashing

* json (standard library) – for data storage

* datetime (standard library) – for timestamps

This project uses only standard Python libraries, making it lightweight and easy to run.

 Installation

1. Clone the repo:
   
git clone https://github.com/ambily08/Voting-System/edit/main/README.md.git
cd blockchain-voting-system

2. Install dependencies:

pip install -r requirements.txt

3.  Usage

python app.py

