# Propuesta de Mejora Técnica: Manejo de Saltos de Línea (LF / CRLF) en Evidencia de Texto

- **Fecha de registro**: 2026-10-13
- **Origen**: Hallazgo empírico durante la verificación offline en Windows 11 (`google-antigravity`, run `20261013T215241Z`).
- **Estado**: Propuesta de mejora pendiente (código y archivos históricos sin modificar).

---

## 1. Descripción del Problema y Causa Raíz

En plataformas Windows, la configuración global o predeterminada del instalador de Git suele ser `core.autocrlf = true`.
Bajo esta configuración:
1. Al clonar o hacer checkout de un repositorio sin la bandera explícita `--config core.autocrlf=false`, Git traduce automáticamente los saltos de línea LF (`\n`) de los archivos identificados como texto a CRLF (`\r\n`) en el árbol de trabajo local.
2. Los archivos binarios (tales como `replay.bundle`, `claude-replay.bundle` y `fresh-codex.bundle`) se conservan byte a byte sin alteración.
3. Sin embargo, los reportes de evidencia en formato JSON (`replay-report.json`, `claude-report.json`, `fresh-codex.json`) son tratados por Git como texto plano.
4. El verificador `experiments/hermes-pmp/verify_chain.py` lee los archivos de evidencia en modo crudo (`path.read_bytes()`) y compara su digest SHA-256 directo contra los hashes fijados en la constante `PINNED`.
5. Al contener bytes `\r\n` en lugar de `\n`, el hash SHA-256 en disco difiere:
   - Hash observado en disco con CRLF: `7a4e48c07877982bb7826d2420b8fa065c6a46c7c8dacdc47ef46d7e18177951`
   - Hash esperado fijado (LF original): `ade8546d585305fdccbb3061da91898e5a3ab991b8178815106faa36de134c7d`
6. `git status --porcelain` reporta el árbol limpio porque Git oculta la diferencia de saltos de línea según `autocrlf`, pero `verify_chain.py` falla con:
   ```json
   {"verified": false, "error": "archive digest mismatch: live-replay-20261006/replay-report.json"}
   ```

---

## 2. Propuestas de Solución

Se identifican dos enfoques complementarios y compatibles con la filosofía de PMP:

### Enfoque A: Declaración explícita en `.gitattributes` (Recomendado a nivel repositorio)
Configurar un archivo `.gitattributes` en la raíz del repositorio (o dentro de `experiments/hermes-pmp/evidence/`) que fuerce a Git a respetar los saltos de línea LF originales independientemente de la configuración del sistema operativo o del usuario:
```gitattributes
# Garantizar que los reportes de evidencia y fixtures preserven LF en cualquier plataforma
experiments/hermes-pmp/evidence/**/*.json text eol=lf
experiments/hermes-pmp/evidence/**/*.md text eol=lf
*.bundle binary
```
*Ventajas*: Cero cambios en el código de Python; Git garantiza la checkout exacta de bytes en Windows, Linux y macOS sin requerir banderas manuales en `git clone`.

### Enfoque B: Diagnóstico amigable en `verify_chain.py` (Robustez de herramienta)
Sin relajar la exigencia estricta de integridad criptográfica de la evidencia, si `read_file` o `verify_chain` detecta una discrepancia de digest pero el hash normalizado (`data.replace(b'\r\n', b'\n')`) coincide con el valor esperado, emitir un mensaje de diagnóstico preciso:
```python
if digest(data) != expected:
    if digest(data.replace(b'\r\n', b'\n')) == expected:
        raise ValueError(f"archive digest mismatch due to CRLF line endings in {name}; "
                         f"configure 'git config core.autocrlf false' or check out with LF")
    raise ValueError('archive digest mismatch: ' + name)
```
*Ventajas*: Permite al usuario/agente identificar inmediatamente que no se trata de corrupción de datos sino de una mutación de saltos de línea propia del entorno Windows.

---

## 3. Propuesta de Prueba de Regresión Separada

Para asegurar que futuras versiones manejen o diagnostiquen este escenario de forma controlada:
- **Ubicación propuesta**: `tests/test_pmp_replay_chain.py`
- **Nombre de prueba**: `test_crlf_detection_and_informative_error`
- **Mecánica del test**:
  1. Crear un directorio temporal con una copia de `EVIDENCE`.
  2. Modificar artificialmente `live-replay-20261006/replay-report.json` inyectando saltos `\r\n`.
  3. Ejecutar `verify_chain.verify_chain(temp_evidence)` y asserting que:
     - El verificador rechaza los bytes mutados sin ejecutar subprocesos de Git.
     - El mensaje de error indica claramente la presencia de saltos de línea CRLF como causal del fallo de digest.

---

## 4. Estado de Implementación
- **Código y fixtures actuales**: Permanecen estrictamente intactos.
- **Acción requerida**: Someter esta propuesta a la decisión de la autoridad humana (Max) para su implementación en un PR o release posterior.
