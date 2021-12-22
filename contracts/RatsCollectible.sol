// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract RatsCollectible is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 internal keyHash;
    uint256 internal fee;

    enum Size {
        NORMAL,
        SKINNY,
        BIG_BONED,
        NORMAL2,
        SKINNY2,
        BIG_BONED2
    }

    enum Accessory {
        NONE,
        BUCKET,
        CHEF,
        DREADLOCKS,
        THUG,
        SANTA,
        TOP,
        WITCH
    }

    struct BGR {
        uint8 blue;
        uint8 green;
        uint8 red;
    }

    struct Rat {
        Size size;
        Accessory accessory;
        BGR ratPrimary;
        BGR ratSecondary;
        BGR ratTertiary;
        BGR ratEyes;
        BGR background;
        BGR accessoryPrimary;
        BGR accessorySecondary;
    }

    mapping(uint256 => Rat) public tokenIdToRat;
    mapping(bytes32 => address) public requestIdToSender;

    event ratAssigned(uint256 indexed tokenId, Rat rat);
    event requestedCollectible(bytes32 indexed requestId, address requester);

    constructor(
        address _VRFCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_VRFCoordinator, _linkToken)
        ERC721("CryRat", "CRAT")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    // getting multiple random numbers
    function expand(uint256 randomValue, uint256 n)
        public
        pure
        returns (uint256[] memory expandedValues)
    {
        expandedValues = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(randomValue, i)));
        }
        return expandedValues;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        uint256[] memory randomNumbers = expand(randomNumber, 23);
        Rat memory rat = Rat(
            Size(randomNumbers[0] % 6),
            Accessory(randomNumbers[1] % 8),
            BGR(
                uint8(randomNumbers[2] % 256),
                uint8(randomNumbers[3] % 256),
                uint8(randomNumbers[4] % 256)
            ),
            BGR(
                uint8(randomNumbers[5] % 256),
                uint8(randomNumbers[6] % 256),
                uint8(randomNumbers[7] % 256)
            ),
            BGR(
                uint8(randomNumbers[8] % 256),
                uint8(randomNumbers[9] % 256),
                uint8(randomNumbers[10] % 256)
            ),
            BGR(
                uint8(randomNumbers[11] % 256),
                uint8(randomNumbers[12] % 256),
                uint8(randomNumbers[13] % 256)
            ),
            BGR(
                uint8(randomNumbers[14] % 256),
                uint8(randomNumbers[15] % 256),
                uint8(randomNumbers[16] % 256)
            ),
            BGR(
                uint8(randomNumbers[17] % 256),
                uint8(randomNumbers[18] % 256),
                uint8(randomNumbers[19] % 256)
            ),
            BGR(
                uint8(randomNumbers[20] % 256),
                uint8(randomNumbers[21] % 256),
                uint8(randomNumbers[22] % 256)
            )
        );
        uint256 newTokenId = tokenCounter;
        tokenIdToRat[newTokenId] = rat;
        emit ratAssigned(newTokenId, rat);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter++;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor approved!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
