# Informe de Reproducción y Verificación — Continuidad ChatGPT → Google Antigravity

- **Fecha de ejecución**: 2026-10-13
- **Run ID**: `20261013T215241Z`
- **Autor / Runtime**: Google Antigravity (sesión limpia, evaluador PMP)
- **Autoridad humana**: Max / Max Devs Solutions
- **Veredicto global**: **`PASS`** *(Recuperación documental PASS; Verificación offline PASS con LF restaurado; Continuidad productiva PENDIENTE)*

---

## 1. Objetivo y Alcance

Demostrar la recuperación de contexto y la continuidad operativa entre participantes de IA heterogéneos (específicamente la continuidad desde sesiones previas impulsadas por ChatGPT hacia Google Antigravity) basándose **exclusivamente en el repositorio Git** como medio de transporte y memoria operativa, sin intercambio de historiales de conversación, memoria oculta ni conocimiento previo del resultado.

- **Repositorio**: `https://github.com/Mad-Max8063/project-memory-protocol-public`
- **Rama objetivo evaluada**: `experiment/hermes-pmp-adapter`
- **Commit exacto (HEAD)**: `c974baf015b58e867e5fccb335a3c5df67d75089`
- **Mensaje de commit**: `docs: close other-machine evidence publication`
- **Rama de documentación**: `docs/antigravity-continuity-20261013`

---

## 2. Entorno de Ejecución y Herramientas Observadas

- **Sistema Operativo**: Microsoft Windows NT 10.0.26300.0 (Windows 11 Home, build 26300)
- **Intérprete Python**: Python 3.14.3
- **Cliente Git**: git version 2.53.0.windows.2
- **Directorio de evaluación**: `%USERPROFILE%\.gemini\antigravity\scratch\pmp-hermes-eval`
- **Directorio temporal aislado**: `%USERPROFILE%\.gemini\antigravity\scratch\pmp-review-tmp-6a6cb581` (configurado en `$env:TEMP` y `$env:TMP`, fuera del clon, sin enlaces ni junctions)
- **Herramientas de red/APIs**: Ninguna. Modo 100% offline. Cero dependencias externas o de terceros.

---

## 3. Estado y Decisiones Recuperadas Exclusivamente desde Git

A partir de la lectura estricta de `AGENTS.md`, `PROJECT_MEMORY.md`, `SPEC.md` y la evidencia archivada, se reconstruyó la siguiente realidad operativa sin pistas previas:

1. **Protocolo y Versión**: PMP Core `0.2.2` (normativo, estable, con Core R3 hardening merged en `main`), perfil `Evidence-backed Handoff` `0.1.1`.
2. **Naturaleza del Track**: La rama `experiment/hermes-pmp-adapter` contiene un puente de archivos experimental, opcional y `stdlib-only` para interoperabilidad con Hermes y otros runtimes. Las propuestas JSON son mero transporte no normativo.
3. **Decisiones Activas Relevantes**:
   - Mantener PMP vendor-neutral; Hermes, Claude y Codex son participantes externos del experimento, no dependencias del Core.
   - Reutilizar sin cambios el parser y validador de Core; no crear nuevos esquemas.
   - Separar estrictamente aserciones de productores, pruebas simuladas (mock) vs en vivo (live), verificación por el host y continuaciones independientes.
   - Mantener explícito el timeout de 300 s de Claude en la tarea de implementación como un handoff fallido/no validado.
   - Delimitación operativa de Hermes/Argon: restricción expresa de no acceder, modificar o depender del experimento anterior para mantener desacopladas herramientas externas (Argon, Obsidian, Jev, Cloudflare).
4. **Próxima Acción Canónica**: Max revisa la evidencia publicada de otra máquina en PR #8 y decide si cerrar el track o autorizar un nuevo experimento acotado (diferenciada explícitamente de la acción archivada del fixture devuelta por `verify_chain.py`).

---

## 4. Evidencia Realmente Verificada frente a Evidencia Solamente Documentada

En estricta conformidad con la sección 5.2 de `SPEC.md`, se establece la separación epistemológica:

| Elemento de Evidencia | Calificación | Justificación / Alcance |
| :--- | :---: | :--- |
| Commit `c974baf015b58e867e5fccb335a3c5df67d75089` | `[VERIFIED]` | Comprobado localmente con `git rev-parse HEAD`. |
| Estado de Git limpio | `[VERIFIED]` | Comprobado localmente con `git status --porcelain` (vacío). |
| Integridad de los 3 bundles de replay | `[VERIFIED]` | Hashes SHA-256 de `replay.bundle`, `claude-replay.bundle` y `fresh-codex.bundle` verificados byte a byte contra los valores fijados en `verify_chain.py`. |
| Integridad de inputs históricos (14 hashes) | `[VERIFIED]` | Verificados por `verify_chain.py` en los commits BASELINE y DISPATCH. |
| Ejecución de los 6 tests de fixture | `[VERIFIED]` | Ejecutados por `verify_chain.py` en subproceso aislado; 6/6 aprobados en 0.002 s. |
| Suite de 7 tests de aceptación de la cadena | `[VERIFIED]` | Ejecutados por `unittest`; 7/7 aprobados en 26.413 s (`OK`). |
| Ejecución pasada en vivo de Hermes (2026-10-06) | `[DOCUMENTED, HISTORICAL]` | Registrada en reportes y sesiones; la llamada al modelo no fue presenciada en esta sesión. |
| Ejecución pasada en vivo de Claude y Codex | `[DOCUMENTED, HISTORICAL]` | Registrada en reportes y sesiones; su evidencia está archivada pero la inferencia fue histórica. |
| Reproducciones same-host previas (Claude / Antigravity) | `[DOCUMENTED, HISTORICAL]` | Existen reportes versionados en el árbol; su ejecución corresponde a sesiones del 2026-10-06. |
| Reproducción en máquina ACER (2026-10-07) | `[DOCUMENTED]` | Evidencia documental provista por el maintainer; no observada directamente por este host. |
| GitHub Actions runs (`37495814502`, `37536055141`, `37711737829`) | `[DOCUMENTED]` | Asentados en memoria canónica; no consultados en vivo por red. |
| GitHub Draft PR #8 | `[DOCUMENTED]` | Asentado en memoria canónica y archivos de sesión. |

---

## 5. Comandos Ejecutados y Resultados Observados

### 5.1. Primera Ejecución: Detección del Fallo de Integridad LF/CRLF
Al ejecutar el verificador directamente sobre el clon de Windows configurado con `core.autocrlf=true`:
```powershell
python -B experiments/hermes-pmp/verify_chain.py --json
```
- **Código de salida**: `1`
- **Resultado**:
  ```json
  {"verified": false, "error": "archive digest mismatch: live-replay-20261006/replay-report.json"}
  ```
- **Suite de pruebas**:
  ```powershell
  python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
  ```
  - **Resultado**: `FAILED (failures=1, errors=1)` en 12.515 s.
  - Fallo en `test_real_archive_chain_and_readonly_boundary` por discrepancia de digest en `replay-report.json`.

### 5.2. Diagnóstico y Recuperación de `core.autocrlf`
1. **Diagnóstico**: `verify_chain.py` lee bytes crudos (`path.read_bytes()`) para verificar hashes SHA-256 inmutables. Git en Windows tradujo los bytes `\n` a `\r\n` en los archivos `.json` de texto al hacer checkout, cambiando el hash en disco de `ade854...` a `7a4e48...`. Los bundles binarios no sufrieron alteración.
2. **Recuperación**: Se aplicó la directiva oficial del proyecto (`git config core.autocrlf false`) y se restauraron los archivos de evidencia para coincidir con los bytes LF de los blobs de Git. El working tree se mantuvo limpio (`git status --porcelain` vacío).

### 5.3. Segunda Ejecución: Verificación Exitosa
```powershell
python -B experiments/hermes-pmp/verify_chain.py --json
```
- **Código de salida**: `0`
- **Resultado JSON**:
  - `verified`: `true`
  - `historical_inputs`: `14`
  - `acceptance_tests`: `6` (Ran 6 tests in 0.002s, `OK`)
  - `final_commit`: `5e717267e23e39a854347ade7e9efa545269c227`
  - `bundle_sha256`: 3 digests coincidentes al 100%.

```powershell
python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
```
- **Código de salida**: `0`
- **Resultado**: `Ran 7 tests in 26.413s` -> **`OK`** (7/7 tests aprobados).

```powershell
python -B -m unittest discover -s tests
```
- **Código de salida**: `0` (con `core.autocrlf=false`)
- **Resultado**: `Ran 83 tests in 38.099s` -> **`OK`** (83/83 tests aprobados).  
  *Nota técnica*: En un checkout afectado por CRLF en Windows, la suite completa arroja 1 fallo (`test_state_serialization_preserves_canonical_bytes_and_sections` en `test_hermes_pmp_adapter.py`) debido a la presencia de `\r` al parsear `seed/PROJECT_MEMORY.md`. Con `core.autocrlf=false`, los 83 tests pasan exitosamente sin alterar código.

---

## 6. Limitaciones de la Evidencia

1. **Identidad de los Modelos**: Los metadatos de Git y reportes JSON confirman consistencia de datos, pero **no proveen prueba criptográfica** de que los modelos que generaron las propuestas históricas fueran efectivamente GPT-5.6-Luna, Claude 3.5 Sonnet u OpenAI Codex (`model_identity_certified: false`).
2. **Frescura de Sesión y Memoria Oculta**: No puede demostrarse criptográficamente la ausencia de memoria previa o caché en los proveedores externos (`session_freshness_certified: false`). Solo se demuestra la portabilidad del contexto a través del repositorio y la ausencia de turnos heredados formalmente declarada.
3. **Independencia de la Evaluación**: Esta evaluación fue ejecutada en la estación de trabajo local con intervención del maintainer humano (Max), no por un evaluador u organización tercera externa e independiente.
4. **Portabilidad de Plataforma**: Las ejecuciones se realizaron en Windows 11. Aunque el código emplea Python estándar y se han documentado instrucciones POSIX, no se ha ejecutado una verificación directa en Linux o macOS en esta sesión.

---

## 7. Costos Incurridos

- **Costo incremental directo**: **USD 0.00**
- No se invocaron APIs de pago, suscripciones de modelos ni servicios externos.
- La facturación o consumo de cuotas de herramientas de sesiones anteriores no fue auditada.

---

## 8. Hallazgo Técnico y Propuesta de Mejora Pendiente

El comportamiento observado respecto a los saltos de línea LF/CRLF en Windows fue documentado en detalle en [`crlf-issue-proposal.md`](crlf-issue-proposal.md). Se propone incorporar `.gitattributes` en el repositorio para blindar los archivos `.json` con `text eol=lf`, evitando fallos silenciosos por configuraciones predeterminadas de Git en Windows. Dicha propuesta permanece pendiente de autorización humana, sin modificar el código actual.

---

## 9. Veredicto Final

- **Recuperación Documental**: **`PASS`**  
  Contexto, estado, decisiones, restricciones y próxima acción canónica recuperados de manera consistente con la evidencia del repositorio Git.
- **Verificación Offline**: **`PASS`**  
  3 bundles, 14 inputs históricos, 6 tests de fixture y 7 tests de aceptación verificados determinísticamente tras garantizar los bytes LF originales.
- **Continuidad Productiva**: **`PENDIENTE`**  
  Resta demostrar la continuidad productiva entre proveedores ejecutando una tarea de desarrollo o ingeniería real, nueva e independiente.
