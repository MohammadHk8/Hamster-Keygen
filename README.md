# Hamster Keygen 🐹

**Hamster Keygen** is a Python-based tool for generating promotional keys for various games by interacting with the GamePromo API. The script automates the process of logging in, emulating gameplay progress, and requesting promo codes for different games. It supports multi-threaded key generation, allowing users to generate multiple keys simultaneously, making it ideal for testing and promotional purposes.

## Features
- **Multi-Threaded Key Generation**: Supports up to 40 parallel key generation tasks using a thread pool for efficient performance.
- **Game Selection**: Users can choose from a variety of pre-configured games with individual API tokens and promo IDs.
- **Configurable Parameters**: Each game has its own delay and number of attempts for event emulation and code generation.
- **Error Handling**: Graceful handling of login failures, rate limits, and failed key generation attempts.
- **API Integration**: Interacts with the GamePromo API for logging in clients, emulating progress, and creating promo codes.

## Games Supported
- ZooPolis
- Chain Cube 2048
- Fluff Crusade
- Train Miner
- MergeAway
- Twerk Race 3D
- Polysphere
- Mow and Trim
- Tile Trio
- Stone Age
- Bouncemasters
- Hide Ball
## Installation
Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/MohammadHk8/hamster-keygen.git
cd hamster-keygen
pip install -r requirements.txt
```

## Usage
1. Run the script.
2. Select a game from the list.
3. Enter the number of keys to generate (1-40).
4. The script will generate the keys and display them once the process is complete.

```bash
python hamster_keygen.py
```

## License
This project is licensed under the MIT License.
