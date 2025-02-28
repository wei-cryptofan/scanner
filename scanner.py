from mnemonic import Mnemonic
from solders.keypair import Keypair
from solana.rpc.api import Client
from concurrent.futures import ThreadPoolExecutor, as_completed
import base58
import re, random, time

client_1 = Client(
    "https://boldest-burned-bird.solana-mainnet.quiknode.pro/b49db7f5380e0541327c6f97ba1b786dc8d38a81"
)

client_2 = Client(
    "https://lingering-winter-silence.solana-mainnet.quiknode.pro/bdb0af77e38761f3726e6dd446b2f968f9b92eff"
)

clients = [client_1, client_2]

mnemo = Mnemonic("english")


def scanner():
    mnemonic_phrase = mnemo.generate(strength=128)
    seed = mnemo.to_seed(mnemonic_phrase, passphrase="")
    keypair = Keypair.from_seed_and_derivation_path(seed, f"m/44'/501'/0'/0'")
    while True:
        try:
            client = random.choice(clients)
            sol_balance = client.get_balance(keypair.pubkey())
            if not sol_balance:
                time.sleep(5)
                continue
            if sol_balance.value > 0:
                with open("key.txt", "a") as file:
                    file.write(f"{seed}\n")
                return True
            return False
        except Exception as e:
            with open("error.txt", "a") as file:
                file.write(
                    f"{base58.b58encode(bytes(keypair.to_bytes_array())).decode('utf-8')}\n"
                )
            time.sleep(5)


def main():
    while True:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_wallet = {executor.submit(scanner) for _ in range(100)}

            for future in as_completed(future_to_wallet):
                result = future.result()

        with open("status.txt", "a") as file:
            file.write("100 wallets scanned.\n")


if __name__ == "__main__":
    main()
