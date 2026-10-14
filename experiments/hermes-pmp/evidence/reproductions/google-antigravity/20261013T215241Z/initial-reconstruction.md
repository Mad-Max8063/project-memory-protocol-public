# INFORME DE RECONSTRUCCIÓN INICIAL — PMP (Project Memory Protocol)
**Sesión de Evaluación / Test de Lectura y Reconstrucción Contextual**
**Fecha**: 2026-10-13  
**Agente**: Receptor PMP (Google Antigravity en sesión limpia)  
**Origen de datos**: Clon local independiente y exclusivo desde Git (`experiment/hermes-pmp-adapter`)

---

## 1. URL, rama, commit exacto y diferencias de alcance

### Identificadores y estado del clon
- **URL remota**: `https://github.com/Mad-Max8063/project-memory-protocol-public` `[VERIFIED]`
- **Rama objetivo**: `experiment/hermes-pmp-adapter` `[VERIFIED]`
- **Commit exacto (HEAD)**: `c974baf015b58e867e5fccb335a3c5df67d75089` `[VERIFIED]`
  - Mensaje: `docs: close other-machine evidence publication`
  - Autor: `Matías Maximiliano Bernal <179927943+Mad-Max8063@users.noreply.github.com>`
  - Fecha: `Wed Oct 7 22:13:11 2026 -0300`
- **Estado del working tree**: Limpio (`git status --porcelain` retorna vacío) `[VERIFIED]`

### Diferencias de alcance entre ramas y replay
1. **Rama `main` (`origin/main` en commit `2d9da5549d802c27b7a47293384d3f0d59b0ff13`)**: `[VERIFIED]`
   - Núcleo normativo público y estable de PMP v`0.2.2` (con Core R3 hardening merged vía PR #1 y cierres en PR #2, #3, #4, #5).
   - Perfil `Evidence-backed Handoff` v`0.1.1`.
   - Tag anotado publicado: `v0.2.2` (peels a `0597ac7fd428e5c693d50caffb8686f8319b9fa4`).
   - GitHub Release pública `386759221` (Latest).
   - Propuesta exploratoria no normativa: `Capability-Aware Handoff` (`docs/proposals/CAPABILITY_AWARE_HANDOFF.md`).
   - No contiene código del adaptador Hermes, bundles de replay ni suite extendida de experimentos.
2. **Replay histórico previo (`Mad-Max8063/pmp-public-replay-01`)**: `[DOCUMENTED]`
   - Demostración pública "ciega" previa del protocolo (Human -> ChatGPT -> Codex -> ChatGPT) concluida en commit `a4e6469a4257f32809b9405946b07fd2ef3e8416` con CI run `32791128976` pasando 7 tests de aceptación. Demuestra la portabilidad de handoff en un repo satélite independiente.
3. **Rama experimental (`experiment/hermes-pmp-adapter`)**: `[VERIFIED]`
   - Bifurcada de `main` en `2d9da5549d802c27b7a47293384d3f0d59b0ff13` (17 commits por delante).
   - Agrega 73 archivos (6133 inserciones, 273 supresiones netas en `PROJECT_MEMORY.md`), incluyendo:
     - Puente de archivos stdlib-only (`experiments/hermes-pmp/adapter.py`, `consumer.py`, `continuation.py`, `replay.py`, `claude_replay.py`).
     - Bundles de Git archivados con reportes JSON (`replay.bundle`, `live-replay-20261006/replay.bundle`, `claude-continuation-20261006/claude-replay.bundle`, `fresh-codex.bundle`).
     - Verificador offline determinista de la cadena archivada (`experiments/hermes-pmp/verify_chain.py`).
     - Tests unitarios y de regresión (`tests/test_hermes_pmp_adapter.py`, `tests/test_claude_pmp_continuation.py`, `tests/test_pmp_replay_chain.py`).
     - Documentación de revisión externa en inglés y apertura del Draft PR #8 contra `main`.
     - Registros e importaciones de reproducciones same-host (Claude Code y Google Antigravity) y reporte de otra máquina Windows (ACER).
   - Core v0.2.2, profiles y adaptadores existentes se mantienen inalterados.

---

## 2. Objetivo de PMP y versión/naturaleza normativa o experimental

- **Objetivo de PMP**: `[VERIFIED]` (según `SPEC.md`)
  - Definir un contrato nativo de repositorio para que participantes humanos y modelos de IA heterogéneos compartan el estado operativo actual de un proyecto sin depender ni compartir memorias privadas de chat, historiales de conversación, embeddings ni bases vectoriales.
  - Git actúa como capa universal de transporte, autoría, orden cronológico e historial auditable.
  - La memoria canónica (`PROJECT_MEMORY.md` en la raíz) actúa como instantánea compacta de lo que es operativamente cierto ahora.
- **Versión**: `[VERIFIED]`
  - PMP Core: `0.2.2`.
  - Perfil Evidence-backed Handoff: `0.1.1`.
- **Naturaleza**: `[VERIFIED]`
  - PMP Core v0.2.2 es **normativo** (establece cláusulas obligatorias MUST/SHOULD, estructura fija de 8 secciones de nivel 2, etiquetas de evidencia `[VERIFIED]`, `[DOCUMENTED]`, `[ASSUMED]`, exclusiones consecuenciales y reglas de precedencia de fuentes).
  - La integración con Hermes en esta rama es **estrictamente experimental y no normativa**:
    - Es un puente de archivos opcional basado únicamente en la librería estándar de Python (`stdlib-only`).
    - No redefine el Core ni crea un esquema PMP nuevo; las propuestas en formato JSON (`proposal.json`) son transporte de datos no normativo.
    - Hermes, Claude y Codex son participantes externos del experimento, nunca dependencias obligatorias del protocolo.

---

## 3. Estado operativo actual y qué ya fue realizado

De acuerdo con `PROJECT_MEMORY.md` y la evidencia archivada, el estado operativo acumulado es:

1. **Puente y pruebas unitarias**: `[VERIFIED]`
   - Implementado `adapter.py` stdlib-only.
   - Pasan 57 unit tests baseline + 13 tests de bridge (70 tests locales).
2. **Replay Mock inicial**: `[VERIFIED]`
   - Ejecutado localmente con commit baseline `a1b7d1b` y handoff `9be6821`.
   - Subagente Codex fresco sin contexto previo verificó y continuó en commit `25e3b50`.
3. **Habilitación de runtime local Hermes (Live)**: `[VERIFIED]`
   - Entorno minimal Windows aislado con upstream Hermes (`e97923c`, Python 3.14.7, SDK 2.24.0, 0/28 herramientas activas).
   - Registro de problema histórico con almacenamiento OAuth, superado aislando `pmp-home` sin inspeccionar credenciales.
4. **Replay en vivo con Hermes**: `[VERIFIED]`
   - Exactamente una retransmisión acotada completada vía CLI de Hermes (`vgit.e97923c`) con modelo `gpt-5.6-luna`. Hermes propuso normalización de 2 etiquetas de fixtures; el host aplicó los cambios y corrió 3 tests de aceptación.
   - Archivada en `experiments/hermes-pmp/evidence/live-replay-20261006/` con reporte y Git bundle.
   - Continuación por subagente Codex independiente desde clon fresco sin turnos heredados.
5. **Continuación con Claude Code**: `[VERIFIED]`
   - Ejecutada sobre el bundle de Hermes real (sin relanzar Hermes). Claude Code 2.1.274 (Sonnet 5) propuso el manifiesto derivado `labels.txt`.
   - El host corrió y aprobó 6 tests de fixture/manifiesto.
   - Subagente Codex independiente inspeccionó el clon resultante, verificó 14 hashes de inputs históricos y 6 tests de fixture, registrando commit `5e717267e23e39a854347ade7e9efa545269c227` y `fresh-codex.bundle`.
6. **Intento fallido de implementación del verificador por Claude**: `[DOCUMENTED]`
   - Se intentó que Claude implementara `verify_chain.py` offline sin herramientas.
   - Resultado: Timeout a los 300 segundos sin propuesta completa retenida. No hubo reintento ni gasto adicional. Registrado explícitamente como handoff de implementación NO validado.
7. **Implementación de verificador offline por Codex y revisión independiente**: `[VERIFIED]`
   - Codex implementó `verify_chain.py` localmente.
   - Revisor Codex independiente detectó 2 problemas de severidad P2: importaciones ignoradas en helper semántico y ancestros enlazados/symlinks.
   - El host corrigió ambos, agregó tests de regresión y alcanzó 83 tests pasando en la suite completa.
8. **Publicación para revisión externa y Draft PR #8**: `[DOCUMENTED]` / `[VERIFIED]`
   - Redactados brief en inglés (`docs/experiments/hermes-review-brief.md`), borrador de PR y copias para redes (no posteadas).
   - Max autorizó publicación de la rama: push a `experiment/hermes-pmp-adapter` (commit `6ae8b85`) y apertura de Draft PR #8 contra `main`. CI run `37495814502` pasó.
   - Smoke test anónimo sin credenciales validó los 3 bundles, 14 inputs y 6 tests de fixture.
9. **Ronda same-host con Claude Code y Google Antigravity**: `[VERIFIED]` (en repo) / `[DOCUMENTED]` (ejecución de los agentes)
   - Realizada el 2026-10-06 sobre el commit fijado `8c96e926b0d28a182759c45c3a0141fa9a934eba`.
   - Ambos runtimes reportaron exit 0, 3 bundles verificados, 14 inputs históricos, 6 tests de fixture y 7 tests de aceptación.
   - Reportes importados formalmente con manifiesto y normalización LF bajo `experiments/hermes-pmp/evidence/reproductions/` en commit `1f56483e472c518d2954d7af15cfa59f1e5cf58e`, publicado a PR #8 (CI run `37536055141`).
   - Se incorporaron observaciones sobre límites en las declaraciones de Antigravity (afirmaciones excesivamente amplias sobre aislamiento/contexto) y desfase de marcas temporales de Claude.
10. **Reproducción en otra máquina reportada por el maintainer (ACER)**: `[DOCUMENTED]`
    - Max reportó el 2026-10-07 una reproducción offline exitosa en una máquina ACER separada con Windows 11 Home recién reinstalado (build 26300, Python 3.14.8, Git 2.56.0.windows.2) en el commit `1f56483e472c518d2954d7af15cfa59f1e5cf58e`.
    - Salida de consola pegada reportó exit 0 en `verify_chain.py --json` y 7 tests de aceptación en 28.160 s.
    - Se registró el error inicial de tipeo en la variable temporal en `REPORT.md`.
    - Documentación incorporada en commit `9ec50b456db0c3df3fe164446a3dcd7f78ef11c1`, pushed a PR #8 (CI run `37711737829`).
11. **Cierre de publicación actual**: `[VERIFIED]`
    - Commit actual en HEAD `c974baf015b58e867e5fccb335a3c5df67d75089` ("docs: close other-machine evidence publication") asienta en la memoria canónica el cierre de la publicación de dicha evidencia.

---

## 4. Decisiones, restricciones, bloqueos y costos prohibidos

### Decisiones activas clave
1. PMP se mantiene vendor-neutral y canónico. Hermes y Claude son participantes experimentales, no dependencias del Core.
2. Reutilización sin modificaciones del parser/validador de Core y Markdown para sesiones. El formato JSON de propuesta es mero transporte no normativo.
3. Separación estricta entre aserciones de productores, mock vs live, verificación por el host y continuación independiente de Codex. Git no certifica identidad ni frescura por sí solo.
4. Tarea acotada de bajo riesgo: normalización de 2 fixture labels. El host retiene la autoridad exclusiva de escritura fija y ejecución de tests.
5. El timeout de 300 s de Claude en la implementación del verificador se mantiene explícito como handoff fallido/no validado; no se inventa reintento ni éxito.
6. Preservar las revisiones same-host y el reporte de la máquina ACER con sus límites de procedencia explícitos, sin asumir revisión de terceros independientes ni identidad garantizada.

### Restricciones y exclusiones consecuenciales
- Prohibido acceder, reactivar, modificar o depender del experimento anterior bloqueado Hermes/Argon. Cero dependencia de Argon, Obsidian, Jev o Cloudflare.
- Prohibido modificar el Core 0.2.2, especificación, perfiles, versionado o validadores existentes.
- Prohibido merge a `main`, release, creación de tags, despliegues, o cambios en infraestructura/DB.
- Prohibido publicar en redes sociales (X/LinkedIn) o contactar revisores externos sin autorización explícita.
- Prohibido leer, solicitar o almacenar credenciales, claves API o archivos `.env`.
- Prohibido ejecutar acciones destructivas en el repositorio (no reset, no clean, no checkout destructivo, no reescritura de historial).
- Las snapshots y bundles son evidencia histórica archivada; el estado actual reside únicamente en `PROJECT_MEMORY.md` del repositorio exterior.

### Bloqueos
- Track anterior Hermes/Argon: bloqueado y descartado definitivamente.
- Timeout de Claude en la tarea de implementación: bloqueó esa vía de implementación (resuelta con Codex local).

### Costos prohibidos
- **Límite incremental estricto: USD 0**.
- Prohibido activar APIs facturables, invocar modelos pagos, comprar créditos, suscribirse a servicios o realizar repeticiones de inferencia en vivo. Cualquier acción que demande costo debe detenerse inmediatamente señalando `BLOCKED_COST`.

---

## 5. Evidencias primarias con sus rutas y calificación de confianza

| Ruta / Identificador | Calificación | Justificación / Alcance de confianza |
| :--- | :---: | :--- |
| `PROJECT_MEMORY.md` (raíz del repositorio) | `[VERIFIED]` | Leído directamente en el clon; memoria canónica operacional de la rama en HEAD `c974baf`. |
| `SPEC.md` | `[VERIFIED]` | Especificación normativa PMP v0.2.2 leída en el árbol local; idéntica a `main`. |
| Commit `c974baf015b58e867e5fccb335a3c5df67d75089` | `[VERIFIED]` | Verificado con `git rev-parse HEAD`. |
| Commit `2d9da5549d802c27b7a47293384d3f0d59b0ff13` | `[VERIFIED]` | Verificado con `git rev-parse origin/main`. |
| Estado de working tree limpio | `[VERIFIED]` | Verificado con `git status --porcelain` (salida vacía). |
| `experiments/hermes-pmp/verify_chain.py` | `[VERIFIED]` | Código fuente presente y versionado en el árbol local. |
| Bundles de replay archivados (`evidence/live-replay-20261006/replay.bundle`, `claude-continuation-20261006/claude-replay.bundle`, `claude-continuation-20261006/fresh-codex.bundle`, y mock bundles) | `[VERIFIED]` | Presentes físicamente en el filesystem local; hashes SHA-256 documentados. |
| `experiments/hermes-pmp/evidence/reproductions/import-manifest.json` | `[VERIFIED]` | Manifiesto de integridad y normalización de reportes presente en el árbol. |
| `experiments/hermes-pmp/evidence/reproductions/claude-code/` y `google-antigravity/` | `[VERIFIED]` / `[DOCUMENTED]` | `[VERIFIED]` como archivos de reporte versionados; `[DOCUMENTED]` en cuanto a la ejecución reportada por esos agentes en el mismo host. |
| `experiments/hermes-pmp/evidence/reproductions/acer-windows-20261007/REPORT.md` | `[DOCUMENTED]` | Evidencia documental basada en consola pegada por Max desde máquina externa tras reinstalación de Windows; no fue una ejecución observada directamente por este host ni una revisión de tercero ajeno. |
| GitHub Actions Runs (`37495814502`, `37536055141`, `37711737829`) | `[DOCUMENTED]` | Registrados en la memoria canónica; no auditados vía red/API en vivo en esta sesión. |
| GitHub Draft PR #8 (`https://github.com/Mad-Max8063/project-memory-protocol-public/pull/8`) | `[DOCUMENTED]` | Registrado en memoria canónica y archivos de sesión. |

---

## 6. Acción próxima EXACTA indicada por la memoria canónica del repositorio externo

La memoria canónica del repositorio exterior (`PROJECT_MEMORY.md` en líneas 245-251) establece textualmente:

```markdown
## Next action

Max: review the published other-machine evidence in the existing draft PR #8,
then choose whether to close this bounded track or authorize a separately
scoped follow-up. No further execution is needed for this reproduction. Do not
invoke live agents, contact reviewers, post, merge or release by default.
```

> **Distinción crítica**: No debe confundirse con la acción archivada del fixture devuelta por los bundles internos o por `verify_chain.py` (que indicaba *"Max / dispatch host: review .project-memory/sessions/codex-after-claude.md and this canonical update, then close the bounded experiment..."*). Esa pertenece al commit final archivado `5e717267e23e39a854347ade7e9efa545269c227` dentro del fixture sintético, no a la memoria viva del repositorio de PMP.

---

## 7. Qué afirmaciones NO se pueden dar por probadas y por qué

1. **Identidad de modelos o personas**: `[ASSUMED]`
   - Ni los metadatos de Git, ni las autorías de commit, ni los JSON constituyen prueba criptográfica de que Hermes, Claude 3.5 Sonnet, OpenAI Codex o Google Antigravity fueron efectivamente los ejecutores de inferencia, ni de la identidad física de los operadores.
2. **Frescura de sesión y ausencia de memoria privada/caché**: `[ASSUMED]`
   - No se puede verificar criptográficamente que un agente carezca de memoria oculta, contexto en caché o sesgo conversacional previo; solo se verifica la recuperabilidad de contexto a través del repositorio y la ausencia de turnos heredados formalmente declarada.
3. **Revisión externa independiente por terceros**: `[DOCUMENTED]`
   - Las pruebas same-host fueron en la misma máquina del maintainer y la prueba en la máquina ACER fue ejecutada y reportada por el propio maintainer (Max). No existe aún registro de reproducción realizada por una persona u organización externa independiente.
4. **Estado remoto en tiempo real de GitHub (CI / PR)**: `[DOCUMENTED]`
   - Sin llamadas a la red/API de GitHub en esta sesión, el estado abierto de PR #8 y el éxito de los runs de CI (`37711737829`, etc.) son afirmaciones documentadas en la memoria que no han sido revalidadas contra los endpoints remotos en esta invocación.
5. **Autonomía o confiabilidad en tareas generales**: `[ASSUMED]`
   - La cadena validada corresponde a una tarea sintética y determinista de juguete (normalizar 2 strings en un JSON y generar un manifest plano de texto). No puede inferirse fiabilidad general de desarrollo autónomo ni benchmark de ahorro de tokens/tiempo.
6. **Ejecución en sistemas operativos POSIX (Linux/macOS)**: `[DOCUMENTED]`
   - La evidencia actual fue generada en Windows 11. Aunque el código usa librerías estándar portables y existen guías para POSIX, no hay registro de ejecución real en entornos no Windows.
7. **Declaración sobre contextos conocidos**:
   - Como agente receptor en esta sesión, no afirmo que no exista memoria oculta en la plataforma global; únicamente declaro los contextos de los que soy consciente en esta ejecución: el prompt inicial del usuario y el contenido inspeccionado dentro de este clon local de Git.

---

## 8. Propuesta de siguiente paso mínimo y SIN GASTO (sin ejecutarlo)

- **Propuesta**:
  - Configurar un directorio temporal limpio y aislado fuera del árbol de trabajo del clon (por ejemplo en `scratch\pmp-review-tmp-<id>` asignado a `$env:TEMP` y `$env:TMP`).
  - Ejecutar en modo offline determinista el verificador de la cadena archivada:
    ```powershell
    python -B experiments/hermes-pmp/verify_chain.py --json
    ```
  - Ejecutar la suite de pruebas unitarias y de integración de la cadena de replay:
    ```powershell
    python -B -m unittest discover -s tests -p test_pmp_replay_chain.py -v
    ```
- **Condiciones de seguridad y costo**:
  - **Costo incremental: USD 0** (no conecta con proveedores, no usa APIs pagas, no instala dependencias externas; requiere únicamente Git y Python estándar ya presentes).
  - **Cero mutación**: El árbol de trabajo permanece intacto (`git status --porcelain` limpio).
  - **Estado**: Queda en suspenso a la espera de autorización explícita para la Fase 2.
