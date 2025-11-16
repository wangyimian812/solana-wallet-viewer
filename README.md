# solana-wallet-viewer
A simple command-line tool that reads a Solana wallet’s SOL balance and SPL token balances using the Solana RPC API
<br><br>
This tool shows:<br>
- SOL balance
- SPL token mint addresses
- SPL token amounts

This tool does not fetch token names or prices. It only reads the raw on-chain
balance data.

## How to run

1. Install the requests library:

   `pip install requests`

2. Run the script:

    `python solana_wallet_reader.py`

3. Enter your Solana wallet address when asked.
