from datetime import datetime

import requests


class DownloadError(Exception):
    """Ogólny błąd pobierania pliku."""


class NotFoundError(DownloadError):
    """Serwer zwrócił kod 404."""


class AccessDeniedError(DownloadError):
    """Serwer zwrócił kod 403."""


def pobierz_plik(url, nazwa_pliku="latest.txt"):
    """Pobiera plik z URL i zapisuje go na dysku."""
    odpowiedz = requests.get(url)

    if odpowiedz.status_code == 404:
        raise NotFoundError(f"Nie znaleziono pliku: {url}")
    if odpowiedz.status_code == 403:
        raise AccessDeniedError(f"Brak dostępu do pliku: {url}")

    with open(nazwa_pliku, "wb") as plik:
        plik.write(odpowiedz.content)

    print(f"Zapisano plik: {nazwa_pliku}")


def log_time(func):
    """Dekorator wypisujący czas przed i po wywołaniu funkcji."""
    def wrapper(*args, **kwargs):
        print(f"Przed wywołaniem: {datetime.now()}")
        result = func(*args, **kwargs)
        print(f"Po wywołaniu: {datetime.now()}")
        return result
    return wrapper

class ETLProcess:
    """ETL na generatorach."""

    def __init__(self, file_name):
        self.file_name = file_name

    def extract(self):
        """Wczytuje plik linijka po linijce."""
        with open(self.file_name, "r") as file:
            for line in file:
                yield line.strip().split(",")

    def transform(self, rows):
        """Liczy sumę, średnią i indeksy brakujących wartości."""
        for row in rows:
            numbers = [float(value) for value in row[1:] if value != "-"]
            missing = [i for i, value in enumerate(row) if value == "-"]
            total = round(sum(numbers), 3)
            mean = round(total / len(numbers), 3)
            yield row[0], total, mean, missing

    @log_time
    def load(self, results):
        """wyniki do dwóch plików CSV."""
        with open("values.csv", "w") as values_file:
            with open("missing_values.csv", "w") as missing_file:
                for number, total, mean, missing in results:
                    missing_text = ",".join([str(i) for i in missing])
                    values_file.write(f"{number},{total},{mean}\n")
                    missing_file.write(f"{number},{missing_text}\n")

    def run(self):
        """Łączy etapy"""
        self.load(self.transform(self.extract()))
        print("Zapisano pliki: values.csv i missing_values.csv")



def main():
    adresy = [
        "https://oleksandr-fedoruk.com/sggw/podyplomowe/file",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/404",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/403",
    ]

    for url in adresy:
        try:
            pobierz_plik(url)
        except DownloadError as blad:
            print(f"Błąd: {blad}")

    etl = ETLProcess("latest.txt")
    etl.load(etl.transform(etl.extract()))
    print("Zapisano pliki: values.csv i missing_values.csv")



if __name__ == "__main__":
    main()