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


if __name__ == "__main__":
    main()