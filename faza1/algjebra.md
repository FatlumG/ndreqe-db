# Pyetesoret ne algjebre relacionale

Pyetesoret jane testuar ne RelaX me te dhenat e projektit. Nen cdo shprehje jepet query-ja e ekzekutuar ne RelaX dhe rezultati.

## Q1. Profesionistet qe ofrojne kategorine "Hidraulik"

$$
\pi_{Perdoruesi.UID,\ Perdoruesi.Emri,\ Perdoruesi.Mbiemri}
\Big(
\sigma_{Kategoria.Emri = \text{'Hidraulik'}}
\big(
Kategoria
\bowtie_{Kategoria.KID = Profesionisti\_Kategoria.KID}
Profesionisti\_Kategoria
\bowtie_{Profesionisti\_Kategoria.UID\_Prof = Perdoruesi.UID}
Perdoruesi
\big)
\Big)
$$

**RelaX:**

```
π Perdoruesi.UID, Perdoruesi.Emri, Perdoruesi.Mbiemri (σ Kategoria.Emri = 'Hidraulik' (Kategoria ⨝ Kategoria.KID = Profesionisti_Kategoria.KID Profesionisti_Kategoria ⨝ Profesionisti_Kategoria.UID_Prof = Perdoruesi.UID Perdoruesi))
```

**Rezultati (3 rreshta):**

| UID | Emri | Mbiemri |
|---:|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 18 | Agim | Thaci |

## Q2. Rezervimet e klientit me email X te profesionistet e verifikuar

Per test: X = `arben.krasniqi@email.com`.

$$
\pi_{R.RZID,\ R.UID\_Klienti,\ R.UID\_Prof,\ R.Statusi}
\Big(
\sigma_{K.Email = \text{'arben.krasniqi@email.com'} \ \wedge\ P.I\_Verifikuar = 1}
\big(
\rho_{K}(Perdoruesi)
\bowtie_{K.UID = R.UID\_Klienti}
\rho_{R}(Rezervimi)
\bowtie_{R.UID\_Prof = P.UID}
\rho_{P}(Profesionisti)
\big)
\Big)
$$

**RelaX:**

```
π R.RZID, R.UID_Klienti, R.UID_Prof, R.Statusi (σ K.Email = 'arben.krasniqi@email.com' ∧ P.I_Verifikuar = 1 (ρ K (Perdoruesi) ⨝ K.UID = R.UID_Klienti ρ R (Rezervimi) ⨝ R.UID_Prof = P.UID ρ P (Profesionisti)))
```

**Rezultati (1 rresht):**

| RZID | UID_Klienti | UID_Prof | Statusi |
|---:|---:|---:|---|
| 1 | 1 | 16 | perfunduar |

## Q3. Profesionistet me se paku nje rezervim nga klient i Prishtines

$$
\pi_{P.UID,\ P.Emri,\ P.Mbiemri}
\Big(
\sigma_{Q.Emri = \text{'Prishtine'} \ \wedge\ K.Roli = \text{'klient'}}
\big(
\rho_{K}(Perdoruesi)
\bowtie_{K.QID = Q.QID}
\rho_{Q}(Qyteti)
\bowtie_{K.UID = R.UID\_Klienti}
\rho_{R}(Rezervimi)
\bowtie_{R.UID\_Prof = P.UID}
\rho_{P}(Perdoruesi)
\big)
\Big)
$$

**RelaX:**

```
π P.UID, P.Emri, P.Mbiemri (σ Q.Emri = 'Prishtine' ∧ K.Roli = 'klient' (ρ K (Perdoruesi) ⨝ K.QID = Q.QID ρ Q (Qyteti) ⨝ K.UID = R.UID_Klienti ρ R (Rezervimi) ⨝ R.UID_Prof = P.UID ρ P (Perdoruesi)))
```

**Rezultati (4 rreshta):**

| UID | Emri | Mbiemri |
|---:|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 19 | Shpend | Ukaj |
| 21 | Faton | Krasniqi |

## Q4. Profesionistet qe ofrojne nje kategori por nuk kane rezervim ne te (diferenca)

$$
Oferta = \pi_{UID\_Prof,\ KID}(Profesionisti\_Kategoria)
$$

$$
Rezervuar = \pi_{UID\_Prof,\ KID}(Rezervimi)
$$

$$
Pa = Oferta - Rezervuar
$$

$$
\pi_{P.UID,\ P.Emri,\ P.Mbiemri}
\big(
\rho_{P}(Perdoruesi) \bowtie_{P.UID = Pa.UID\_Prof} Pa
\big)
$$

**RelaX:**

```
Oferta = π UID_Prof, KID (Profesionisti_Kategoria)
Rezervuar = π UID_Prof, KID (Rezervimi)
Pa = Oferta - Rezervuar
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = Pa.UID_Prof Pa)
```

**Rezultati (3 rreshta):**

| UID | Emri | Mbiemri |
|---:|---|---|
| 17 | Valon | Rexhepi |
| 23 | Ramadan | Jashari |
| 25 | Skender | Osmani |

## Q5. Profesionistet me note 5 nga me shume se nje klient (self-join)

$$
Notat5 = \pi_{R.UID\_Prof,\ R.UID\_Klienti}
\big(
\sigma_{V.Nota = 5}
(\rho_{V}(Vleresimi) \bowtie_{V.RZID = R.RZID} \rho_{R}(Rezervimi))
\big)
$$

$$
Dyshe = \pi_{X.UID\_Prof}
\big(
\sigma_{X.UID\_Prof = Y.UID\_Prof \ \wedge\ X.UID\_Klienti \neq Y.UID\_Klienti}
(\rho_{X}(Notat5) \times \rho_{Y}(Notat5))
\big)
$$

$$
\pi_{P.UID,\ P.Emri,\ P.Mbiemri}
\big(
\rho_{P}(Perdoruesi) \bowtie_{P.UID = Dyshe.UID\_Prof} Dyshe
\big)
$$

**RelaX:**

```
Notat5 = π R.UID_Prof, R.UID_Klienti (σ V.Nota = 5 (ρ V (Vleresimi) ⨝ V.RZID = R.RZID ρ R (Rezervimi)))
Dyshe = π X.UID_Prof (σ X.UID_Prof = Y.UID_Prof ∧ X.UID_Klienti ≠ Y.UID_Klienti (ρ X (Notat5) cross join ρ Y (Notat5)))
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = Dyshe.UID_Prof Dyshe)
```

**Rezultati (1 rresht):**

| UID | Emri | Mbiemri |
|---:|---|---|
| 16 | Besnik | Maxhuni |

## Q6. Klientet qe kane rezervuar "Elektricist" ose kane dhene noten 1 (union)

$$
A = \pi_{R.UID\_Klienti}
\big(
\sigma_{K.Emri = \text{'Elektricist'}}
(\rho_{K}(Kategoria) \bowtie_{K.KID = R.KID} \rho_{R}(Rezervimi))
\big)
$$

$$
B = \pi_{R.UID\_Klienti}
\big(
\sigma_{V.Nota = 1}
(\rho_{V}(Vleresimi) \bowtie_{V.RZID = R.RZID} \rho_{R}(Rezervimi))
\big)
$$

$$
C = A \cup B
$$

$$
\pi_{P.UID,\ P.Emri,\ P.Mbiemri}
\big(
\rho_{P}(Perdoruesi) \bowtie_{P.UID = C.UID\_Klienti} C
\big)
$$

**RelaX:**

```
A = π R.UID_Klienti (σ K.Emri = 'Elektricist' (ρ K (Kategoria) ⨝ K.KID = R.KID ρ R (Rezervimi)))
B = π R.UID_Klienti (σ V.Nota = 1 (ρ V (Vleresimi) ⨝ V.RZID = R.RZID ρ R (Rezervimi)))
C = A ∪ B
π P.UID, P.Emri, P.Mbiemri (ρ P (Perdoruesi) ⨝ P.UID = C.UID_Klienti C)
```

**Rezultati (5 rreshta):**

| UID | Emri | Mbiemri |
|---:|---|---|
| 3 | Driton | Gashi |
| 5 | Fatmir | Morina |
| 6 | Gentiana | Shala |
| 13 | Nora | Gjoka |
| 15 | Pranvera | Kastrati |
