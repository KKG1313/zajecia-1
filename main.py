import requests


def pobierz_plik(url, nazwa_pliku="latest.txt"):
    """Pobiera plik z URL i zapisuje go na dysku pod podaną nazwą."""
    odpowiedz = requests.get(url)

    with open(nazwa_pliku, "wb") as plik:
        plik.write(odpowiedz.content)

    print(f"Zapisano plik: {nazwa_pliku}")


def main():
    url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"
    pobierz_plik(url)
    pobierz_plik(url, "dane.csv")

if __name__ == "__main__":
    main()