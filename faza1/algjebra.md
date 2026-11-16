# Algjebra relacionale – Ndreqe (Faza 1)

> Shënim: në specifikimin publik të ekipit janë përcaktuar Q1–Q3. Issue #7 përmend gjashtë pyetje, por për Q4–Q6 nuk u gjetën përshkrime konkrete në issue #5 ose në PR-in e algjebrës. Për të mos shpikur kërkesa, ky dokument përfshin vetëm pyetjet e përcaktuara.

## Q1. Emrat e profesionistëve që ofrojnë kategorinë “Hidraulik”

**Shprehja:**

```text
π_{Perdoruesi.Emri, Perdoruesi.Mbiemri} (
  σ_{Kategoria.Emri = 'Hidraulik'} (
    (Kategoria ⋈_{Kategoria.KID = Profesionisti_Kategoria.KID} Profesionisti_Kategoria)
      ⋈_{Profesionisti_Kategoria.UID_Prof = Profesionisti.UID} Profesionisti
      ⋈_{Profesionisti.UID = Perdoruesi.UID} Perdoruesi
  )
)
```

**Shpjegimi:** Zgjedhim kategorinë Hidraulik, e bashkojmë me lidhjen Profesionisti_Kategoria, me tabelën Profesionisti dhe me Perdoruesi, pastaj projektojmë emrin dhe mbiemrin.

**Rezultati i pritur:**

| Emri | Mbiemri |
|---|---|
| Agim | Thaci |
| Besnik | Maxhuni |
| Valon | Rexhepi |

## Q2. Rezervimet e klientit me email X të kryera me profesionistë të verifikuar

**Shprehja:**

```text
π_{Rezervimi.RZID, Rezervimi.UID_Klienti, Rezervimi.UID_Prof, Rezervimi.Statusi} (
  σ_{Klient.Email = X ∧ Profesionisti.I_Verifikuar = 1} (
    (ρ_{Klient}(Perdoruesi)
      ⋈_{Klient.UID = Rezervimi.UID_Klienti} Rezervimi)
      ⋈_{Rezervimi.UID_Prof = Profesionisti.UID} Profesionisti
  )
)
```

**Shpjegimi:** Gjejmë përdoruesin me email X, bashkojmë rezervimet e tij me profesionistët dhe mbajmë vetëm profesionistët e verifikuar. Për testim, X zëvendësohet me `arben.krasniqi@email.com`.

**Rezultati i pritur për email-in e testimit:**

| RZID | UID_Klienti | UID_Prof | Statusi |
|---:|---:|---:|---|
| 1 | 1 | 16 | perfunduar |

## Q3. Profesionistët që kanë të paktën një rezervim nga klient që banon në Prishtinë

**Shprehja:**

```text
π_{Prof.UID, Prof.Emri, Prof.Mbiemri} (
  σ_{Klient.Roli = 'klient' ∧ Qyteti.Emri = 'Prishtine'} (
    ((ρ_{Klient}(Perdoruesi)
      ⋈_{Klient.QID = Qyteti.QID} Qyteti)
      ⋈_{Klient.UID = Rezervimi.UID_Klienti} Rezervimi)
      ⋈_{Rezervimi.UID_Prof = Prof.UID} ρ_{Prof}(Perdoruesi)
  )
)
```

**Shpjegimi:** Gjejmë klientët që banojnë në Prishtinë, bashkojmë rezervimet e tyre me përdoruesit profesionistë dhe projektojmë identifikuesin, emrin dhe mbiemrin e profesionistëve.

**Rezultati i pritur:**

| UID | Emri | Mbiemri |
|---:|---|---|
| 16 | Besnik | Maxhuni |
| 17 | Valon | Rexhepi |
| 19 | Shpend | Ukaj |
| 21 | Faton | Krasniqi |

## Pyetjet Q4–Q6

Nuk janë përfshirë, sepse përshkrimet e tyre nuk janë të pranishme në specifikimin e disponueshëm të projektit. Duhet të konfirmohen nga ekipi/profesori para se të shkruhen shprehjet dhe rregullat përkatëse.
