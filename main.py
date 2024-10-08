import json
import time
import random
import requests
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configuration for different games
game_promo_configs = {
    1: {
        'name': 'ZooPolis',
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'promoId': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'eventsDelay': 21000,
        'attemptsNumber': 22,
    },
    2: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
        'eventsDelay': 20000,
        'attemptsNumber': 15,
    },
    3: {
        'name': 'Fluff Crusade',
        'appToken': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'promoId': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'eventsDelay': 23000,
        'attemptsNumber': 18,
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
        'eventsDelay': 20000,
        'attemptsNumber': 15,
    },
    5: {
        'name': 'MergeAway',
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4',
        'eventsDelay': 20000,
        'attemptsNumber': 15,
    },
    6: {
        'name': 'Twerk Race 3D',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'eventsDelay': 20000,
        'attemptsNumber': 15,
    },
    7: {
        'name': 'Polysphere',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'eventsDelay': 20000,
        'attemptsNumber': 18,
    },
    8: {
        'name': 'Mow and Trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'eventsDelay': 21000,
        'attemptsNumber': 17,
    },
    9: {
        'name': 'Tile Trio',
        'appToken': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'promoId': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'eventsDelay': 40000,
        'attemptsNumber': 22,
    },
    10: {
        'name': 'Stone Age',
        'appToken': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'promoId': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    11: {
        'name': 'Bouncemasters',
        'appToken': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'promoId': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    12: {
        'name': 'Hide Ball',
        'appToken': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'promoId': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'eventsDelay': 40000,
        'attemptsNumber': 30,
    },
    13: {
        'name': 'Pin Out Master',
        'appToken': 'd2378baf-d617-417a-9d99-d685824335f0',
        'promoId': 'd2378baf-d617-417a-9d99-d685824335f0',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    14: {
        'name': 'Count Masters',
        'appToken': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'promoId': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    15: {
        'name': 'Infected Frontier',
        'appToken': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'promoId': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    16: {
        'name': 'Among Water',
        'appToken': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'promoId': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    },
    17: {
        'name': 'Factory World',
        'appToken': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'promoId': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'eventsDelay': 20000,
        'attemptsNumber': 30,
    }
}

session = requests.Session()  # Reuse session for faster requests

current_app_config = None
keygen_active = False
progress_lock = threading.Lock()
global_progress = 0
total_attempts = 0

def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

def login(client_id):
    url = 'https://api.gamepromo.io/promo/login-client'
    headers = {'Content-Type': 'application/json'}
    body = {
        'appToken': current_app_config['appToken'],
        'clientId': client_id,
        'clientOrigin': 'deviceid'
    }
    response = session.post(url, headers=headers, json=body)  # Use session
    data = response.json()
    if response.status_code != 200:
        if data.get('error_code') == "TooManyIpRequest":
            raise Exception('Rate limit hit. Waiting before retrying.')
        else:
            raise Exception(data.get('error_message', 'Failed to log in'))
    return data['clientToken']

def generate_uuid():
    return str(uuid.uuid4())

def emulate_progress(client_token):
    url = 'https://api.gamepromo.io/promo/register-event'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_token}'
    }
    body = {
        'promoId': current_app_config['promoId'],
        'eventId': generate_uuid(),
        'eventOrigin': 'undefined'
    }
    response = session.post(url, headers=headers, json=body)
    data = response.json()
    return data.get('hasCode', False)

def generate_key(client_token):
    url = 'https://api.gamepromo.io/promo/create-code'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_token}'
    }
    body = {'promoId': current_app_config['promoId']}
    response = session.post(url, headers=headers, json=body)
    data = response.json()
    if response.status_code != 200:
        raise Exception(data.get('error_message', 'Failed to generate key'))
    return data['promoCode']

def sleep(ms):
    time.sleep(ms / 1000.0)

def delay_random():
    return random.random() / 3 + 1

def update_total_progress():
    global global_progress
    with progress_lock:
        global_progress += 1
        if global_progress % (total_attempts // 20) == 0:  # Update progress every 5%
            print(f"Overall Progress: {round((global_progress / total_attempts) * 100)}%")

def generate_single_key(i):
    client_id = generate_client_id()
    try:
        client_token = login(client_id)
    except Exception as e:
        print(f"Failed to log in for key {i + 1}: {str(e)}")
        return None

    key = None
    for attempt in range(current_app_config['attemptsNumber']):
        sleep(current_app_config['eventsDelay'] * delay_random())
        has_code = emulate_progress(client_token)
        if has_code:
            key = generate_key(client_token)
            break
        update_total_progress()

    if key:
        print(f"Generated key {i + 1}: {key}")
    else:
        print(f"Failed to generate key {i + 1} after all attempts.")

    return key

def main():
    global keygen_active, current_app_config, total_attempts, global_progress

    # Reset progress trackers
    global_progress = 0

    # Step 1: User selects the game
    print("Select a game:")
    for idx, game in game_promo_configs.items():
        print(f"{idx}: {game['name']}")
    game_choice = int(input("Enter the number corresponding to your choice: "))

    if game_choice not in game_promo_configs:
        print("Invalid choice, exiting.")
        return

    current_app_config = game_promo_configs[game_choice]

    # Step 2: User selects the number of keys to generate (max 40)
    key_count = int(input("Enter the number of keys to generate (1-40): "))
    if key_count < 1 or key_count > 40:
        print("Invalid number of keys, exiting.")
        return

    total_attempts = key_count * current_app_config['attemptsNumber']
    keygen_active = True
    keys = set()

    with ThreadPoolExecutor(max_workers=min(key_count, 40)) as executor:  # Dynamic worker pool size
        futures = [executor.submit(generate_single_key, i) for i in range(key_count)]

        for future in as_completed(futures):
            key = future.result()
            if key:
                keys.add(key)

    keygen_active = False
    print("100% - Key generation complete")

    print("Generated keys:")
    for key in keys:
        print(key)

if __name__ == "__main__":
    main()
