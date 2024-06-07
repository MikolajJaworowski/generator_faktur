# Generator faktur

---

### Uruchomienie skryptu

1. Zainstaluj wymagane zależności zdefiniowane w pliku `requirements.txt`
2. Utwórz plik konfiguracyjny o strukturze podanej niżej, w ścieżce z głównym skryptem `./config.json`
```json
{
  "webhook": "", // Opcjonalne
  "save_path": "./faktury",
  "invoices": [
    {
      "seller": {
        "name": "Sprzedający",
        "address": "Testowa 1, 00-200 Warszawa, Polska",
        "nip": "11111111111"
      },
      "buyer": {
        "name": "Kupujący",
        "address": "Testowa 2, 00-120 Warszawa, Polska",
        "nip": "0000000000"
      },
      "items": [
        {
          "name": "Name 1",
          "quantity": 1,
          "unit": "jednostka",
          "net_price": 100.00,
          "vat_rate": 23
        }
      ],
      "issue_place": "Miejsce wystawienia",
      "payment_due_days": 14,
      "payment_method": "Przelew", // Jeżeli wybrano przelew trzeba podać nazwę banku i nr. konta
      "bank_name": "Bank Firmowy",
      "bank_account": "1111111111111111111",
      "gtu_codes": ["GTU_12", "GTU_1"] // Opcjonalne
    }
  ]
}
```
3. Uruchom skrypt `python main.py`

---

### Parametry skryptu
Skrypt przyjmuje parametry:
* -h --help - wyświetlenie pomocy
* -c --config - przekazanie ścieżki do pliku konfiguracyjnego

---

### Założenia skryptu

Skrypt zakłada że jest jedynym bytem wystawiającym faktury. Jest to istotne ze względu na ich numerowanie - przy uruchomieniu skryptu wygenerowane faktury będą zawsze numerowane od 1 (nawet jeżeli w tym miesiącu zostały już wystawione jakieś faktury).

Skrypt zakłada że będzie uruchamiany raz w miesiącu (najlepiej regularnie), sam tworzy strukturę folderów oraz faktury w nich.

Nazewnictwo folderów jest w formacie YYYY-MM
Nazewnictwo faktur jest w formacie YYYY-MM-{nr. faktury}-{nazwa kupującego}.pdf

Faktury mają tylko jeden wygląd, a jedyna możliwa personalizacja odbywa się poprzez przekazanie (lub nie) opcjonalnych danych w konfiguracji.

---

### Zasada działania

1. Skryp odczytuje plik konfiguracyjny podany przez użytkownika, lub z domyślnej ścieżki
2. Następuje walidacja konfiguracji
3. Skrypt tworzy potrzebne foldery (jeżeli nie istnieją)
4. Skrypt mapuje dane potrzebne do wystawienia faktury
5. Skrypt generuje fakturę i zapisuje ją do pliku
6. Kroki 4 i 5 są powtarzane dla każdej faktury zleconej do wystawienia
7. Po wystawieniu wszystkich faktur, jeżeli został podany webhook, skrypt zbiera informacje o wystawionych fakturach i wysyła request POST na podany adres.

---

### Powiadomienia webhook

Skrypt przyjmuje adres url na który ma zostać wysłany request POST z informacją o wygenerowanej fakturze.

Request body zostało zoptymalizowane pod działanie z wybranym botem: [Link do dokumentacji](https://matrix-org.github.io/matrix-hookshot/latest/setup/webhooks.html)
