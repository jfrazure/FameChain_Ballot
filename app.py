import os
import json
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from web3 import Web3
import matplotlib.pyplot as plt
import pandas as pd
# New Library
from PIL import Image


st.set_page_config(page_title="FameChain Ballot", 
                   page_icon=":moneybags:", 
                   layout="wide",) 

# load env file
load_dotenv()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))

accounts = w3.eth.accounts
account = accounts[0]


# Loading pics to use on the app via Pillow
billie_pic = Image.open("Images/BillieE.png")
elon_pic = Image.open("Images/Elon.png")
tyson_pic = Image.open("Images/MikeTy.png")
paris_pic = Image.open("Images/Parishil.png")
snoop_pic = Image.open("Images/Snoop.png")
famechain_1 = Image.open("Images/famechain1.jpg")
famecoin = Image.open("Images/famechaincoin.jpg")
fame_vote_pic = Image.open("Images/famechainvote.jpg")

# creating a List of the Candidates 
candidates_df = pd.DataFrame([
    {"name": "Mike Tyson", "slogan": "The Champ of Knocking Out Cash"},
    {"name": "Elon Musk", "slogan": "Dogecoin To The Moon!"},   
    {"name": "Snoop Dog", "slogan": "Scooping Up That Bizzy, Making you Dizzy"},
    {"name": "Paris Hilton", "slogan": "<img src='Images/Parishil.png'>"},
    {"name": "Billie Eilish", "slogan": "Bitcoin's Bad Girl"}
])
#################################
##### LOAD_CONTRACT Function #### 
#################################
def load_contract():
    with open("famechain_abi.json") as f:
        contract_abi = json.load(f)
    # set the contract address of the deployed contract
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # getting the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    return contract

# Load the contract
contract = load_contract()


#######################
# Streamlit interface #
#######################
#@st.cache_resource()

# Title message and add 
# def the webapp pages breakdown
def main():
    st.title("The FameChain dApp")

    st.sidebar.title("Navigation Bar")
    page = st.sidebar.radio("Go to", ("Welcome", "Candidates","Vote","Results"))

    if page == "Welcome":
        welcome_page()
    elif page == "Candidates":
        candidates_page()
    elif page == "Vote":
        vote_page()
    elif page == "Results":
        results_page()

# Welcome page        
#def welcome_page():
def welcome_page():
    with st.container():
        st.subheader("Where the stars align in the world of digital assets!")
        st.title('Welcome to the FameChain Ballot!')
        st.write("##")
        st.image(famechain_1)
        st.write("---")
        st.write("##")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write("##")
            st.write('Welcome to FameChain,')  
            st.write( ''' With our exchange buzzing with new assets and celebrity coin traders, we're ready to skyrocket to the top with an electrifying campaign. 
                        Picture this: your favorite celebs endorsing us in flashy online and TV ads, catapulting FameChain to new heights. 
                        But here's the twist: YOU get to choose the face of our campaign through a thrilling blockchain vote, ensuring fairness and excitement for all members. 
                        Get ready to cast your vote and witness history in the making! Here are the nominees:
                        ''')
        with right_column:
            st.image(famecoin)
            
# Page 2 - candidates and slogans. Add pics    
# Display candidates and their slogans
def candidates_page():
    with  st.container():
        #st.write('---')
        st.subheader("Which Crypto Star Shines the Brightest!")
        #st.write('---')
        st.write('##')
        st.markdown("#### Candidates")
        st.write('---')
        # left_column, right_column = st.columns((2,1))
        #with left_column:
            #candidates = contract.functions.getCandidates().call()
        #    for candidate in candidates_df:
        #        st.write(candidates_df["name"], ["slogan"])
        #with right_column:    
        st.markdown("## Mike Tyson")
        st.image(tyson_pic)
        st.markdown('### The Champ of Knocking Out Cash.')
        st.write('---')
        st.write('##')
        st.markdown('## Elon Musk')
        st.image(elon_pic)
        st.markdown('### Dogecoin to the Moon!')
        st.write('---')
        st.write('##')
        st.markdown('## Snoop dog')
        st.image(snoop_pic)
        st.markdown('### Scooping Up That Bizzy, Making you Dizzy')
        st.write('---')
        st.write('##')
        st.markdown('## Paris Hilton')
        st.image(paris_pic)
        st.markdown("### That's Hot")
        st.write('---')
        st.write('##')
        st.markdown('## Billie Ellish')
        st.image(billie_pic)
        st.markdown("### Bitcoin's Bad Girl")
        st.write('---')
        st.write('##')

# Page 3 - Voting Page
def vote_page():
    with st.container():
        st.header('Vote for your Crypto Amassoador')
        selected_candidate = st.selectbox('Choose a candidate', range(1,6))
        # enter wallet address to cast your vote
        wallet_address = st.text_input("Enter your wallet address to cast your vote!")
        # selected_candidate_index = candidates_df[candidates_df["name"]==selected_candidate].index
        # voter_account = st.selectbox("Select Account", options=accounts)
        if st.button('Vote'):
            try:
                if wallet_address:
                    tx_hash = contract.functions.vote(selected_candidate).transact({'from':wallet_address, "gas":1000000})
                    st.write('Vote casted!')
                    st.balloons()
                else:
                    st.error("please enter a valid wallet address")
            except Exception as e:
                st.error(f'Error: {e}')
# Page 4 - results
# End voting
def results_page():
    with st.container():
        st.write("---")
        st.header("Who will it be?")
        st.image(fame_vote_pic)
        st.write("Click below to see the results")
        st.write("##")
        if st.button("Show Results"):
            try:
                results = contract.functions.getResults().call()
                for result in results:
                    st.write(f"Candidate {result[0]} - Votes: {result[3]}")
            except Exception as e:
                st.error(f"Error: {e}")

                # Add total votes for each candidate
        st.write("##")
        st.header("Total Votes for Each Candidate")
        st.write('##')
        if st.button("See all Votes for each Candidate."):
            try:
                votes = contract.functions.getAllVotesForCandidates().call()
                for i, vote_count in enumerate(votes):
                    st.write(f"Candidate {i+1} - Total Votes: {vote_count}")
            except Exception as e:
                st.error(f"Error: {e}")

        # Get total votes for a specific candidate
    candidate_id = st.number_input("Enter Candidate ID:", min_value=1, max_value=6, value=1)
    if st.button("Individual Results"):
        total_votes = contract.functions.getTotalVotesForCandidate(candidate_id).call()
        st.write(f"Total Votes for Candidate {candidate_id}: {total_votes}")      

# call our function
if __name__ == "__main__":
    main()
