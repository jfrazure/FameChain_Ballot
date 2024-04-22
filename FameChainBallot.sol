// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;
// make sure to compile in 0.8.0


// Create a smart contract for a decentralized voting system
contract FameChainBallot {
    // Creating a struct to contain all candidates data on the ballot
    struct Candidate {
        uint id;
        string name;
        string slogan;
        uint voteCount;
    }
    // Creator of the FameChainBallot smart contract
    address public owner;

    // Mapping the voters to their address
    mapping(address => bool) public voters;

    // mapping candidates --> For example, candidates[1] would give you the Candidate with an id of 1.
    mapping (uint => Candidate) public candidates;

    // variable of the count number of candidates
    uint public candidatesCount;

    // Variable to store the start of the voting period
    uint public votingStarts;

    // Variable to store the duration of the voting period
    uint public votingDuration = 11 minutes; // Example duration, adjust as needed

    // Creating a end to the voting contract
    uint public votingEnds;

    // Event to track when a vote is cast
    event voteEvent (uint indexed _candidateId);

    // construct the smart contract
    constructor() {
        // The owner of the smart construct
        owner = msg.sender;

        // Set the start of the voting period to the deployment time of the contract
        votingStarts = block.timestamp;
        // Setting the amount of time the election will stay open --> change in DEMO to 11 mins
         votingEnds = votingStarts + votingDuration;  
        // change in DEMO to 11 mins 
        // votingEnds = block.timestamp + 24 hours;
        
        // Initialize candidates
        addCandidate("Mike Tyson", "The Champ of Knocking Out Cash", 0);
        addCandidate("Elon Musk", "Dogecoin To The Moon!", 0);
        addCandidate("Snoop Dog", "Scooping Up That Bizzy, Making you Dizzy", 0);
        addCandidate("Paris Hilton", "That's Hot", 0);
        addCandidate("Billie Eilish", "Bitcoin's Bad Girl", 0);
    }
    // Add the candidates to the constructor
    function addCandidate(string memory _name, string memory _slogan, uint _initialVoteCount) private {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, _slogan, _initialVoteCount);
}
    function vote (uint _candidateId) public {
        // Only allows vote to cast a vote once
        require(!voters[msg.sender], "You have already voted.");

        // Makes sure that the voter can only vote during the open ballot period
        require(block.timestamp <= votingEnds, "Voting has ended.");

        // Checks to ensure the candidate Id is valid
        require(_candidateId > 0 && _candidateId <= candidatesCount);

        // Checks to make sure voter is not putting an incorrect candidateId
        // require(_candidateId < candidatesCount, "Invalid candidate index");
        require(_candidateId <= candidatesCount, "Invalid candidate index");
        voters[msg.sender] = true;

        // Increment the vote count of the candidate
        candidates[_candidateId].voteCount ++;

        // Emit Event
        emit voteEvent(_candidateId);
        
    }
    // Create a function to getResults of the final count of votes after voting period has ended
    function getResults() public view returns (Candidate[] memory) {
        // Only allows users to check winner after voting period ended
        require(block.timestamp > votingEnds, "Voting is still ongoing.");
        // Creating a for loop for getting the results of votes
        Candidate[] memory results = new Candidate[](candidatesCount);
        for (uint i = 1; i <= candidatesCount; i ++) {
            results[i-1] = candidates[i];
        }
        return results;
    }
    
    // Three function to call the results two are active while voting is active. One calls the final winner after voting votingEnds

    // Create a function to get the candidates data
    function getCandidates(uint256 _index) public view returns (string memory, string memory, uint256) {
        // validating that user input a valid candidate id to call
        require(_index < candidatesCount, "Invalid candidate index");
    
        Candidate memory candidate = candidates[_index + 1]; // Adding 1 to the index to match the candidate ID
    
        return (candidate.name, candidate.slogan, candidate.voteCount);
    }

    // get all votes for the cadidates
    function getAllVotesForCandidates() public view returns (uint[] memory) {
        uint[] memory votes = new uint[](candidatesCount);
        for (uint i = 1; i <= candidatesCount; i++) {
            votes[i-1] = candidates[i].voteCount;
        }
        return votes;
    }
    // function to get the votes for only one person at a time via indexes
    function getTotalVotesForCandidate(uint _candidateId) public view returns (uint) {
       require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID");
       return candidates[_candidateId].voteCount;
    }  
}