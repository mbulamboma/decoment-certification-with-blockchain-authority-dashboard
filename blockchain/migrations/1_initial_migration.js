var DocumentCertification = artifacts.require("./../contracts/DocumentCertification.sol");

module.exports = function(deployer) {
  deployer.deploy(DocumentCertification);
};