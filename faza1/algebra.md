# Relational Algebra Queries

## Q1. Names of professionals who offer the category "Hidraulik"

**Expression:**

\[
\pi_{Perdoruesi.Emri,\ Perdoruesi.Mbiemri}
\left(
\sigma_{Kategoria.Emri='Hidraulik'}
\left(
(Kategoria \bowtie_{Kategoria.KID=Profesionisti\_Kategoria.KID} Profesionisti\_Kategoria)
\bowtie_{Profesionisti\_Kategoria.UID\_Prof=Profesionisti.UID} Profesionisti
\bowtie_{Profesionisti.UID=Perdoruesi.UID} Perdoruesi
\right)
\right)
\]

**Explanation:** Selects the Hidraulik category, joins it with the professionals who offer it, and returns their first and last names.

**Expected result:**

| Emri | Mbiemri |
|---|---|
| Besnik | Maxhuni |
| Valon | Rexhepi |
| Agim | Thaci |

## Q2. Bookings of the client with email X made with verified professionals

**Expression:**

\[
\pi_{Rezervimi.RZID,\ Rezervimi.UID\_Klienti,\ Rezervimi.UID\_Prof,\ Rezervimi.Statusi}
\left(
\sigma_{Klient.Email='X' \land Profesionisti.I\_Verifikuar=1}
\left(
(\rho_{Klient}(Perdoruesi)
\bowtie_{Klient.UID=Rezervimi.UID\_Klienti} Rezervimi)
\bowtie_{Rezervimi.UID\_Prof=Profesionisti.UID} Profesionisti
\right)
\right)
\]

**Explanation:** Finds the client's bookings by email and keeps only bookings assigned to verified professionals.

**Expected result:** Depends on the email represented by X. For testing with `arben.krasniqi@email.com`, the result is:

| RZID | UID_Klienti | UID_Prof | Statusi |
|---|---:|---:|---|
| 1 | 1 | 16 | perfunduar |

For the test, replace `X` in the expression with `arben.krasniqi@email.com`.

## Q3. Professionals who have at least one booking from a client living in Prishtina

**Expression:**

\[
\pi_{Prof.UID,\ Prof.Emri,\ Prof.Mbiemri}
\left(
\sigma_{Klient.Roli='klient' \land Qyteti.Emri='Prishtine'}
\left(
((\rho_{Klient}(Perdoruesi)
\bowtie_{Klient.QID=Qyteti.QID} Qyteti)
\bowtie_{Klient.UID=Rezervimi.UID\_Klienti} Rezervimi)
\bowtie_{Rezervimi.UID\_Prof=Prof.UID}
\rho_{Prof}(Perdoruesi)
\right)
\right)
\]

**Explanation:** Finds clients living in Prishtina, joins their bookings with the professionals, and returns each professional who has at least one such booking.

**Expected result:**

| UID | Emri | Mbiemri |
|---:|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 19 | Shpend | Ukaj |
| 21 | Faton | Krasniqi |
