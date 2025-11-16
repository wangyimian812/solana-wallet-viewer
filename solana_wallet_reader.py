import requests

rpc_url = "https://api.mainnet-beta.solana.com"   #RPC = Remote Procedure Call RPC asks the Solana node, node then replies with real balance. In other words, RPC gets the balance information

def get_solana_balance(wallet_address):

    # The structure is fixed 
    payload = {         # payload = the request message you send to Solana
        "jsonrpc": "2.0",
        "id": 1,
        "method":"getBalance",
        "params":[wallet_address]
    }

    reply = requests.post(rpc_url, json=payload, timeout=10)
    data = reply.json()
    #Lamports = Solana’s smallest unit, like cents for dollars
    lamports = data["result"]["value"]  #  1 SOL = 1000000000 lamports
    solana_amount = lamports / 1000000000
    return solana_amount

def get_token_balances_on_solana_chain(wallet_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,"method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}, # This is not a wallet, it is a Solana Program Library (SPL) ID, which manages all tokens. The ID is fixed 
            {"encoding": "jsonParsed"}
        ]
    }
    reply = requests.post(rpc_url, json=payload, timeout=10) # "json=payload" this is not an assignment. It simply means sending this JSON object (payload) to the Solana RPC server. The json= is a parameter name
    data = reply.json()
    tokens = []

    for item in data["result"]["value"]:  # Each item is one token, the "value" contains each token amount
        info = item["account"]["data"]["parsed"]["info"]
        mint = info["mint"]                       # Mint means token ID, namely the address of this token 
        amount_info = info["tokenAmount"]
        ui_amount = amount_info["uiAmount"]       # Human readable amount converted from the raw machine amount which is not easy to read

# A wallet can have a token account with 0 balance, and don’t print them
        if ui_amount and ui_amount != 0:  #ui_amount checks if the value exists and is not None    # ui_amount != 0 checks if the amount is not zero
            tokens.append((mint, ui_amount))

    return tokens


def main():
    wallet_address = input("Enter your Solana wallet address: ").strip() #strip() removes any extra spaces from the start or end of what the user typed
    if not wallet_address:
        print("No address was given.")
        return 
    
    try:
        solana = get_solana_balance(wallet_address)
        print(f"\nSOL balance: {solana:.6f}")
    except Exception as error:  # This will print actual error message, which is helpful for debugging
        print("Error getting SOL balance", error)
        return
    
    try:
        other_solana_tokens = get_token_balances_on_solana_chain(wallet_address)
    except Exception as error:
        print("Error getting token balances", error)
        return
    
    if not other_solana_tokens:
        print("\nNo SPL tokens found.")
    else:
        print("\nSPL tokens:")
        for item in other_solana_tokens:
            mint = item[0]
            amount = item[1]
            print(f"{mint}: {amount}")

if __name__ == "__main__":
    main()
