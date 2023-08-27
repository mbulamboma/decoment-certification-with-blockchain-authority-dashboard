// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract DocumentCertification {
    address public owner;
      
    struct Document {
        string contentHash;  
        uint256 timestamp;    
        string owner; 
        string importantInfos;
        string fileUrl;
    }
    
    mapping(string => Document) public certifiedDocuments;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can perform this action");
        _;
    }

    constructor() public {
        owner = msg.sender;
    }

    function certifyDocument(string memory _contentHash, string memory _owner_name, string memory _smallDesc, string memory _fileUrl) public {
        require(bytes(_contentHash).length > 0, "Content hash cannot be empty");
        require(certifiedDocuments[_contentHash].timestamp == 0, "Document is already certified");
        
        Document memory newDocument = Document({
            contentHash: _contentHash,
            timestamp: block.timestamp,
            owner: _owner_name,
            importantInfos: _smallDesc,
            fileUrl: _fileUrl
        });
        
        certifiedDocuments[_contentHash] = newDocument;
    }

    
    function getCertificationInfo(string memory _contentHash) public view returns (
        string owner,
        string importantInfos,
        string fileUrl,

    ) {
        Document memory doc = certifiedDocuments[_contentHash];
        if(doc.timestamp != 0){
          return ("", "", "")
        }
        
        return (doc.owner, doc.importantInfos, doc.fileUrl);
    }
 
}
