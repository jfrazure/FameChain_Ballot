// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FameChainBallot {
    struct Candidate {
        uint id;
        string name;
        string slogan;
        uint voteCount;
    }

    address public owner;
    mapping(address => bool) public voters;
    // Candidate[] public candidates;
    //bool public votingEnded;
    mapping (uint => Candidate) public candidates;
    uint public candidatesCount;

    uint public votingEnds;

    // Event to track when a vote is cast
    //event VoteCast(address indexed voter, uint256 candidateIndex);
    event voteEvent (uint indexed _candidateId);

    constructor() {
        owner = msg.sender;
        votingEnds = block.timestamp + 24 hours; // change in DEMO to 2 mins
        
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
        require(!voters[msg.sender], "You have already voted.");
        require(block.timestamp <= votingEnds, "Voting has ended.");
        require(_candidateId > 0 && _candidateId <= candidatesCount);
        require(_candidateId < candidatesCount, "Invalid candidate index");
        voters[msg.sender] = true;
        // Increment the vote count of the candidate
        candidates[_candidateId].voteCount ++;
        // Emit Event
        emit voteEvent(_candidateId);
        
    }
    
    function getResults() public view returns (Candidate[] memory) {
        require(block.timestamp > votingEnds, "Voting is still ongoing.");
        Candidate[] memory results = new Candidate[](candidatesCount);
        for (uint i = 1; i <= candidatesCount; i ++) {
            results[i-1] = candidates[i];
        }
        return results;
    }
    
    function getCandidates(uint256 _index) public view returns (string memory, string memory, uint256) {
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