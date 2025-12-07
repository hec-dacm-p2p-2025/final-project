# dcm-final-project-p2p
End-to-end project for the DaCM course, built around real-time Binance P2P market data. The work includes a Python data pipeline, a reusable analysis package, and an interactive dashboard, all developed collaboratively in a single coordinated repository.

## 🤖 Automated Data Pipeline

This repository includes an automated GitHub Actions workflow that runs every 15 minutes to:
- Fetch real-time Binance P2P market data
- Retrieve Brazilian Central Bank (BCB) exchange rates
- Process and commit data automatically

### 📖 Documentation

- **[Solución Rápida](/.github/SOLUCION_RAPIDA.md)** - Guía rápida en español para configurar la tarea automatizada
- **[Actions Troubleshooting Guide](/.github/ACTIONS_TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide
- **[Workflow Documentation](/.github/workflows/README.md)** - Detailed workflow information

### ⚠️ Important Note

The automated workflow requires the workflow file to be on the `main` branch to run on schedule. See the documentation above for details.
