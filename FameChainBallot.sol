// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

// create a smart contract to vote on the World wide Crypto Ambassador
contract FameChainballot {

    // candidates struct
    struct Candidate {
        string name;
        string slogan;
        uint256 voteCount;
    }
    // Empty list of Candidates to poplulate
    Candidate[] public candidates;
    // owner of this contract
    address owner;
    // Mapping to store the voter's address and whether they have voted
    mapping(address => bool) public voters;
    // Mapping to store the number of tokens assigned to each voter
    mapping(address => uint256) public voterTokens;
    // start and end times
    uint public votingStarts;
    uint public votingEnds;
    uint private _votingDuration;

// cadidates constructor
    constructor(uint _voteDuration) {
        candidates.push(Candidate("Mike Tyson", "The Champ of Knocking Out Cash", 0));
        candidates.push(Candidate("Elon Musk", "Dogecoin To The Moon!", 0));
        candidates.push(Candidate("Snoop Dog", "Scooping Up That Bizzy, Making you Dizzy ", 0));
        candidates.push(Candidate("Paris Hilton", "That's Hot", 0));
        candidates.push(Candidate("Billie Eilish", "Bitcoin's Bad Girl", 0));
    // Set the voting start time as the current block timestamp
        votingStarts = block.timestamp;
        
        // Set the voting end time by adding the duration to the start time
        votingEnds = block.timestamp + (_voteDuration * 1440 minutes); // voteDuration is 1 day
    }
// Register the Voters 
    function registerVoter(address _voter, uint256 _tokens) external {
            require(!voters[_voter], "Voter already registered");
            voters[_voter] = true;
            voterTokens[_voter] = _tokens;
        }

// function to vote
    function vote(uint256 _candidateIndex) public {
        require(voters[msg.sender], "Voter not registered");
        require(_candidateIndex < candidates.length, "Invalid candidate index");
        require(voterTokens[msg.sender] > 0, "Insufficient tokens to vote");
        require(block.timestamp >= votingStarts && block.timestamp <= votingEnds, "Voting is not currently allowed");

        // Decrement the token count of the voter
        voterTokens[msg.sender]--;

        // Increment the vote count of the candidate
        candidates[_candidateIndex].voteCount++;

        // Emit event
        emit VoteCast(msg.sender, _candidateIndex);
    }
// Event to track when a vote is cast
    event VoteCast(address indexed voter, uint256 candidateIndex); 

    // Function to get the total number of candidates
    function getCandidateCount() external view returns (uint256) {
        return candidates.length;
    }

    // Function to get the details of a candidate
    function getCandidate(uint256 _index) external view returns (string memory, string memory, uint256) {
        require(_index < candidates.length, "Invalid candidate index");
        return (candidates[_index].name, candidates[_index].slogan, candidates[_index].voteCount);
    }
    
    // Function to check if voting is currently allowed
    function isVotingAllowed() external view returns (bool) {
        return (block.timestamp >= votingStarts && block.timestamp <= votingEnds);
    }
// calculate the votes
    // Function to get the total votes for a candidate
    function getTotalVotesForCandidate(uint256 _index) external view returns (uint256) {
        require(_index < candidates.length, "Invalid candidate index");
        return candidates[_index].voteCount;
    }
    // get all votes for the cadidates
    function getAllVotesForCadidates() public view returns (Candidate[] memory){
        return candidates;
    }
    // display the remaining time of the open ballot 
    function getTimeRemaining() public view returns (uint256) {
        require(block.timestamp >= votingStarts, "Ballot is not open yet!");
        if  (block.timestamp >= votingEnds) {
            return 0;
        }
        return votingEnds - block.timestamp;
    }

}