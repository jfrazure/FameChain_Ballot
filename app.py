# load needed libraries
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

# Streamlit web-page config 
st.set_page_config(page_title="FameChain Ballot", 
                   page_icon=":moneybags:", 
                   layout="wide",) 

# load env file
load_dotenv()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))

# create variables to the Ganache accounts for testing
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

# creating a List of the Candidates into a dataframe
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

# defining the function to load the smart contract into this code
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
    st.title("FameChain dApp")
    # creating a navigation bar on the left side of the webapp
    st.sidebar.title("Navigation Bar")
    page = st.sidebar.radio("Go to", ("Welcome", "Candidates","Vote","Results"))
    # defining the pages
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
        st.subheader("Which Crypto Star Shines the Brightest!")
        st.write('##')
        st.markdown("#### Candidates")
        st.write('---')
        # Candidate 1
        st.markdown("## Mike Tyson")
        st.image(tyson_pic)
        st.markdown('### The Champ of Knocking Out Cash.')
        st.write('---')
        st.write('##')
        # Candidate 2
        st.markdown('## Elon Musk')
        st.image(elon_pic)
        st.markdown('### Dogecoin to the Moon!')
        st.write('---')
        st.write('##')
        # Candidate 3
        st.markdown('## Snoop dog')
        st.image(snoop_pic)
        st.markdown('### Scooping Up That Bizzy, Making you Dizzy')
        st.write('---')
        st.write('##')
        # Candidate 4
        st.markdown('## Paris Hilton')
        st.image(paris_pic)
        st.markdown("### That's Hot")
        st.write('---')
        st.write('##')
        # Candidate 5
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
        ### one method to acces the accounts on the Ganache server
        # selected_candidate_index = candidates_df[candidates_df["name"]==selected_candidate].index
        #voter_account = st.selectbox("Select Account", options=accounts)
        if st.button('Vote'):
            try:
                if wallet_address:
                    tx_hash = contract.functions.vote(selected_candidate).transact({'from':wallet_address, "gas":3000000})
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
        # This function is only available when the voting period is ended --> establiished in smart contract / 2 mins for demo
        if st.button("Show Results"):
            try:
                results = contract.functions.getResults().call()
                ### Creating a pie chart that displays after the winner is determined ###
                # Collect vote counts for each candidate
                vote_counts = [result[3] for result in results]
                candidate_names = [candidates_df.loc[i, "name"] for i in range(len(vote_counts))]
                #candidate_names = [f"Candidate {result[0]}" for result in results]

                # Plot a pie chart
                fig, ax = plt.subplots()
                ax.pie(vote_counts, labels=candidate_names, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                # Set background color
                fig.patch.set_facecolor('darkviolet')
                # Display the pie chart
                st.pyplot(fig)
                # Display the winner
                winner_index = vote_counts.index(max(vote_counts))
                winner_name = candidate_names[winner_index]
                st.markdown(f"# The FameChain Crypto Ambassador is... {winner_name}!")
                #for result in results:
                #    st.write(f"Candidate {result[0]} - Votes: {result[3]}")
            except Exception as e:
                st.error(f"Error: {e}")
        st.write("---")
                # Add total votes for each candidate
        st.header("Total Votes for Each Candidate")
        st.write('##')
        # Creating a button to see all votes for all people on the ballot --> functional at all times
        if st.button("See all Votes for each Candidate."):
            try:
                votes = contract.functions.getAllVotesForCandidates().call()
                for i, vote_count in enumerate(votes):
                    st.write(f"Candidate {i+1} - Total Votes: {vote_count}")

               # Create a dynamic pie chart
                vote_counts = [vote_count for vote_count in votes]
                candidate_names = [candidates_df.loc[i, "name"] for i in range(len(votes))]
                dynamic_fig, ax = plt.subplots()
                # Set background color
                dynamic_fig.patch.set_facecolor('darkviolet')
                ax.pie(vote_counts, labels=candidate_names, autopct='%1.1f%%')
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(dynamic_fig)
                

            except Exception as e:
                st.error(f"Error: {e}")
        st.write('---')
        st.write('##')
        # Get total votes for a specific candidate
    candidate_id = st.number_input("Enter Candidate ID:", min_value=1, max_value=6, value=1)
    # create a button to access the results for selected candidate
    if st.button("Individual Results"):
        # calling the getTotalVotesForCandidate from smart contract
        total_votes = contract.functions.getTotalVotesForCandidate(candidate_id).call()
        st.write(f"Total Votes for Candidate {candidate_id}: {total_votes}")      

# call our function
if __name__ == "__main__":
    main()
