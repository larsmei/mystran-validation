# mystran-validation

Validierungssuite für [MYSTRAN](https://github.com/MYSTRANsolver/MYSTRAN):
Eingabedecks, Referenz-F06 und ein Vergleichsskript.

Die Decks und Referenz-F06 stammen aus der offiziellen Sammlung
[MystranSolver/MYSTRAN_Validation](https://github.com/MystranSolver/MYSTRAN_Validation)
und wurden für eine handliche Suite ausgewählt.

## Inhalt

```
eingabe/                 MYSTRAN-/NASTRAN-Bulk (.DAT, .bdf)
referenz_f06/            Referenzlösungen (MYSTRAN-F06)
testdefinitionen/        Kriterien der Upstream-Suite
run_validation.py        F06-Vergleich (Verschiebungen, Eigenwerte)
run_all.sh               Batch-Lauf aller Decks
```

## Voraussetzungen

- Python 3.9+
- Ein MYSTRAN-Binary (`mystran` / `mystran.exe`), z. B. aus den
  [Releases](https://github.com/MYSTRANsolver/MYSTRAN/releases) oder selbst gebaut.

## Suite ausführen

```bash
git clone https://github.com/larsmei/mystran-validation.git
cd mystran-validation
```

Einzelnes Deck:

```bash
mystran eingabe/bar_01.DAT
python3 run_validation.py --f06 bar_01.F06 --reference referenz_f06/bar_01.F06
```

Erwartete Ausgabe: `PASS` (Default rtol=5e-5, atol=1e-8).

Alle Fälle:

```bash
chmod +x run_all.sh
MYSTRAN=mystran ./run_all.sh
```

Windows (PowerShell):

```powershell
mystran.exe .\eingabe\bar_01.DAT
python .\run_validation.py --f06 .\bar_01.F06 --reference .\referenz_f06\bar_01.F06
```

Referenz nur anzeigen:

```bash
python3 run_validation.py --extract referenz_f06/EB-BAR-CC-GIV.F06
```

## Enthaltene Fälle

Siehe Tabelle im Repository-README. Kurz: CBAR, CBUSH, CROD, RBE2, RBE3,
GRAV, HEXA8, Eigenwerte (Givens), NAS S30 gravity/hexa.

Beispiele Sollwerte:
- bar_01 GRID 2: T = (-4.618988, 1.628426, 0.391897)
- EB-BAR-CC-GIV Mode 1-4: 10.68719, 62.81653, 166.3460, 289.9396 Hz

Vollständige Upstream-Suite: https://github.com/MystranSolver/MYSTRAN_Validation

## Lizenz

MIT (Testdateien analog zur Upstream-Lizenz).
