# Project Valhalla

*Valhalla* – In Norse mythology, Valhalla, the hall of the slain warriors, was, symbolically,
unbreachable. An invincible fortress, protected by Odin himself, where only the worthy made it
inside. Heimdall kept an eye on all, and all warriors within would wait until judgement day, 
or Ragnarok, when they would go defend the allfather. 

This is the less poetic, more useful version. Valhalla is a Python project designed to 
interact with a local MySQL database. It uses a master password, which is stored as a 
hash, to encrypt and decrypt passwords from a given table. 

SHA-256 is utilized as the Hashing algorithm and 
aes is utilized as the encryption standard of choice.

## Features
- Interacts with local MySQL database
- Stores the master password as a hash (secure)
- Encrypts and decrypts passwords from MySQL table

## Installation
1. Clone the repository
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Set up your MySQL database and configure the connection settings.
2. Run the main script to start interacting with the database:
    ```sh
    python3 main.py
    ```

## Testing
Run the unit tests to ensure everything is working correctly:
```sh
python -m unittest discover tests