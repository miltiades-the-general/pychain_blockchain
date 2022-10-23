# Pychain Ledger

################################################################################
# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

################################################################################
# Step 1:
# Create a Data Class named Record
# Construct the class with a sender and receiver attribute of type string, and amount attribute with type float

@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

################################################################################
# Step 2:
# Modify the Existing Block Data Class to Store Record Data

@dataclass
class Block:
    # Assign a record attribute to the Record class
    record: Record

    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        # Create a function that instantiates a hash using the sha256 algorithm
        # Update the hash with each of the attributes from the Block class
        # Return the hash 
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

################################################################################

# Add an input area where you can get a value for `sender` from the user.
sender_address = st.text_input("Please enter your address")

# Add an input area where you can get a value for `receiver` from the user.
receiver_address = st.text_input("Please enter the address you would like to send to")

# Add an input area where you can get a value for `amount` from the user.
send_amount = st.slider("Please enter the amount you would like to send")

if st.button("Add Block"):
    # Define the prev_block as the most recent block in the chain [-1]
    prev_block = pychain.chain[-1]
    # apply the hash_block() method to the prev_block
    prev_block_hash = prev_block.hash_block()

    # instantiate a new_block that is a Block object
    # define record in the new_block as a Record object with the user input values fulfilling the parameters
    # Define a creator id and the prev_hash as the prev_block_hash
    new_block = Block(
        record=Record(
            sender_address,
            receiver_address,
            send_amount
        ),
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code (continues)

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())

################################################################################
