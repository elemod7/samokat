import csv
import logging
import phonenumbers
from datetime import datetime

def save_to_csv(user_id, name, phone_number, message, file_path='user_requests.csv'):
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, name, phone_number, message])
    except Exception as e:
        logging.error(f"Ошибка при записи в CSV: {e}")

def normalize_phone_number(phone: str) -> str:
    try:
        parsed_number = phonenumbers.parse(phone, "RU")
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None

def read_user_ids(file_path='user_ids.csv'):
    user_ids = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    user_ids.append(int(row[0])) 
                except ValueError:
                    logging.warning(f"Неверный ID пользователя: {row[0]}")
    except FileNotFoundError:
        logging.warning(f"Файл {file_path} не найден.")
    return user_ids

def is_male_name(name: str) -> bool:
    name = name.strip().lower()
    female_endings = ("а", "я", "ия")
    return not any(name.endswith(ending) for ending in female_endings)
