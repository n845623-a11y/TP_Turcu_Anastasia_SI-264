# Laboratorul 6 — Forensics și steganografie

Soluție pentru lucrările A și B. Toate probele sunt generate local și pot fi regenerate.

## Rulare în PowerShell

```powershell
cd "$HOME/Desktop/lucrarenrutty"
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ruleaza.py
```

`ruleaza.py` execută toate etapele, inclusiv testele. Output-ul se salvează în `rezultate/output.txt`. Raportul este în `raport.md`. Nu sunt necesare pytest, conturi sau acces la rețea după instalarea Pillow.

Scriptul original `probe/pregateste.py` nu a fost furnizat. Versiunea inclusă generează probe demonstrative echivalente; rezultatele nu reprezintă probele originale ale cadrului didactic. GPS-ul este artificial. Challenge-ul opțional nu este inclus în fișa atașată.

Predarea prin git se face în depozitul personal al disciplinei. Copiază conținutul acestui folder în acel depozit, verifică fișierele și rulează comenzile cerute de fișă:

```powershell
git add .
git commit -m "Lab 6: decoder universal + forensics si stego"
git push
```

 Proiectul este încărcat în depozitul personal al disciplinei, în folderul `laboratorul 6`.
