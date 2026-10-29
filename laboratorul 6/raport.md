# Laboratorul 6 — Informații invizibile, forensics și steganografie

## Scop și proveniența probelor

Am implementat un decoder în straturi, căutarea cheii XOR pe un octet, verificarea hashurilor prin dicționar, analiza fișierelor și steganografia LSB. Toate operațiile au fost executate pe fișiere demonstrative generate local.

Fișa primită nu include scriptul original de pregătire sau probele disciplinei. Scriptul `probe/pregateste.py` din această lucrare este o implementare proprie care creează probe echivalente. Rezultatele de mai jos sunt reale pentru aceste probe, nu rezultate pretinse pentru fișierele originale. Coordonatele GPS sunt introduse artificial.

## Lucrarea A

### A1 Text și octeți

Pentru `s = "Salut"`, `s.encode()` produce `b"Salut"`, iar `b[0]` este numărul 83. Reprezentarea hexazecimală este `53616c7574`; `bytes.fromhex("53616c7574")` reface octeții inițiali. Output-ul se află în `rezultate/incalzire.txt`.

### A2 și A3 Recunoaștere și decodare

`ghici_strat` verifică URL, hex și apoi base64, în această ordine. Pentru URL se caută secvențe `%xx`; hex cere lungime pară și caractere hexazecimale; base64 este validat strict. `desfa` întoarce tipul și rezultatul în octeți. Un text poate semăna cu o codare, deci clasificarea este o euristică, nu o dovadă.

### A4 Straturi multiple

Comandă: `python arsenal/forensics/decode.py probe/mesaj.txt --fisier`

Au fost desfăcute straturile URL → base64 → hex. Mesajul final este:

```text
FLAG{straturile_au_fost_decodate}
```

Fișa rezultatului este `arsenal/forensics/fisa.json`. Bucla are limita de 8 pași și detectează rezultate repetate. Nu se oprește imediat ce rezultatul este imprimabil, deoarece și un strat intermediar hex sau base64 poate fi imprimabil. Exemplul `NTM1OTU3NTk=` devine `53595759`, apoi `SYWY`; interpretarea următoare ca base64 ar produce octeți neimprimabili și este respinsă de euristică.

### A5 XOR cu o cheie de un octet

Comandă: `python arsenal/forensics/decode.py probe/xor.bin --fisier --mod xor --iesire rezultate/xor.json`

Au fost încercate toate cele 256 de chei. Cheia identificată este **73**, adică **0x49**. Textul recuperat este `FLAG{xor_cu_cheia_73}`. Programul păstrează candidații imprimabili și îi ordonează după un scor simplu; imprimabilitatea singură nu garantează cheia corectă. În această probă, formatul FLAG confirmă candidatul.

### A6 Hashuri și dicționar

Comandă: `python arsenal/forensics/decode.py probe/hashuri.txt --fisier --mod hash --iesire rezultate/hashuri.json`

| Lungime | Algoritm al probei | Parolă recuperată |
| --- | --- | --- |
| 32 | MD5 | laborator6 |
| 40 | SHA1 | parola123 |
| 64 | SHA256 | securitate |

Fiecare cuvânt din wordlist este hashuit și comparat cu ținta. Hashul nu este decriptat. Lungimea sugerează algoritmul numai în setul de algoritmi folosit de laborator; în general nu îl identifică unic. O parolă absentă din dicționar nu poate fi găsită prin această căutare.

### A7 Interfață și teste

Interfața folosește argparse, acceptă un șir sau `--fisier`, iar `--mod` selectează decode, xor ori hash. `--iesire` stabilește fișa JSON. Testele se rulează cu `python -m unittest discover -s teste -v`.

## Lucrarea B

### B1 Tipurile reale

`foto.jpg` are semnătura JPEG `ff d8`, iar `ascuns.png` are semnătura PNG `89 50 4e 47 0d 0a 1a 0a`. `stego.png` este tot PNG. Funcția include și recunoașterea PDF și ZIP; semnătura ZIP singură nu distinge DOCX de alte arhive ZIP.

### B2 Text imprimabil

Regexul pe octeți `[ -~]{4,}` identifică, între altele, `secret.txt` și `FLAG{arhiva_ascunsa_la_coada}`. Într-un binar pot exista și secvențe imprimabile întâmplătoare; indiciile trebuie confirmate. Lista completă se află în `rezultate/forensics.json` și în output-ul de execuție.

### B3 EXIF și GPS

Metadatele recuperate sunt Make = `Laborator demonstrativ`, Model = `Camera virtuala`, DateTime = `2026:10:20 12:00:00`.

Coordonatele introduse în probă sunt 47° 1′ 12″ N și 28° 49′ 48″ E. Formula este grade + minute / 60 + secunde / 3600, cu semn negativ pentru S sau W. Rezultatul este **47.020000 N, 28.830000 E**. Aceste valori sunt artificiale, nu localizarea unei fotografii reale.

### B4 Extragerea arhivei

Programul parcurge chunkurile PNG până la IEND, apoi caută semnătura ZIP în datele de după imagine. Astfel evită alegerea unei semnături accidentale din pixelii comprimați. Arhiva începe la octetul **2772** și a fost salvată în `rezultate/gasit.zip`. Verificarea CRC a arhivei a reușit.

Arhiva conține `secret.txt`, cu textul:

```text
FLAG{arhiva_ascunsa_la_coada}
```

Conținutul este salvat și în `rezultate/secret.txt`. Nu sunt extrase automat căi arbitrare din arhivă.

### B5 Ascunderea mesajului

Comandă: `python arsenal/forensics/lsb.py ascunde probe/foto.jpg stego.png "FLAG{ascuns_in_pixeli}"`

Imaginea este convertită în RGB. Octeții UTF-8 ai mesajului, urmați de un octet nul, sunt transformați în biți de la cel mai semnificativ la cel mai puțin semnificativ. Fiecare bit înlocuiește ultimul bit al următorului canal R, G, B, în ordinea pixelilor. Programul verifică întâi capacitatea și respinge mesajele cu terminator nul în interior.

Imaginea are 320 × 240 pixeli și 230400 de canale. Capacitatea este 28800 de octeți, din care un octet este rezervat terminatorului. Mesajul ocupă 22 de octeți împreună cu terminatorul. PNG păstrează exact acești biți; o recomprimare JPEG îi poate distruge.

### B6 Recuperarea mesajului

Comandă: `python arsenal/forensics/lsb.py dezvaluie stego.png`

Rezultatul efectiv este:

```text
FLAG{ascuns_in_pixeli}
```

Citirea parcurge aceleași canale, grupează biții câte 8 și se oprește la octetul nul. Mesajul recuperat este identic cu cel ascuns.

## Verificare și reproducere

`python ruleaza.py` regenerează probele, execută lucrările A și B și rulează testele. Output-ul complet este salvat în `rezultate/output.txt`. Cele **8 teste au trecut**, acoperind base64, hex, URL, straturi, XOR, MD5/SHA1/SHA256, intrări invalide, GPS, recuperare LSB cu diacritice și limite de capacitate.

Challenge-ul opțional nu a fost realizat deoarece `challenge.bin` original nu este furnizat. Predarea a fost încărcată în depozitul personal al disciplinei, în folderul `laboratorul 6`. Instrucțiunile de rulare și predare sunt în `README.md`.

## Concluzii

Codarea este reversibilă fără cheie. XOR pe un octet poate fi analizat prin numai 256 de încercări. Hashurile sunt verificate prin comparare, iar succesul dicționarului depinde de cuvintele disponibile. Semnăturile identifică structura fișierului, metadatele pot expune informații suplimentare, iar datele pot fi ascunse atât după sfârșitul unei imagini, cât și în biții pixelilor. Toate rezultatele prezentate sunt susținute de fișiere și de output-ul programelor.
