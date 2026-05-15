// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LandRegistry {

    // Land structure
    struct Land {

        string ownerName;
        string landId;
        string location;
        uint area;
    }

    // Store all land records
    Land[] public lands;

    // Register new land
    function registerLand(

        string memory _ownerName,
        string memory _landId,
        string memory _location,
        uint _area

    ) public {

        lands.push(

            Land(
                _ownerName,
                _landId,
                _location,
                _area
            )
        );
    }

    // Get total registered lands
    function getTotalLands()

        public
        view
        returns(uint)

    {

        return lands.length;
    }

    // Get land details
    function getLand(uint index)

        public
        view

        returns(

            string memory,
            string memory,
            string memory,
            uint
        )

    {

        Land memory l = lands[index];

        return (

            l.ownerName,
            l.landId,
            l.location,
            l.area
        );
    }
}