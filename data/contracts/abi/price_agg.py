abi = [
    {
        "name": "AddPricePair",
        "inputs": [
            {"name": "n", "type": "uint256", "indexed": False},
            {"name": "pool", "type": "address", "indexed": False},
            {"name": "is_inverse", "type": "bool", "indexed": False},
        ],
        "anonymous": False,
        "type": "event",
    },
    {
        "name": "RemovePricePair",
        "inputs": [{"name": "n", "type": "uint256", "indexed": False}],
        "anonymous": False,
        "type": "event",
    },
    {
        "name": "MovePricePair",
        "inputs": [
            {"name": "n_from", "type": "uint256", "indexed": False},
            {"name": "n_to", "type": "uint256", "indexed": False},
        ],
        "anonymous": False,
        "type": "event",
    },
    {
        "name": "SetAdmin",
        "inputs": [{"name": "admin", "type": "address", "indexed": False}],
        "anonymous": False,
        "type": "event",
    },
    {
        "stateMutability": "nonpayable",
        "type": "constructor",
        "inputs": [
            {"name": "stablecoin", "type": "address"},
            {"name": "sigma", "type": "uint256"},
            {"name": "admin", "type": "address"},
        ],
        "outputs": [],
    },
    {
        "stateMutability": "nonpayable",
        "type": "function",
        "name": "set_admin",
        "inputs": [{"name": "_admin", "type": "address"}],
        "outputs": [],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "sigma",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "stablecoin",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
    {
        "stateMutability": "nonpayable",
        "type": "function",
        "name": "add_price_pair",
        "inputs": [{"name": "_pool", "type": "address"}],
        "outputs": [],
    },
    {
        "stateMutability": "nonpayable",
        "type": "function",
        "name": "remove_price_pair",
        "inputs": [{"name": "n", "type": "uint256"}],
        "outputs": [],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "price",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "price_pairs",
        "inputs": [{"name": "arg0", "type": "uint256"}],
        "outputs": [
            {
                "name": "",
                "type": "tuple",
                "components": [{"name": "pool", "type": "address"}, {"name": "is_inverse", "type": "bool"}],
            }
        ],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "admin",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
]
