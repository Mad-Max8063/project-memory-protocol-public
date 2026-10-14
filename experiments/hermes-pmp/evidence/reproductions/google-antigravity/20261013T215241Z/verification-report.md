# EVALUACIÓN Y VERIFICACIÓN OFFLINE DE PROJECT MEMORY PROTOCOL (PMP)
**Fase 2: Ejecución, Verificación de Evidencia Archivada y Calificación Epistemológica**

- **Fecha de evaluación**: 2026-10-13
- **Evaluador / Runtime**: Google Antigravity (sesión limpia, modo receptor PMP)
- **Veredicto global**: **`PASS`** *(con observaciones técnicas documentadas sobre `core.autocrlf` en Windows)*
- **Costo incremental**: **USD 0** (100% offline, sin APIs pagas, sin invocaciones de inferencia en vivo, sin dependencias instaladas)

---

## 1. Confirmación de Estado del Clon y Análisis de Seguridad Previo

### 1.1. Estado de Git y HEAD
- **Commit HEAD**: `c974baf015b58e867e5fccb335a3c5df67d75089` `[VERIFIED]`
- **Mensaje**: `docs: close other-machine evidence publication`
- **Estado de working tree**: Limpio (`git status --porcelain` retorna vacío) `[VERIFIED]`

### 1.2. Análisis de Seguridad Previo de `experiments/hermes-pmp/verify_chain.py`
Antes de cualquier ejecución, se auditó exhaustivamente el código fuente del verificador:
- **Dependencias**: Utiliza exclusivamente la librería estándar de Python (`argparse`, `json`, `pathlib`, `re`, `subprocess`, `sys`, `tempfile`). Cero paquetes de terceros `[VERIFIED]`.
- **Aislamiento de red**: No realiza sockets, llamadas HTTP ni conexiones remotas. Opera en modo 100% local `[VERIFIED]`.
- **Entorno seguro (`clean_env`)**: Limpia variables de entorno y no lee credenciales, tokens ni claves de proveedores `[VERIFIED]`.
- **Protección de Git**: Ejecuta comandos con `-c safe.directory`, `-c core.autocrlf=false` y redirige `core.hooksPath` a un directorio vacío para evitar inyección de ganchos `[VERIFIED]`.
- **Validación de rutas y symlinks (`unlinked_root`)**: Valida que ni la raíz de evidencia ni sus ancestros sean symlinks o junctions de Windows para evitar desvíos fuera del árbol previsto `[VERIFIED]`.
- **Ejecución acotada de tests**: Ejecuta subprocesos con timeout de 30s mediante `sys.executable -I -B -c ...` cargando únicamente los módulos de test fijos y confiables (`test_fixture.py`, `test_manifest.py`), sin descubrimiento dinámico arbitrario `[VERIFIED]`.
- **Conclusión de seguridad**: Seguro para ejecución local sin riesgo de efectos colaterales.

### 1.3. Aislamiento de Entorno Temporal
Se configuró un directorio temporal externo e independiente fuera del árbol del clon:
- Ruta configurada: `scratch\pmp-review-tmp-<guid>`
- Asignado a: `$env:TEMP` y `$env:TMP` `[VERIFIED]`

---

## 2. Comandos Ejecutados, Códigos de Salida y Resultados Observados

### 2.1. Hallazgo Técnico Inicial: Discrepancia por `core.autocrlf` en Windows
En la primera corrida con el clon predeterminado de Windows:
- **Comando**: `python -B experiments/hermes-pmp/verify_chain.py --json`
- **Código de salida**: `1`
- **Salida**: `{"verified": false, "error": "archive digest mismatch: live-replay-20261006/replay-report.json"}`
- **Análisis de causa raíz**:
  El script `verify_chain.py` lee los archivos de evidencia en crudo con `read_bytes()` y calcula el hash criptográfico SHA-256 directo. En Windows, si el clon se realiza sin `--config core.autocrlf=false`, Git traduce los saltos de línea de los archivos de texto (`.json`) de LF (`\n`) a CRLF (`\r\n`).
  - Hash obtenido en disco (CRLF): `7a4e48c07877982bb7826d2420b8fa065c6a46c7c8dacdc47ef46d7e18177951`
  - Hash esperado fijado (LF original): `ade8546d585305fdccbb3061da91898e5a3ab991b8178815106faa36de134c7d`
  Los archivos `.bundle` (binarios) no sufrieron alteración y sus digests coincidieron con los valores fijados.
- **Resolución**:
  Tal como lo especifica taxativamente la documentación oficial en `docs/experiments/hermes-review-brief.md` (línea 76), en Windows es mandatorio operar con `core.autocrlf=false`. Al restaurar los archivos de evidencia para reflejar exactamente los bytes LF de los blobs de Git, el árbol de trabajo se mantuvo limpio (`git status --porcelain` vacío) y se procedió a la verificación formal.

---

### 2.2. Ejecución Formal del Verificador de Cadena (`verify_chain.py`)
- **Comando exacto**:
  ```powershell
  python -B experiments/hermes-pmp/verify_chain.py --json
  ```
- **Código de salida**: `0` `[VERIFIED]`
- **Salida stdout (JSON)**:
  ```json
  {
    "verified": true,
    "historical_inputs": 14,
    "acceptance_tests": 6,
    "next_action": "Max / dispatch host: review .project-memory/sessions/codex-after-claude.md and this canonical update, then close the bounded experiment. No implementation action remains; any further experiment requires a new scoped task.",
    "final_commit": "5e717267e23e39a854347ade7e9efa545269c227",
    "model_identity_certified": false,
    "session_freshness_certified": false,
    "test_command": [
      "python",
      "-I",
      "-B",
      "-c",
      "import os,sys,unittest; sys.path.insert(0,os.getcwd()); suite=unittest.defaultTestLoader.loadTestsFromNames([\"test_fixture\",\"test_manifest\"]); result=unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(0 if result.wasSuccessful() else 1)"
    ],
    "test_exit_code": 0,
    "test_stdout": "",
    "test_stderr": "test_normalized_labels (test_fixture.FixtureTests.test_normalized_labels) ... ok\ntest_shape_and_ids (test_fixture.FixtureTests.test_shape_and_ids) ... ok\ntest_whitespace_contract (test_fixture.FixtureTests.test_whitespace_contract) ... ok\ntest_manifest_has_no_blank_lines (test_manifest.ManifestTests.test_manifest_has_no_blank_lines) ... ok\ntest_manifest_has_two_distinct_ids (test_manifest.ManifestTests.test_manifest_has_two_distinct_ids) ... ok\ntest_manifest_matches_fixture_in_order (test_manifest.ManifestTests.test_manifest_matches_fixture_in_order) ... ok\n\n----------------------------------------------------------------------\nRan 6 tests in 0.002s\n\nOK\n",
    "bundle_sha256": {
      "live-replay-20261006/replay.bundle": "b729b7f2220f5e639ad9e43f205314c45055d69eab966689b0438f178398de17",
      "claude-continuation-20261006/claude-replay.bundle": "b9c7e80bdd3c25a4aca67c43dd647fa3325f4340a9f51de5bbc7a61b9f1e03ec",
      "claude-continuation-20261006/fresh-codex.bundle": "1a5eb32bc3cc3c240be4a0533d110d86adf7291240628defc6f9109b45324b25"
    },
    "scope": "fixed archived chain; offline integrity and local test verification"
  }
  ```
- **Salida stderr**: *(vacía)*

---

### 2.3. Ejecución Formal de la Suite de Aceptación del Verificador
- **Comando exacto**:
  ```powershell
  python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
  ```
- **Código de salida**: `0` `[VERIFIED]`
- **Salida stdout/stderr**:
  ```text
  test_cli_json_usage_and_failure_exit_codes (test_pmp_replay_chain.ChainAcceptanceTests.test_cli_json_usage_and_failure_exit_codes) ... ok
  test_corrupted_bundle_rejected_before_git (test_pmp_replay_chain.ChainAcceptanceTests.test_corrupted_bundle_rejected_before_git) ... ok
  test_ignored_import_payload_rejected_without_execution (test_pmp_replay_chain.ChainAcceptanceTests.test_ignored_import_payload_rejected_without_execution) ... ok
  test_missing_archive_and_linked_inputs_rejected (test_pmp_replay_chain.ChainAcceptanceTests.test_missing_archive_and_linked_inputs_rejected) ... ok
  test_modified_report_rejected_before_git (test_pmp_replay_chain.ChainAcceptanceTests.test_modified_report_rejected_before_git) ... ok
  test_real_archive_chain_and_readonly_boundary (test_pmp_replay_chain.ChainAcceptanceTests.test_real_archive_chain_and_readonly_boundary) ... ok
  test_semantic_verifier_rejects_changed_result_and_missing_handoff (test_pmp_replay_chain.ChainAcceptanceTests.test_semantic_verifier_rejects_changed_result_and_missing_handoff) ... ok

  ----------------------------------------------------------------------
  Ran 7 tests in 26.413s

  OK
  ```

---

## 3. Comparación con el Informe de Reconstrucción Inicial

| Elemento Reconstruido | Previsión Fase 1 | Resultado Observado Fase 2 | Estado |
| :--- | :--- | :--- | :---: |
| **Commit HEAD** | `c974baf015b58e867e5fccb335a3c5df67d75089` | `c974baf015b58e867e5fccb335a3c5df67d75089` | **Coincide** |
| **Estado Git** | Working tree limpio | `git status --porcelain` limpio antes y después | **Coincide** |
| **Digest de Bundles** | 3 bundles archivados coincidentes | 3 bundles validados contra SHA-256 fijados | **Coincide** |
| **Inputs Históricos** | 14 hashes verificados | 14 hashes verificados en commit BASELINE y DISPATCH | **Coincide** |
| **Tests de Fixture** | 6 tests unitarios deterministas | 6 tests pasaron en 0.002s (exit code 0) | **Coincide** |
| **Tests de Verificador**| 7 tests de aceptación | 7 tests pasaron en 26.413s (`OK`, exit code 0) | **Coincide** |
| **Next Action Archivada** | Acción del fixture en `5e717267` | Exactamente la recuperada en el JSON del verificador | **Coincide** |
| **Sensibilidad a CRLF** | No enfatizada en Fase 1 | Causa directa de fallo de digest si `autocrlf=true` | **Descubrimiento Técnico** |

---

## 4. Correcciones Epistemológicas y Normativas Obligatorias

### 4.1. Corrección de Afirmaciones Históricas Indebidamente Marcadas como `[VERIFIED]`
En la Fase 1, se etiquetaron de forma inexacta ciertos hitos históricos como `[VERIFIED]` basándose en su lectura documental de `PROJECT_MEMORY.md`. 

De acuerdo con la sección 5.2 de `SPEC.md`, la etiqueta `[VERIFIED]` aplica **única y exclusivamente** a lo comprobado contra evidencia empírica durante la sesión y timestamp actual. En consecuencia, se corrigen formalmente las siguientes clasificaciones:

1. **La ejecución real de Hermes en vivo (2026-10-06)**:  
   - *Corrección*: Es **`[DOCUMENTED, HISTORICAL]`**, NO `[VERIFIED]` por esta sesión. Lo que en esta sesión es `[VERIFIED]` es la **integridad criptográfica y offline del bundle y reporte archivados** (`evidence/live-replay-20261006/replay.bundle`).
2. **La continuación de Claude Code (Sonnet 5) y Codex (2026-10-06)**:  
   - *Corrección*: Es **`[DOCUMENTED, HISTORICAL]`**. Se comprueba que los commits en los bundles existen y sus tests pasan (`[VERIFIED]`), pero la llamada al modelo no fue presenciada en esta sesión.
3. **Las reproducciones same-host de Claude Code y Google Antigravity**:  
   - *Corrección*: Son **`[DOCUMENTED, HISTORICAL]`**; existen archivos de reporte versionados en el repositorio (`[VERIFIED]`), pero su ejecución pasada es un registro documental.
4. **La reproducción en la máquina ACER (2026-10-07)**:  
   - *Corrección*: Permanece como **`[DOCUMENTED]`**; es un reporte de consola transcripto por el maintainer, no una ejecución observada por el host.

### 4.2. Corrección sobre el Bloqueo de Hermes/Argon
- *Error en Fase 1*: Se describió como *"bloqueado y descartado definitivamente"* o *"bloqueo permanente del protocolo"*.
- *Corrección*:  
  La restricción en `PROJECT_MEMORY.md` establece textualmente:  
  *`- Do not access, modify, reactivate, repair or depend on the blocked previous Hermes/Argon experiment. No Argon, Obsidian, Jev or Cloudflare dependency.`*  
  Se trata de una **restricción operativa y exclusión de alcance específica para este track/rama**, diseñada para evitar arrastrar complejidad o dependencias bloqueadas (Argon, Obsidian, Jev, Cloudflare). No es una declaración ontológica ni una prohibición dogmática permanente de la especificación PMP, sino una delimitación pragmática de ingeniería para mantener el adaptador actual minimal, desacoplado y basado solo en la librería estándar.

---

## 5. Límites de la Evidencia y Distinciones Críticas

Para mantener el rigor de evaluación, se establecen tres niveles de certeza independientes:

1. **Recuperación de contexto vía Git**: **DEMOSTRADA / `[VERIFIED]`**  
   Un agente receptor sin historial previo de chat ni conocimiento adelantado puede leer `AGENTS.md`, `PROJECT_MEMORY.md` y la evidencia del repo, reconstruyendo con total precisión el estado del proyecto, decisiones, restricciones, prioridades y la próxima acción canónica.
2. **Verificación de evidencia archivada**: **DEMOSTRADA / `[VERIFIED]`**  
   Los bundles de Git, árboles de commits, propuestas JSON y tests de fixture se verifican offline de manera determinista, comprobando la inmutabilidad y coherencia de los artefactos generados.
3. **Identidad real y frescura de sesión de los modelos**: **NO CERTIFICADA / `[ASSUMED]`**  
   Git y los hashes SHA-256 **no proveen prueba criptográfica de identidad de agentes** (no demuestran si fue Hermes, Claude, Codex o un script local simulado), ni garantizan la ausencia de memoria privada o caché en los proveedores externos. Esta limitación está explícitamente codificada en el protocolo (`model_identity_certified: false`, `session_freshness_certified: false`).

---

## 6. Confirmación de Cierre de Git
- **Commit actual**: `c974baf015b58e867e5fccb335a3c5df67d75089` `[VERIFIED]`
- **Comprobación final**: `git status --porcelain` retorna vacío `[VERIFIED]`
- **Integridad**: No se modificaron archivos versionados, no se agregaron archivos no trackeados al repositorio y no se alteró la memoria canónica.

---

## 7. Veredicto Final

# `PASS`

La evidencia archivada coincide con la memoria canónica del repositorio. La verificación offline es reproducible y determinista a costo incremental USD 0, sujeta a la configuración de `core.autocrlf=false` en plataformas Windows.
