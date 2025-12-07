# Solución Rápida: Tarea Automatizada No Funciona

## ❗ Problema
La tarea automatizada en GitHub Actions no está corriendo según el cronograma (cada 15 minutos).

## ✅ Causa Identificada
**Los workflows programados con `schedule` en GitHub Actions SOLO se ejecutan desde la rama predeterminada (`main`).**

Esta es una limitación de la plataforma GitHub, no es un error en la configuración del workflow.

## 🔧 Solución

### Para activar la tarea automatizada:
**Mergear este PR a la rama `main`**

Una vez mergeado:
- ✅ El workflow se ejecutará automáticamente cada 15 minutos
- ✅ Los datos se actualizarán en `phase1_data_pipeline/data/`
- ✅ Los logs se guardarán en `phase1_data_pipeline/logs/`
- ✅ Los cambios se commitearán automáticamente al repositorio

## 📋 Verificación

### Antes del merge (en esta rama):
- ❌ La programación automática NO funciona
- ✅ El trigger manual SÍ funciona (botón "Run workflow")

### Después del merge (en `main`):
- ✅ La programación automática FUNCIONA
- ✅ El trigger manual SIGUE funcionando

## 🧪 Probar Manualmente

Mientras tanto, puedes ejecutar el workflow manualmente:
1. Ve a la pestaña "Actions"
2. Selecciona "Phase 1 Data Pipeline"
3. Haz clic en "Run workflow"
4. Selecciona la rama y confirma

## 📚 Documentación Adicional

- **Guía completa de troubleshooting:** [ACTIONS_TROUBLESHOOTING.md](ACTIONS_TROUBLESHOOTING.md) (en inglés)
- **Documentación del workflow:** [workflows/README.md](workflows/README.md) (en inglés)

## ⏰ Configuración del Cronograma

El workflow está configurado para ejecutarse:
```yaml
schedule:
  - cron: "*/15 * * * *"  # Cada 15 minutos
```

**Importante:** GitHub usa tiempo UTC para las tareas programadas.

## 🔍 Checklist de Verificación

Después de mergear a `main`, verifica que:
- [ ] El workflow aparece en la pestaña Actions
- [ ] No hay mensaje "This workflow is disabled"
- [ ] Las ejecuciones programadas aparecen con event: "schedule"
- [ ] Los commits automáticos se generan cada 15 minutos

## ❓ Si Aún No Funciona Después del Merge

Si después de mergear a `main` el workflow programado no funciona:

1. **Verifica que el workflow esté habilitado:**
   - Ve a Actions → Phase 1 Data Pipeline
   - Si ves "Enable workflow", haz clic

2. **Verifica permisos del repositorio:**
   - Settings → Actions → General
   - Asegúrate que "Allow all actions" esté seleccionado
   - Workflow permissions: "Read and write permissions"

3. **Verifica permisos de la organización** (si aplica):
   - Organization Settings → Actions → General
   - Verifica que los workflows estén permitidos

4. **Actividad del repositorio:**
   - GitHub desactiva workflows si no hay commits en 60 días
   - Solución: Hacer cualquier commit a `main`

## ✨ Resultado Esperado

Una vez funcionando correctamente, verás:
- Commits automáticos cada 15 minutos con mensaje "Automated update — [fecha]"
- Datos actualizados en `phase1_data_pipeline/data/`
- Logs detallados de cada ejecución
- Historial de ejecuciones en la pestaña Actions

---

**Nota:** El workflow ya está correctamente configurado. Solo necesita estar en la rama `main` para que las ejecuciones programadas funcionen.
