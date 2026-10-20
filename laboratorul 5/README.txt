Laborator Python: funcții, metode și importuri pe web
Nivel: student anul I – Securitate cibernetică

INSTALARE
1. Instalați Python 3.9 sau mai nou.
2. Deschideți terminalul în directorul web_lab.
3. Instalați biblioteca externă:
   python -m pip install -r requirements.txt

RULARE
- Exercițiile 1–8:  python part1_imports.py
- Exercițiile 9–20: python part2_methods.py
- Exercițiile 21–34: python part3_functions.py
- Exercițiile 35–43: python part4_modules.py
- Proiect final:    python main.py https://cybercor.org

Fișierele report.csv și report.json sunt create de main.py la rulare.
Programul trimite doar cereri GET/HEAD către cybercor.org. Cererile care verifică
antete personalizate sunt trimise către httpbin.org. Este folosit timeout, iar
cererile repetate sunt separate prin pauze.

Notă: valorile din raport depind de răspunsurile reale ale site-ului și se pot schimba.
