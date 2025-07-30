import streamlit as st
import hashlib
import pandas as pd
import json
import time
import os

# Blockchain Class
class Block:
    def __init__(self, index, voter_hash, state, district, party, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.voter_hash = voter_hash
        self.state = state
        self.district = district
        self.party = party
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.index}{self.timestamp}{self.voter_hash}{self.state}{self.district}{self.party}{self.previous_hash}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def to_dict(self):
        return self.__dict__

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        # Create the genesis block (first block)
        genesis_block = Block(0, "GENESIS", "None", "None", "None", "0")
        self.chain.append(genesis_block)

    def add_vote(self, voter_id, state, district, party):
        # Ensure the chain has at least one block (the genesis block)
        if len(self.chain) == 0:
            self.create_genesis_block()

        previous_block = self.chain[-1]
        voter_hash = hashlib.sha256(voter_id.encode()).hexdigest()
        new_block = Block(len(self.chain), voter_hash, state, district, party, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def save_chain(self, filename="blockchain.json"):
        with open(filename, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self, filename="blockchain.json"):
        try:
            with open(filename, "r") as f:
                chain_data = json.load(f)
                # Ensure Block objects are created properly from loaded data
                self.chain = []
                for block_data in chain_data:
                    block = Block(
                        block_data['index'],
                        block_data['voter_hash'],
                        block_data['state'],
                        block_data['district'],
                        block_data['party'],
                        block_data['previous_hash']
                    )
                    self.chain.append(block)
        except (FileNotFoundError, json.JSONDecodeError):
            self.create_genesis_block()
        # Ensure the chain has at least one block
        if len(self.chain) == 0:
            self.create_genesis_block()

# Initialize blockchain
blockchain = Blockchain()

# Predefined voting data (with candidate image file names)
voting_data = {
    "Kerala": {
        "Thiruvananthapuram": [
            {"party": "LDF", "image": "Dustin_Henderson.webp"},
            {"party": "UDF", "image": "Eddie_Munson.webp"},
            {"party": "BJP", "image": "Eleven_-_The_Piggyback.webp"}
        ],
        "Ernakulam": [
            {"party": "LDF", "image": "Erica_Sinclair_-_S4.webp"},
            {"party": "UDF", "image": "Jim_Hopper_S2.webp"},
            {"party": "BJP", "image": "Lucas_S4.webp"}
        ]
    },
    "Tamil Nadu": {
        "Chennai": [
            {"party": "DMK", "image": "Max_-_Season_4.webp"},
            {"party": "AIADMK", "image": "Mike_Wheeler_S3.webp"},
            {"party": "BJP", "image": "Nancy_S2_alt.webp"}
        ],
        "Coimbatore": [
            {"party": "DMK", "image": "Steve_-_Season_4.webp"},
            {"party": "AIADMK", "image": "Vecna_S4.webp"},
            {"party": "BJP", "image": "Will_in_California.webp"}
        ]
    }
}

# Sample unique_id to state and district mapping (can be replaced with a real mapping)
unique_id_mapping = {
    "12345": {"state": "Kerala", "district": "Thiruvananthapuram"},
    "67890": {"state": "Kerala", "district": "Ernakulam"},
    "11111": {"state": "Tamil Nadu", "district": "Chennai"},
    "22222": {"state": "Tamil Nadu", "district": "Coimbatore"}
}

# Function to save votes to blockchain
def save_vote(voter_name, unique_id, state, district, party):
    blockchain.add_vote(unique_id, state, district, party)
    blockchain.save_chain()
    print(f"Vote added: {voter_name} voted for {party} in {district}, {state}.")

# Function to get vote counts
def get_vote_counts():
    df = pd.DataFrame([vars(block) for block in blockchain.chain if block.index > 0])
    if df.empty:
        return pd.DataFrame(columns=["State", "District", "Party", "Votes"])
    return df.groupby(["state", "district", "party"]).size().reset_index(name="Votes")

# Streamlit App
st.title("Blockchain Voting System")

menu = st.sidebar.radio("Navigation", ["User Page", "Admin Page"])

if menu == "User Page":
    st.header("Cast Your Vote")
    
    # Get unique ID input
    unique_id = st.text_input("Enter Your Unique ID")

    # If unique_id is entered, suggest state and district
    if unique_id:
        if unique_id in unique_id_mapping:
            state = unique_id_mapping[unique_id]["state"]
            district = unique_id_mapping[unique_id]["district"]
            st.write(f"Suggested State: {state}")
            st.write(f"Suggested District: {district}")
        else:
            st.error("Unique ID not recognized. Please enter a valid ID.")

    # Voting section
    if unique_id and unique_id in unique_id_mapping:
        state = unique_id_mapping[unique_id]["state"]
        district = unique_id_mapping[unique_id]["district"]
        
        candidates = voting_data[state][district]
        party = st.radio(
            "Select Party",
            [candidate["party"] for candidate in candidates],
            format_func=lambda x: x  # Display party names
        )

        # Display image of selected candidate
        selected_candidate = next(candidate for candidate in candidates if candidate["party"] == party)
        candidate_image_path = f"images/{selected_candidate['image']}"
        st.image(candidate_image_path, caption=f"Candidate from {party}", width=200)

        # Button to submit vote
        voter_name = st.text_input("Enter Your Name")
        if st.button("Submit Vote"):
            if voter_name and unique_id:
                save_vote(voter_name, unique_id, state, district, party)
                st.success("Vote Submitted Successfully!")
            else:
                st.error("Please enter both your name and valid unique ID.")

elif menu == "Admin Page":
    st.header("Vote Counts")
    vote_counts = get_vote_counts()
    st.dataframe(vote_counts)
