# Ndreqe DB

Databaza relacionale për platformën Ndreqe, ku njerëzit në Kosovë rezervojnë profesionistë për shtëpinë.
Projekt për lëndën Bazat e të Dhënave, FIEK.

## Struktura
- skema.md : skema relacionale (burimi i së vërtetës)
- data/ : një CSV për tabelë (UTF-8, me header)
- faza1/ : algebra.md, fakte.dl, rregulla.dl, rezultatet.md
- sql/ : skriptat MySQL (Faza 2)

## Rregullat e punës
- Branch default: dev. Main është i mbrojtur.
- Çdo punë në branch feature/... dhe PR te dev.
- Çdo PR aprovohet nga lideri para bashkimit.
- Skema ndryshon vetëm me PR te skema.md.