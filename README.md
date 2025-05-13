# Grupowanie playlist dekadami na Spotify

Aplikacja umożliwiająca pobranie playlisty Spotify, zebranie informacji o utworach (w tym roku wydania) oraz utworzenie nowych playlist, pogrupowanych według dekad.

## Opis

### Uwaga, aby skrypt zadziałał, należy być twórcą lub współtwórcą playlisty!

Aplikacja:

- Pobiera dane z playlisty Spotify, w tym informacje o utworach.
- Dla każdego utworu próbuje pobrać rok wydania na podstawie albumu.
- Grupy utworów są tworzone na podstawie dekad (np. 1960s, 1970s, itd.).
- Tworzy nowe playlisty dla każdej dekady, a utwory są przypisywane do odpowiednich playlist.
- Tworzy osobną playlistę dla utworów, które nie mają określonego roku wydania (tzw. "Nieznana dekada").

## Wymagania

Aby uruchomić aplikację, musisz spełnić kilka wymagań:

1. Sklonuj to repozytorium:
```bash
git clone https://github.com/Greyg12/SpotiApi.git
cd SpotiApi
```
2. Zaintaluj Python w wersji 3.6 lub wyższej (jeśli jeszcze go nie masz).
3. Zaintaluj biblioteki:
    - `spotipy`
    - `pandas`
    - `numpy`
    - `python-dotenv`
    
   Możesz je zainstalować za pomocą poniższego polecenia:

   ```bash
   pip install spotipy pandas numpy python-dotenv
   ```
4. 🔧 Zarejestruj aplikację na https://developer.spotify.com/dashboard
   Kliknij "Create an App"

   Ustaw:

   Nazwa (dowolna)

   Opis (np. “Dekadowy analizator playlisty”)

   Dodaj redirect_uri, np.:

   http://localhost:8888/callback
   (To musi być dokładnie taki sam URI jak w .env i kodzie.)

5. Utwórz plik `.env` w katalogu głównym projektu i uzupełnij go danymi ze Spotify:

   Aby aplikacja mogła połączyć się z API Spotify, musisz utworzyć plik `.env` w katalogu głównym aplikacji.  
   Plik powinien zawierać następujące zmienne:

   ```env
   SPOTIPY_CLIENT_ID=twoje_client_id
   SPOTIPY_CLIENT_SECRET=twoje_client_secret
   SPOTIPY_REDIRECT_URI=twoje_redirect_uri
   ```


## Uruchomienie

1. **Zaktualizuj ID playlisty** w pliku `.py`:
   
   Otwórz skrypt i znajdź linię:

   ```python
   playlist_id = '4fsu0ZRfn3EJ4ezICrYAcV'
   ```

   Zaznaczoną część linku, należy użyć w zmiennej playlist_id
   ![Link](images/link.png)
 
2. **Uruchom skrypt**
   
   main.py
3. **Zaloguj się do Spotify:**

   Przy pierwszym uruchomieniu przeglądarka otworzy się z prośbą o zalogowanie i autoryzację aplikacji.
4. **Poczekaj na zakończenie:**

   Przy większych playlistach, wykonanie skryptu może potrwać kilka minut.

   Skrypt pobierze dane, pogrupuje je według dekad i utworzy nowe playlisty w Twoim profilu Spotify. Każda z nich będzie mieć nazwę w formacie:

   Nazwa oryginalnej playlisty - 1990s
   Nazwa oryginalnej playlisty - 2000s
   itd.
   Na końcu zobaczysz komunikat:

   🎉 Proces zakończony pomyślnie!

   ![Success](images/ua.png)


## Działanie aplikacji:

   Pobieranie playlisty – Aplikacja pobiera playlistę na podstawie podanego playlist_id.

   Grupowanie utworów – Utwory w playliście są grupowane według dekad. Jeśli rok utworu nie jest dostępny, zostanie przypisany do grupy "Nieznana dekada".

   Tworzenie playlist – Na podstawie grup dekad tworzone są nowe playlisty, które zawierają odpowiednie utwory.

## Przykład

   Jeśli masz playlistę, która zawiera utwory z różnych lat, aplikacja automatycznie pogrupuje je w następujący sposób:

   ua - 1960s

   ua - 1970s

   ua - 1980s

   itd.

   ua - Nieznana dekada (dla utworów bez roku wydania)

   Każda z tych playlist będzie zawierała odpowiednie utwory, pogrupowane według dekad.

![Result](images/result.png)