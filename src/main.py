from area_codes import area_codes
from string import ascii_lowercase as letters
from dvla import vehicle_info
from twitter import twitter_client, tweet

def get_stored_plate_count():
    with open("../last_plate.txt", "r", encoding="utf8") as f:
        return int(f.read())

def inc_stored_plate_count():
    with open("../last_plate.txt", "r", encoding="utf8") as read_f:
        stored_count = read_f.read()

    with open("../last_plate.txt", "w", encoding="utf8") as write_f:
        write_f.write(str(int(stored_count) + 1))

def handle_plate(client, first, second, year, r1, r2, r3):
    plate = first + second + str(year).zfill(2) + ' ' +\
        r1.upper() + r2.upper() + r3.upper()

    response = vehicle_info(plate)
    info = response.json()

    if response.status_code == 404:
        print(f"{get_stored_plate_count()} Invalid: {plate}")
        with open("../invalid.txt", "a+", encoding="utf8") as invalid_f:
            invalid_f.write(f"{plate}\n")
    elif response.status_code == 200:
        print(f"{get_stored_plate_count()} Valid: {plate}")
        with open("../valid.txt", "a+", encoding="utf8") as valid_f:
            valid_f.write(f"{plate}\n")
        tweet(client, info, plate)


def main():
    client = twitter_client()

    current_count = 0
    for idx, first in enumerate(list(area_codes)):
        for second in list(area_codes.values())[idx]:
            for year in range(100):
                # 01 is not a valid date code
                if year == 1:
                    continue
                # r1 => random 1
                for r1 in letters:
                    for r2 in letters:
                        for r3 in letters:
                            current_count += 1
                            if current_count < get_stored_plate_count():
                                print("Skipping plate: " + str(current_count))
                            elif current_count > get_stored_plate_count():
                                handle_plate(
                                    client, first, second, year, r1, r2, r3
                                )
                                inc_stored_plate_count()

if __name__ == "__main__":
    main()
