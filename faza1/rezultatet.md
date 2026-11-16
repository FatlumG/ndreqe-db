# Krahasimi i rezultateve: RelaX dhe Datalog

Gjashte pyetesoret jane ekzekutuar ne RelaX (algjebra relacionale) dhe ne Datalog (DES) me te njejtat te dhena. Per cdo pyetesor jepet query-ja, rezultati dhe nese dy sistemet perputhen.

## Q1 - Profesionistet qe ofrojne "Hidraulik"

**RelaX:**

```
π Perdoruesi.UID, Perdoruesi.Emri, Perdoruesi.Mbiemri (σ Kategoria.Emri = 'Hidraulik' (Kategoria ⨝ Kategoria.KID = Profesionisti_Kategoria.KID Profesionisti_Kategoria ⨝ Profesionisti_Kategoria.UID_Prof = Perdoruesi.UID Perdoruesi))
```

**Datalog:**

```
q1(UID, Emri, Mbiemri) :-
    kategoria(KID, 'Hidraulik', _),
    profesionisti_kategoria(UID, KID, _, _, _),
    profesionisti(UID, _, _, _, _),
    perdoruesi(UID, Emri, Mbiemri, _, _, _, _, _, _).
```

**Rezultati (3 rreshta):**

| UID | Emri | Mbiemri |
|---|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 18 | Agim | Thaci |

**Statusi:** RelaX dhe Datalog perputhen.

## Q2 - Rezervimet e klientit me email X te profesionistet e verifikuar

Per test: X = `arben.krasniqi@email.com`.

**RelaX:**

```
π R.RZID, R.UID_Klienti, R.UID_Prof, R.Statusi (σ K.Email = 'arben.krasniqi@email.com' ∧ P.I_Verifikuar = 1 (ρ K (Perdoruesi) ⨝ K.UID = R.UID_Klienti ρ R (Rezervimi) ⨝ R.UID_Prof = P.UID ρ P (Profesionisti)))
```

**Datalog:**

```
q2(RZID, UID_Klienti, UID_Prof, Statusi) :-
    perdoruesi(UID_Klienti, _, _, 'arben.krasniqi@email.com', _, _, _, _, _),
    rezervimi(RZID, UID_Klienti, UID_Prof, _, _, _, _, _, _, Statusi, _, _),
    profesionisti(UID_Prof, _, _, 1, _).
```

**Rezultati (1 rresht):**

| RZID | UID_Klienti | UID_Prof | Statusi |
|---|---|---|---|
| 1 | 1 | 16 | perfunduar |

**Statusi:** RelaX dhe Datalog perputhen.

## Q3 - Profesionistet me se paku nje rezervim nga klient i Prishtines

**RelaX:**

```
π P.UID, P.Emri, P.Mbiemri (σ Q.Emri = 'Prishtine' ∧ K.Roli = 'klient' (ρ K (Perdoruesi) ⨝ K.QID = Q.QID ρ Q (Qyteti) ⨝ K.UID = R.UID_Klienti ρ R (Rezervimi) ⨝ R.UID_Prof = P.UID ρ P (Perdoruesi)))
```

**Datalog:**

```
q3(UID_Prof, Emri, Mbiemri) :-
    qyteti(QID, 'Prishtine', _),
    perdoruesi(UID_Klienti, _, _, _, _, QID, 'klient', _, _),
    rezervimi(_, UID_Klienti, UID_Prof, _, _, _, _, _, _, _, _, _),
    profesionisti(UID_Prof, _, _, _, _),
    perdoruesi(UID_Prof, Emri, Mbiemri, _, _, _, _, _, _).
```

**Rezultati (4 rreshta):**

| UID | Emri | Mbiemri |
|---|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 19 | Shpend | Ukaj |
| 21 | Faton | Krasniqi |

**Statusi:** RelaX dhe Datalog perputhen.

## Q4 - Profesionistet qe ofrojne nje kategori por nuk kane rezervim ne te

**RelaX:**

```
Oferta = π UID_Prof, KID (Profesionisti_Kategoria)
Rezervuar = π UID_Prof, KID (Rezervimi)
Pa = Oferta - Rezervuar
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = Pa.UID_Prof Pa)
```

**Datalog:**

```
ka_rezervim_kat(UID_Prof, KID) :-
    rezervimi(_, _, UID_Prof, KID, _, _, _, _, _, _, _, _).

q4(UID_Prof, Emri, Mbiemri) :-
    profesionisti_kategoria(UID_Prof, KID, _, _, _),
    not(ka_rezervim_kat(UID_Prof, KID)),
    profesionisti(UID_Prof, _, _, _, _),
    perdoruesi(UID_Prof, Emri, Mbiemri, _, _, _, _, _, _).
```

**Rezultati (3 rreshta):**

| UID | Emri | Mbiemri |
|---|---|---|
| 17 | Valon | Rexhepi |
| 23 | Ramadan | Jashari |
| 25 | Skender | Osmani |

**Statusi:** RelaX dhe Datalog perputhen.

## Q5 - Profesionistet me note 5 nga me shume se nje klient

**RelaX:**

```
Notat5 = π R.UID_Prof, R.UID_Klienti (σ V.Nota = 5 (ρ V (Vleresimi) ⨝ V.RZID = R.RZID ρ R (Rezervimi)))
Dyshe = π X.UID_Prof (σ X.UID_Prof = Y.UID_Prof ∧ X.UID_Klienti ≠ Y.UID_Klienti (ρ X (Notat5) cross join ρ Y (Notat5)))
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = Dyshe.UID_Prof Dyshe)
```

**Datalog:**

```
q5(UID_Prof, Emri, Mbiemri) :-
    vleresimi(_, RZID1, 5, _, _),
    rezervimi(RZID1, UID_Klienti1, UID_Prof, _, _, _, _, _, _, _, _, _),
    vleresimi(_, RZID2, 5, _, _),
    rezervimi(RZID2, UID_Klienti2, UID_Prof, _, _, _, _, _, _, _, _, _),
    UID_Klienti1 \= UID_Klienti2,
    profesionisti(UID_Prof, _, _, _, _),
    perdoruesi(UID_Prof, Emri, Mbiemri, _, _, _, _, _, _).
```

**Rezultati (1 rresht):**

| UID | Emri | Mbiemri |
|---|---|---|
| 16 | Besnik | Maxhuni |

**Statusi:** RelaX dhe Datalog perputhen.

## Q6 - Klientet qe kane rezervuar "Elektricist" ose kane dhene noten 1

**RelaX:**

```
A = π R.UID_Klienti (σ K.Emri = 'Elektricist' (ρ K (Kategoria) ⨝ K.KID = R.KID ρ R (Rezervimi)))
B = π R.UID_Klienti (σ V.Nota = 1 (ρ V (Vleresimi) ⨝ V.RZID = R.RZID ρ R (Rezervimi)))
C = A ∪ B
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = C.UID_Klienti C)
```

**Datalog:**

```
q6(UID_Klienti, Emri, Mbiemri) :-
    kategoria(KID, 'Elektricist', _),
    rezervimi(_, UID_Klienti, _, KID, _, _, _, _, _, _, _, _),
    perdoruesi(UID_Klienti, Emri, Mbiemri, _, _, _, _, _, _).

q6(UID_Klienti, Emri, Mbiemri) :-
    vleresimi(_, RZID, 1, _, _),
    rezervimi(RZID, UID_Klienti, _, _, _, _, _, _, _, _, _, _),
    perdoruesi(UID_Klienti, Emri, Mbiemri, _, _, _, _, _, _).
```

**Rezultati (5 rreshta):**

| UID | Emri | Mbiemri |
|---|---|---|
| 3 | Driton | Gashi |
| 5 | Fatmir | Morina |
| 6 | Gentiana | Shala |
| 13 | Nora | Gjoka |
| 15 | Pranvera | Kastrati |

**Statusi:** RelaX dhe Datalog perputhen.

## Perfundimi

| Pyetesori | RelaX | Datalog | Statusi |
|---|---|---|---|
| Q1 | 3 | 3 | perputhen |
| Q2 | 1 | 1 | perputhen |
| Q3 | 4 | 4 | perputhen |
| Q4 | 3 | 3 | perputhen |
| Q5 | 1 | 1 | perputhen |
| Q6 | 5 | 5 | perputhen |

Te gjashta pyetesoret kthejne te njejtat rreshta ne dy sistemet. Nuk ka dallime.
