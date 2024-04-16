import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# load env file
load_dotenv("SAMPLE.env")

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#################################
##### LOAD_CONTRACT Function #### 
#################################
def load_contract():
    with open("FameChain_abi.json") as f:
        contract_abi = json.load(f)
    # set the contract address of the deployed contract
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # getting the contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    return contract

# Load the contract
contract = load_contract()

# Define a function to load candidate data
def load_candidates():
    # This should be replaced with your method of loading candidate data
    # For example, it could be loaded from a JSON file or a database
    return [
        {"name": "Mike Tyson", "slogan": "The Champ of knocking out Cash!", "voteCount": 0, "image": "<path_to_image>"},
        {"name": "Elon Musk", "slogan": "DogeCoin to the Mooon!", "voteCount": 0, "image": "path_to_bob_image"},
        {"name": "Snoop Dog", "slogan": "Scooping Up That Bizzy, Making you Dizzy!", "voteCount": 0, "image": "path_to_bob_image"},
        {"name": "Paris Hilton", "slogan": "Thats Hot...", "voteCount": 0, "image": "path_to_bob_image"},
        {"name": "Billie Ellish", "slogan": "Bitcoin's Bad Girl.", "voteCount": 0, "image": "path_to_bob_image"},
        # Add more candidates as needed
    ]

candidates = load_candidates()

# Define pages as functions
def welcome_page():
    st.title("Welcome to the Crypto Ambassador Election")
    st.write("This is a decentralized application (DApp) that allows you to vote for your favorite crypto ambassador candidate using Ethereum blockchain technology.")

def voter_registration_page():
    st.title("Voter Registration")
    voter_address = st.text_input("Enter your Ethereum address:")
    return voter_address

def voting_page(voter_address):
    st.title("Crypto Ambassador Election")
    
    # Display candidate details with slogans and images
    for i, candidate in enumerate(candidates):
        st.image(candidate["image"], caption=candidate["name"])
        st.write(f"**Candidate #{i+1}**: {candidate['name']}")
        st.write(f"Slogan: {candidate['slogan']}")
        st.write(f"Vote count: {candidate['voteCount']}")
        if st.button(f"Vote for {candidate['name']}", key=f"vote_{i}"):
            # Call the vote function in the smart contract
            tx_hash = contract.functions.vote(i).transact({
                "from": voter_address
            })
            st.write("Vote successfully cast for", candidate['name'])
            st.write("Transaction hash:", tx_hash.hex())
        st.write("---")

def results_page():
    st.title("Election Results")
    
    # Fetch vote counts for each candidate
    vote_counts = [candidate['voteCount'] for candidate in candidates]
    names = [candidate['name'] for candidate in candidates]
    
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(vote_counts, labels=names, autopct='%1.1f%%')
    st.write("Vote Distribution:")
    st.pyplot(fig)

# Main app logic
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "Register", "Vote", "Results"])
    
    if page == "Welcome":
        welcome_page()
    elif page == "Register":
        voter_address = voter_registration_page()
        if voter_address:
            st.sidebar.success("Registration successful!")
            st.sidebar.button("Go to Voting Page")
    elif page == "Vote":
        voter_address = st.sidebar.text_input("Enter your Ethereum address to vote:")
        if voter_address:
            voting_page(voter_address)
    elif page == "Results":
        results_page()

if __name__ == "__main__":
    main()
