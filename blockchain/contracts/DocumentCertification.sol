// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract DocumentCertification {
    address public owner;
      
    struct Document {
        string contentHash; 
        string fileHash;  
        uint256 timestamp;  
    }
    
    mapping(string => Document) public certifiedDocuments;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can perform this action");
        _;
    }

    constructor() public {
        owner = msg.sender;
    } 
 
    function documentExists(string memory _contentHash) public view returns (bool) {
        return bytes(certifiedDocuments[_contentHash].contentHash).length != 0;
    }
 
    function saveDocument(string memory _contentHash, string memory _fileHash) public onlyOwner {
        require(!documentExists(_contentHash), "Content hash already exists");
        uint256 timestamp = block.timestamp;
        certifiedDocuments[_contentHash] = Document(_contentHash, _fileHash, timestamp);
    }
}
