# 🕮 Projekat 2 — Mašina za pretraživanje PDF dokumenta (search engine)

Ovaj projekat implementira konzolnu mašinu za pretraživanje sadržaja jednog PDF dokumenta. Program pri pokretanju parsira stranice dokumenta (ili učitava već parsiran `txt/json` ulaz), gradi podatkovne strukture za efikasno pretraživanje (trie, invertovani indeks, graf stranica) i omogućava korisniku unos naprednih tekstualnih upita sa rangiranjem rezultata.

Glavni cilj: omogućiti brzo i relevantno pretraživanje knjige "Data Structures and Algorithms in Python" (koristi se kao test fajl), uz konzolni meni, isticanje pojmova u kontekstu i serijalizaciju struktura radi ubrzanja narednih pokretanja.

**Brzi pregled**
- **Naziv projekta:** `Projekat2` — pretraga PDF-a
- **Glavni fajl za pokretanje:** `main.py`
- **Ulazni podaci:** PDF fajl (preporučeno) ili već parsirani `txt/json` (`parsed_text.json`)
- **Glavne komponente:** `parsing_pdf.py`, `Trie.py`, `trie_serialization.py`, `Graph.py`, `graph_serialization.py`, `search.py`, `save_and_highlight_results.py`

**Funkcionalnosti**
- **Parsiranje PDF-a:** Ekstrakcija teksta sa svake stranice (modul `parsing_pdf.py`). Ako ne želite PDF parsiranje, možete koristiti već parsiran fajl `parsed_text.json`.
- **Trie:** Struktura za efikasno pretraživanje reči po stranicama (`Trie.py`, `trie_serialization.py`).
- **Graf stranica:** Reprezentacija veza između stranica na osnovu referenci u tekstu (npr. "See page 136") u `Graph.py`.
- **Rangiranje rezultata:** Rang se formira na osnovu broja pojavljivanja upitnih reči na stranici, pojavljivanja reči na povezanim stranicama i broja in-linkova (sve u `search.py`).
- **Konzolni meni:** Interaktivni meni za unos upita, paginaciju rezultata i dodatne opcije.
- **Serijalizacija:** Sačuvane strukture mogu se učitati narednim pokretanjima radi ubrzanja (`trie_serialization.py`, `graph_serialization.py`).
- **Isticanje (highlight):** Opcija za generisanje PDF stranica sa označenim ključnim rečima (`save_and_highlight_results.py`).

**Podržane opcije pretrage**
- Jedna ili više reči razdvojenih razmakom (rangira se po učestalosti i prisustvu svih reči).
- Logički operatori: `AND`, `OR`, `NOT` (kombinovanje u izrazima).
- Fraze u navodnicima ("..."), npr. `"binary search"` — traži tačnu sekvencu reči.
- Autocomplete i wildcard podrška (npr. `fun*` predlozi autocomplete).

**Primeri upita**
- `python AND sequence`
- `dictionary NOT list`
- `"binary search"`
- `fun*` (autocomplete / predlozi)

**Kako pokrenuti (Windows / PowerShell)**
1. (Preporuka) Kreirajte virtuelno okruženje i instalirajte zavisnosti ako koristite biblioteke za PDF:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Pokrenite program i pratite konzolni meni:

```powershell
python main.py
```

Napomena: ako nemate `requirements.txt`, za PDF parsing preporučujemo `pdfminer.six` ili `PyPDF2`. Takođe, za obojeni ispis u konzoli može se koristiti `termcolor` ili `colorama`.

**Struktura repozitorijuma**
- `main.py` — ulazna tačka i konzolni meni
- `parsing_pdf.py` — parsiranje PDF dokumenata u tekst-po-stranici
- `Trie.py` — implementacija trie strukture
- `trie_serialization.py` — serijalizacija / deserijalizacija trie-a
- `Graph.py` — reprezentacija grafa stranica i pomoćne metode
- `graph_serialization.py` — serijalizacija / deserijalizacija grafa
- `search.py` — logika upita, rangiranje i formiranje rezultata
- `save_and_highlight_results.py` — generisanje PDF-a sa označenim pojmovima
- `parsed_text.json` — primer već parsiranog sadržaja (opciono)
- `rezultati/` — folder za snimljene rezultate i generisane PDF-ove

**Ocenjivanje (kako projekat zadovoljava kriterijume zadatka)**
- 10 poena (osnovne funkcije):
	- Rezultati sadrže redni broj rezultata, redni broj stranice i kratak kontekst.
	- Isticanje traženih reči u isečku (konzolno obojeno ili sa mark-up-om).
	- Rangiranje zasnovano na broju pojavljivanja traženih reči.
	- Višerečeni upiti utiču na ukupni rang (više pojavljivanja → viši rang).
	- Konzolni meni za iniciranje pretrage.
- 17 poena:
	- Rangiranje uzima u obzir i veze (in-linkove) i broj pojavljivanja na stranicama koje linkuju ciljnu stranicu.
	- Stranice su organizovane kao graf (`Graph.py`).
	- Trie koristi se za efikasno pretraživanje reči (`Trie.py`).
- 21 poen:
	- Serijalizacija struktura radi bržeg ponovnog pokretanja (`*_serialization.py`).
	- Podrška logičkih operatora `AND`, `OR`, `NOT` i paginacija rezultata.
- >21 poen (dodatno):
	- Fraze, predlozi "did you mean", grupisanje operatora sa zagradama i autocomplete.
	- Dodatne opcije: generisanje PDF-a sa prvih N rezultata, isticanje u PDF-u.

**Saveti za testiranje**
- Testirajte prvo sa `parsed_text.json` da izbegnete dugotrajno parsiranje PDF-a.
- Koristite knjigu "Data Structures and Algorithms in Python" iz `Files/Literatura` kao testni dokument.
- Proverite da li su serijalizovani fajlovi kreirani nakon prvog pokretanja; sledeća pokretanja će biti brža.

**Moguća poboljšanja**
- Poboljšati rangiranje koristeći TF-IDF ili PageRank po grafo-logici.
- GUI ili web interfejs za lakše pregledanje i paginaciju rezultata.
- Naprednije PDF highlighting rešenje koristeći biblioteku koja podržava izmenu PDF-a.

---
Ako želite, mogu odmah:
- pokrenuti `main.py` (ako želite da testiram lokalno),
- ili ažurirati `requirements.txt` sa preporučenim paketima,
- ili dodati primer upita i snimak izlaza.


