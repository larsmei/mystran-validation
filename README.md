# mystran-validation

Validierungssuite für [MYSTRAN](https://github.com/MYSTRANsolver/MYSTRAN):
Eingabedecks, Sollwerte (Verschiebung, Eigenwerte, **Spannungen**) und Runner.

Quelle: [MystranSolver/MYSTRAN_Validation](https://github.com/MystranSolver/MYSTRAN_Validation).

## Suite ausführen

```bash
git clone https://github.com/larsmei/mystran-validation.git
cd mystran-validation
mystran eingabe/bar_01.DAT
python3 run_validation.py --f06 bar_01.F06 --expected-json referenz_werte.json --case bar_01
MYSTRAN=mystran ./run_all.sh
```

Spannungs-Kriterien (BAR/ROD/BUSH/SOLID) stehen in
`testdefinitionen/spannungen.txt` und in `referenz_werte.json`
(`bar_stresses`, `rod_stresses`, `bush_stresses`, `solid_stresses`).

## Spannungs-Testfälle

| Fall | Element | Geprüfte Spannungen | Referenz |
|---|---|---|---|
| `bar_01` | CBAR | SA1..SA4, Axial, SA-Max/Min | SA2 = 2027.083, Axial = 13.38525 |
| `bush_01` | CBUSH | S1..S6 | S1 = 457.7756, S2 = -37234.88 |
| `SB-RODDISPL-N-LOAD` | CROD | Axial, Torsion | EID1 Axial = 2162.162, Torsion = 0 |
| `SB-RBE2-01-CROD-03` | CROD | Axial | EID14 = 9.0e4, EID21 = 1.1e5 |
| `SB-BAR-GRAV` | CBAR | SA*, Axial | EID12 Axial = 60.30, SA-Max = 106.425 |
| `NAS S30 hexa` | HEXA8 | Center YY, von Mises | 17121.99 (xx/zz/tau ~ 0) |
| `SB-HEXA08-…-2x2x2` | HEXA8 | Center Tensor + vM | vM = 233.8019 |

Upstream-Analytik (nicht in diesem Teilpaket, aber dokumentiert):
`NAS S30 corner stress strain hex8.bdf` — Corner YY=2, ZZ=3 auf EID 1.
`CHEXA.bdf` in `cases_new.txt` — Center-Tensor 2000/2000/2000 plus Schub 400
(teilweise KNOWNFAIL, Issue 225).

Offizielle Pfade: `BARSTRESSES`, `RODSTRESSES`, `SHELLSTRESSES`, `SOLIDSTRESSES`.
