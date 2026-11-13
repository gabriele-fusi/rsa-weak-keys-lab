# Risultati grezzi del laboratorio

Ambiente: Python 3.13.18, RsaCtfTool 0.1.0 (commit 4ffadb0, 2026-10-23), gmpy2 2.3.2,
venv isolato, macchina cloud condivisa (CPU single-thread per il timing, nessuna GPU).

## Esperimento 1 — Fermat (primi vicini, RSA-1024)
Comando: `RsaCtfTool --publickey keys/fermat.pub --attack fermat --private`
Esito: SUCCESSO — chiave privata recuperata
Tempo reale: 0.860s (user 0.252s)

## Esperimento 2 — Wiener (esponente privato piccolo, RSA-1024)
Comando: `RsaCtfTool --publickey keys/wiener.pub --attack wiener --private`
Esito: SUCCESSO — chiave privata recuperata
Tempo reale: 0.218s (user 0.195s)

## Esperimento 3 — Common factors (due chiavi, stesso primo p, RSA-1024 ciascuna)
Comando: `RsaCtfTool --publickey "keys/commonfactor_a.pub,keys/commonfactor_b.pub" --attack common_factors --private`
Esito: SUCCESSO — entrambe le chiavi private recuperate
Tempo reale: 0.227s

## Esperimento 4 — Chiave di controllo (RSA-2048, generata correttamente)
Comando: `RsaCtfTool --publickey keys/control.pub --attack fermat wiener pollard_rho pollard_p_1 williams_pp1 roca --private --timeout 20`
Esito: FALLIMENTO per tutti gli attacchi (atteso)
- fermat: timeout dopo 20.0s
- pollard_p_1: timeout dopo 17.7s (si ferma da solo prima del timeout pieno)
- wiener: fallito istantaneamente (0.0007s) — d non è piccolo
- pollard_rho: timeout dopo 20.0s
- roca: non eseguito (richiede SageMath, non installato in questo ambiente)
- williams_pp1: timeout dopo 20.0s
Tempo totale: 1m17.98s per 5 attacchi

## Tabella riassuntiva

| Attacco      | Chiave target      | Bit  | Difetto introdotto                  | Esito    | Tempo   |
|--------------|---------------------|------|--------------------------------------|----------|---------|
| Fermat       | fermat.pub          | 1024 | p e q troppo vicini                  | Rotta    | 0.86s   |
| Wiener       | wiener.pub          | 1024 | esponente privato d troppo piccolo   | Rotta    | 0.22s   |
| Common factors | commonfactor_{a,b}.pub | 1024 | due chiavi condividono lo stesso p | Rotte (entrambe) | 0.23s |
| Controllo (5 attacchi) | control.pub | 2048 | nessuno (RSA-2048 standard)         | Resistita | 78.0s (timeout su tutti) |

Nota: i tempi assoluti dipendono dalla CPU della macchina usata; il punto dell'esperimento
è il confronto relativo (frazioni di secondo contro timeout) e la riproducibilità con lo
script fornito, non il numero esatto di millisecondi.

## Verifica di riproducibilità (seconda esecuzione, da zero)

Rieseguito l'intero `scripts/run_lab.sh` con chiavi rigenerate da capo:
- Fermat: successo in 0.271s
- Wiener: successo in 0.237s
- Common factors: successo in 0.221s
- Controllo (5 attacchi): fallimento su tutti, 1m18.377s totali

Stesso esito qualitativo della prima run (tutti gli attacchi deboli sotto il secondo,
il controllo resiste), con tempi assoluti leggermente diversi per via delle chiavi
casuali diverse e del carico della macchina condivisa — coerente con quanto scritto
nell'articolo.
