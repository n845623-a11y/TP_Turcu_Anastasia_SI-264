# Laboratorul 8 – Lucrarile A si B

Arhiva contine materiale pentru cele DOUA FISE ATASATE: GitHub pas cu pas
si Unealta stricata, reparata cu git. Nu este laboratorul 9 despre colectii.

## Ce este pregatit si ce trebuie sa faci tu

Ai doua foldere-model: exercitiu-git si exercitiu-2, fisele originale,
un program functional pentru B, date de exemplu si raportul generat.
Nu exista istoric Git fabricat, conturi sau depozite GitHub create.
Lucrarea cere actiuni reale pe contul tau si commit-uri facute pas cu pas.
Originalele pentru B sunt acum incluse in Originale_ELSE.
Solutia reparata si raportul sunt in exercitiu-git/depanare.
Citeste REPARATII_LAB_B.md pentru cele zece modificari exacte.

## Lucrarea A – pe rand, in terminalul VS Code

A1. Intra in contul tau GitHub. Daca ai cont, nu crea altul.
A2. Verifica si configureaza Git (inlocuieste valorile intre ghilimele):

```powershell
git --version
git config --global user.name "NUMELE TAU"
git config --global user.email "EMAILUL TAU DE PE GITHUB"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

A3. Pe GitHub creeaza exercitiu-git, Public, cu README bifat.
A4. Intr-un folder de lucru SEPARAT de modelele din arhiva:

```powershell
git clone https://github.com/USERNAME/exercitiu-git.git
cd exercitiu-git
code .
```

Inlocuieste USERNAME cu utilizatorul tau. Nu copia tot modelul deodata:
altfel nu mai faci etapele cerute in istoric.
A5. Copiaza numai salut.py din model in depozitul clonat, apoi:

```powershell
python salut.py
git status
git add salut.py
git commit -m "Adaug salut.py"
```

A6. Ruleaza git push si autentifica-te in browser cand ti se cere.
A7. Pe GitHub editeaza README.md: adauga Aici exersez git.
Salveaza cu Commit changes. In terminal:

```powershell
git pull
Get-Content README.md
```

A8. Creeaza mediul virtual, apoi copiaza .gitignore din model:

```powershell
python -m venv .venv
git status --short
git add .gitignore
git commit -m "Ignor mediul virtual"
git push
```

A9. Ruleaza git log --oneline. Adauga temporar in salut.py:
print("al doilea")
Salveaza si ruleaza git diff. Apoi git restore salut.py elimina
DOAR aceasta modificare de exercitiu, nesalvata intr-un commit.
A10. Intr-un folder nou exercitiu-2, separat de primul depozit,
copiaza README.md din modelul exercitiu-2, apoi:

```powershell
git init
git add README.md
git commit -m "Primul commit"
```

Pe GitHub creeaza exercitiu-2 Public, FARA README. Apoi:

```powershell
git remote add origin https://github.com/USERNAME/exercitiu-2.git
git branch -M main
git push -u origin main
```

A11. Verifica ambele linkuri. Primul depozit trebuie sa aiba cel putin
patru commit-uri: initial, salut.py, README editat online, .gitignore.
A12. Pentru erori consulta tabelul din fisa originala inclusa.

## Lucrarea B – metoda obligatorie cu originalele ELSE

B1. In depozitul REAL exercitiu-git ruleaza git pull.
Creeaza depanare si pune acolo inventar.py STRICAT si tinte.json ORIGINALE.

```powershell
git add depanare
git commit -m "Pornire: inventar.py stricat"
cd depanare
python inventar.py tinte.json --prag 1000
```

B2. Citeste ultima linie a erorii, gaseste linia indicata, explica problema,
repara un singur lucru si ruleaza iar. Dupa fiecare reparatie:

```powershell
git add inventar.py
git commit -m "Descrie eroarea si reparatia facuta"
```

B3. Repara mai intai SyntaxError si IndentationError: semne lipsa,
paranteze si spatii la inceput de rand.
B4. Repara numele variabilelor, conversiile text/numar, cheile lipsa,
return lipsa si tratarea portului invalid, conform erorilor originalului.
B5. Compara iesirea cu rezultatul asteptat: verifica return pus prea devreme
si lista golita/recreata in bucla. Fa un commit pentru fiecare reparatie.
Cele zece modificari exacte sunt explicate in REPARATII_LAB_B.md.
B6. Dupa toate cele zece reparatii:

```powershell
python inventar.py tinte.json --prag 1000
python inventar.py tinte.json
git add raport_inventar.json
git commit -m "Raportul uneltei reparate"
git push
git log --oneline
```

Predai linkurile celor doua depozite; in exercitiu-git trebuie sa se vada
pornirea, cele zece reparatii si raportul. Noteaza ajutorul primit de la
ChatGPT in README. ZIP-ul singur nu tine locul istoricului cerut.

## Cum rulezi exemplul functional inclus

Deschide folderul-model exercitiu-git in VS Code, Terminal > New Terminal:

```powershell
cd depanare
python inventar.py tinte.json --prag 1000
```

Daca pe calculator merge numai py, inlocuieste python cu py.
Rezultatul este in REZULTAT_ASTEPTAT.txt. Pragul implicit este 1024.
Pentru acest exemplu nu trebuie instalate biblioteci suplimentare.
Nu trebuie introduse date personale in tinte.json.
Numele, emailul si USERNAME se folosesc numai in pasii Git/GitHub.

Exercitiile despre recon.py sunt optionale si necesita unealta ta anterioara;
nu sunt incluse ca implementare deoarece acel fisier nu a fost atasat.
