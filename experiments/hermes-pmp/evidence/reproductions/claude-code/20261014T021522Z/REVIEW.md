# PMP — Revisión independiente del handoff productivo (fix de fines de línea en Windows)

- Revisor: Claude Code (Opus 5.5), participante lógico, sin atestación de identidad
- Fecha: 2026-10-13
- Implementación revisada: Google Antigravity
- Rama: `experiment/pmp-windows-line-endings-20261013` (local, **no publicada**)
- Commit revisado: `dbb55f5c9dbfab15bdc708d160d5285a41ca2435` (confirmado)
- Padre: `224a67fd9cac0d5d5b257f15b2c27232b3eaa7fa` (está en `origin/docs/antigravity-continuity-20261013`)
- Evidencia usada: solo el repo, Git, `AGENTS.md`, `PROJECT_MEMORY.md` y archivos versionados. No usé conversaciones previas.

## Veredicto: **PASS** (con observaciones que no bloquean)

El `.gitattributes` resuelve el fallo original en clones nuevos, con `core.autocrlf=true` y con `false`. Las dos configuraciones dan árboles de trabajo byte a byte idénticos, y todos los gates pasan: memoria, release, verificador offline, 7 tests de aceptación y 87 tests en total. El control (el commit padre con `autocrlf=true`) reproduce el fallo original. El fix toca solo 4 archivos: no cambia el Core 0.2.2, los profiles, los scripts, los adapters, los bundles ni `experiments/`.

## 1. Estado reconstruido desde PMP (sin chat)

| Ítem | Reconstrucción | Verificado |
|---|---|---|
| Problema original | Windows trae `core.autocrlf=true` a nivel sistema, así que los JSON y Markdown de evidencia se descargan con CRLF. El SHA-256 de `live-replay-20261006/replay-report.json` deja de coincidir (`verify_chain.py` sale con 1). Además, el regex del adapter captura `hermes-pmp-fixture\r`. | Sí, lo reproduje en el control (ver §4) |
| Decisión | Active decision #11: `* text=auto eol=lf` + `*.bundle binary`, sin aflojar las verificaciones criptográficas ni tocar el Core ni los bundles | Sí |
| Archivos cambiados | `.gitattributes`, `tests/test_line_endings_regression.py`, `.project-memory/sessions/windows-line-endings-fix.md`, `PROJECT_MEMORY.md` | Sí (`git diff --stat 224a67f HEAD`: 4 archivos, +144/−8) |
| Evidencia | La sesión `windows-line-endings-fix.md` y los informes de Antigravity del 20261013T215241Z. Los 61 paths locales que figuran en `## Evidence` existen. | Sí |
| Restricciones vigentes | USD 0. No cambiar el Core, la spec ni los profiles. No mergear, taggear, releasear ni postear. No tocar el experimento Hermes/Argon bloqueado. La rama y el PR externo ya estaban autorizados (para la rama anterior). | Sí |
| Próxima acción autorizada | Que Claude Code haga una verificación independiente desde un checkout limpio con `autocrlf` en true y en false, con verificador, aceptación, suite completa (87) y validadores. **Sin push, sin merge y sin tocar el PR #8.** | Es esta revisión |

## 2. Entorno

- Windows 11 Home 10.0.26300, Git 2.53.0.windows.2, Python 3.14.3
- `core.autocrlf=true` a nivel **sistema** (`C:/Program Files/Git/etc/gitconfig`), sin override global
- Repo fuente `%USERPROFILE%\.gemini\antigravity\scratch\pmp-hermes-eval`: no lo modifiqué (solo hice lecturas y `clone --no-local` desde él)
- Clones descartables en `%USERPROFILE%\pmp-rev-claude-20261013\`, un directorio nuevo con ruta corta. El primer intento en el scratchpad falló con `Filename too long`, que es justo el problema de rutas largas que ya menciona el brief.

## 3. Checkouts independientes

| Clon | Config | HEAD | Archivos CRLF (sin contar bundles) | `git ls-files --eol` (worktree) |
|---|---|---|---|---|
| `crlf-true` | `autocrlf=true` | dbb55f5 | **0** | 129 lf, 3 none, 5 -text |
| `crlf-false` | `autocrlf=false` | dbb55f5 | **0** | 129 lf, 3 none, 5 -text |
| `control-parent` | `autocrlf=true`, clon `--no-checkout` + checkout del padre | 224a67f | **126** | 126 crlf, 3 none, 5 -text |

- `diff -rq --exclude=.git crlf-true crlf-false` → **sin diferencias** (byte a byte idénticos).
- En el índice, todos los blobs ya eran LF (129 `i/lf`) y no hay ningún blob con CRLF. Por eso el `.gitattributes` **no provoca renormalización ni diffs fantasma**: `git status` queda limpio en todos los clones, antes y después de correr todo.
- Nota de método: un primer control (clon en HEAD + checkout del padre) no servía, porque Git solo reescribe los archivos que cambian entre commits y quedaba 1 solo archivo CRLF. Lo descarté (`control-parent-INVALID`) y lo rehíce sin checkout previo.

## 4. Resultados de ejecución

| Gate | `crlf-true` | `crlf-false` | `control-parent` (sin fix) |
|---|---|---|---|
| `python -B scripts/validate_memory.py PROJECT_MEMORY.md` | rc 0, VALID | rc 0, VALID | rc 0 |
| `python -B scripts/validate_release_candidate.py .` | rc 0, "Core 0.2.2; profile 0.1.1; links, size, and secrets passed" | rc 0, igual | rc 0 |
| `python -B experiments/hermes-pmp/verify_chain.py --json` | rc 0, `verified: true`, 3 bundles, 14 inputs, 6 tests de fixture, `test_exit_code 0` | rc 0, igual | **rc 1**, `archive digest mismatch: live-replay-20261006/replay-report.json` |
| `unittest … -p test_pmp_replay_chain.py` | 7 tests OK (23.264 s) | 7 tests OK (23.244 s) | **FAILED** (1 failure, 1 error) |
| `unittest … -p test_line_endings_regression.py` | 4 OK | 4 OK | (no existe en el padre) |
| `unittest discover -s tests` | **87 OK** (28.968 s) | **87 OK** (28.972 s) | **83, FAILED** (2 failures, 1 error) |

Los fallos del control coinciden exactamente con los que documentó Antigravity: `archive digest mismatch`, `'hermes-pmp-fixture\r' != 'hermes-pmp-fixture'` y la salida del CLI con 1.

SHA-256 de los bundles que reporta el verificador (iguales en los dos clones):
- `live-replay-20261006/replay.bundle` `b729b7f2…8de17`
- `claude-continuation-20261006/claude-replay.bundle` `b9c7e80b…1e03ec`
- `claude-continuation-20261006/fresh-codex.bundle` `1a5eb32b…24b25`

Integridad del resto del repo: `git diff --name-only 224a67f HEAD -- SPEC.md profiles scripts adapters templates '*.bundle' experiments` da vacío.

## 5. Revisión crítica de los cuatro tests

Hice una prueba de mutación: copié el archivo de tests nuevo en una copia descartable del control (sin `.gitattributes`, worktree con CRLF).

| Test | Sin el fix | Juicio |
|---|---|---|
| `test_gitattributes_configuration_exists_and_enforces_lf` | FAIL | Útil como guarda de configuración. Solo busca la cadena (no interpreta atributos), pero alcanza. |
| `test_evidence_json_files_have_no_crlf` | FAIL | Es la regresión real: cubre el archivo que falló. Solo detecta el problema si el checkout se hizo con `autocrlf=true`; con `false` pasa igual (por eso hace falta el test 1). |
| `test_seed_files_have_no_crlf` | FAIL | Cubre el fallo del adapter (`\r` en el seed). Si `seed/` o `claude-seed/` desaparecen, pasa en vacío (`if seed_dir.is_dir()`); hoy los dos existen, con 6 archivos. |
| `test_crlf_injection_fails_digest_before_subprocess` | **ok** | **No prueba el fix.** Confirma que `verify_chain` rechaza un digest alterado antes del subprocess (sirve como test del verificador), pero pasa con o sin `.gitattributes`. La sesión lo presenta como test de regresión del fix: es un error de rótulo, no un defecto. |

Detalles de estilo (no cambian el resultado): `import json` no se usa, e `import sys` aparece después de armar `sys_path`.

## 6. Efectos secundarios de `* text=auto eol=lf`

| Aspecto | Resultado |
|---|---|
| Churn o diffs fantasma en archivos existentes | Ninguno: todos los blobs ya eran LF |
| Binarios | Los únicos binarios son los 5 `.bundle`, marcados como `binary` (`-text`). Git ya los detectaba como binarios, así que esa regla es un seguro extra. |
| `.ps1` en LF | `windows-runtime.ps1` sale en LF. PowerShell lo ejecuta igual, no hace falta excepción. |
| `.bat`/`.cmd` (necesitan CRLF) | No hay ninguno. Si se suma alguno, va a hacer falta `*.bat text eol=crlf` / `*.cmd text eol=crlf`. |
| `git archive` (entrega en ZIP) | 0 entradas con CRLF de 177: el fix también mejora el paquete portable |
| Clones internos de bundles | `verify_chain.py` ya fuerza `-c core.autocrlf=false` al clonar bundles (líneas 51–52 y 242), así que es coherente con el fix |
| **Worktrees viejos que avanzan a este commit** | **Gap.** Copié el control (CRLF) e hice `git checkout dbb55f5`: quedaron 125 archivos CRLF, `git status` **limpio** (incluso después de `update-index --really-refresh`) y el verificador **sigue fallando** con el mismo digest mismatch. Se arregla rehaciendo el checkout: `rm .git/index && git checkout HEAD -- .` → 129 lf, status limpio, `verified: true`. Es un comportamiento normal de Git (solo reescribe lo que cambió), pero ni la memoria ni la sesión lo mencionan. Quien tenga un clon previo con `autocrlf=true` (por ejemplo, las reproducciones de Antigravity) va a ver el mismo fallo sin ninguna pista. |
| SHAs históricos fijados en la documentación (c974baf, 1f56483, `experiment/hermes-pmp-adapter`) | No tienen `.gitattributes`, así que siguen necesitando `core.autocrlf=false`. El brief ya usa `--config core.autocrlf=false` y tiene que quedar así. |

## 7. Posibles defectos y riesgos (por severidad)

1. **(Media, documentación)** No hay nota de migración para worktrees existentes con CRLF: el fallo sigue y `git status` no avisa. Lo aconsejable es agregar una línea a la memoria o al brief con el remedio (`rm .git/index && git checkout HEAD -- .`, o volver a clonar).
2. **(Baja)** El test 4 aparece como regresión del fix, pero no depende de él (lo confirmé por mutación). Convendría cambiarle el rótulo en la sesión o la memoria, o sacarlo del conteo de "regresión".
3. **(Baja)** El test 3 puede pasar en vacío si se renombran los directorios de seeds.
4. **(Baja, a futuro)** Los binarios nuevos dependen de la autodetección de `text=auto`, y los `.bat`/`.cmd` van a necesitar excepción CRLF si se agregan.
5. **(Info)** La primera viñeta de la memoria marca como `[VERIFIED]` resultados que verificó el mismo implementador. Esta revisión los confirma de forma independiente en esta máquina, pero es el mismo host Windows, no una reproducción externa.

## 8. Limitaciones

- Mismo host para la implementación y la revisión. No es una reproducción en otra máquina ni por otra persona.
- No hice `git fetch`: lo que digo sobre el remoto sale de los refs de seguimiento locales (la cabeza de PR #8 estaría en `c974baf` y el padre `224a67f` en `origin/docs/antigravity-continuity-20261013`). Pueden estar desactualizados. Con `ls-remote` confirmé que esta rama no existe en `origin`.
- No probé Linux/macOS ni otras versiones de Git.
- Los tiempos por comando no quedaron registrados (faltaba `bc`). Uso los tiempos que reporta `unittest`.
- No modifiqué código ni tests del repo revisado. Las copias mutadas (`mut-no-attr`, `upgrade`) son descartables, fuera del clon de revisión, y no se commitearon.

## 9. Recomendación

**Publicable.** Las correcciones de la §7 son de documentación y rótulo, y pueden ir en un commit de seguimiento antes o después de publicar.

Próximo paso exacto (no lo ejecuté; necesita la autorización de Max, porque la memoria vigente prohíbe el push en este handoff):

```bash
git -C "/.gemini/antigravity/scratch/pmp-hermes-eval" push origin experiment/pmp-windows-line-endings-20261013
```

Publica la rama como rama **nueva** del remoto. No toca el PR #8 ni `main`. Antes, si Max quiere, se puede sumar en esa rama un commit con la nota de migración (§7.1) y el cambio de rótulo del test 4 (§7.2), más la actualización de la memoria con esta revisión.

## Rastro

- Logs completos: `%USERPROFILE%\pmp-rev-claude-20261013\logs\{crlf-true,crlf-false,control-parent}\*.out`
- Script de la batería: `%USERPROFILE%\pmp-rev-claude-20261013\battery.sh`
- Clones: `main` (revisión), `crlf-true`, `crlf-false`, `control-parent`, `control-parent-INVALID`, `mut-no-attr`, `upgrade`. Todos descartables.
