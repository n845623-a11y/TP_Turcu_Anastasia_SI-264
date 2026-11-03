# Cele zece reparatii ale programului ORIGINAL

Foloseste Originale_ELSE/inventar.py ca punct de pornire in depozitul tau.
Datele tinte.json sunt cele furnizate de tine. Exemplarele din exercitiu-git/depanare sunt deja reparate.
Nu copia solutia finala peste original la inceput: aplica pe rand pasii de mai jos. Dupa fiecare modificare salveaza si ruleaza din nou.

Pornire, din radacina depozitului exercitiu-git:
```powershell
git pull
git add depanare
git commit -m "Pornire: inventar.py stricat"
cd depanare
python inventar.py tinte.json --prag 1000
```

## Reparatia 1: SyntaxError: adaug doua puncte la definitia incarca

Inlocuieste:
```python
def incarca(cale)
```
Cu:
```python
def incarca(cale):
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "SyntaxError: adaug doua puncte la definitia incarca"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 2: IndentationError: indentez return None in except

Inlocuieste:
```python
    except ValueError:
    return None
```
Cu:
```python
    except ValueError:
        return None
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "IndentationError: indentez return None in except"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 3: NameError: corectez tinta in tinte

Inlocuieste:
```python
len(tinta)
```
Cu:
```python
len(tinte)
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "NameError: corectez tinta in tinte"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 4: TypeError: convertesc numarul tintelor in text

Inlocuieste:
```python
print("Tinte citite: " + len(tinte))
```
Cu:
```python
print("Tinte citite: " + str(len(tinte)))
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "TypeError: convertesc numarul tintelor in text"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 5: KeyError: folosesc necunoscut pentru serviciul lipsa

Inlocuieste:
```python
serviciu = t["serviciu"]
```
Cu:
```python
serviciu = t.get("serviciu", "necunoscut")
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "KeyError: folosesc necunoscut pentru serviciul lipsa"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 6: AttributeError: intorc dictionarul grupe

Inlocuieste:
```python
        grupe[serviciu].append(port)
```
Cu:
```python
        grupe[serviciu].append(port)
    return grupe
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "AttributeError: intorc dictionarul grupe"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 7: TypeError: citesc pragul ca int

Inlocuieste:
```python
p.add_argument("--prag", default=1024)
```
Cu:
```python
p.add_argument("--prag", type=int, default=1024)
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "TypeError: citesc pragul ca int"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 8: ValueError: tratez portul invalid cu port_valid

Inlocuieste:
```python
        port = int(t["port"])
```
Cu:
```python
        port = port_valid(t["port"])
        if port is None:
            continue
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "ValueError: tratez portul invalid cu port_valid"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 9: Logica: mut return rezultat dupa bucla

Inlocuieste:
```python
            rezultat.append(t["gazda"])
        return rezultat
```
Cu:
```python
            rezultat.append(t["gazda"])
    return rezultat
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "Logica: mut return rezultat dupa bucla"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Reparatia 10: Logica: pastrez porturile deja adaugate serviciului

Inlocuieste:
```python
        grupe[serviciu] = []
```
Cu:
```python
        grupe.setdefault(serviciu, [])
```
Apoi:
```powershell
python inventar.py tinte.json --prag 1000
git add inventar.py
git commit -m "Logica: pastrez porturile deja adaugate serviciului"
```

Urmatoarea eroare poate aparea dupa reparatie: acest lucru este normal. Pasul 8 poate sa nu fie vizibil pana muti return la pasul 9. Ultimele doua reparatii corecteaza rezultate incomplete.

## Verificarea finala
```powershell
python inventar.py tinte.json --prag 1000
python inventar.py tinte.json
git add raport_inventar.json
git commit -m "Raportul uneltei reparate"
git push
git log --oneline
```
Commit-urile se creeaza cand parcurgi tu pasii. Arhiva nu contine istoric Git precompletat.
