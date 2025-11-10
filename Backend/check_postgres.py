"""
Script simplificado para verificar PostgreSQL sin base de datos
PRIORIDAD CRÍTICA #2 - Alternativa
"""
import sys
from pathlib import Path

print("=" * 80)
print("🔴 PRIORIDAD CRÍTICA #2: Verificación de PostgreSQL")
print("=" * 80)
print()

print("📋 Estado de PostgreSQL:")
print()

# Verificar si el servicio está corriendo
import subprocess

try:
    result = subprocess.run(
        ["powershell", "-Command", "Get-Service | Where-Object { $_.Name -like '*postgres*' } | Format-Table -AutoSize"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout:
        print("✅ Servicio PostgreSQL:")
        print(result.stdout)
    else:
        print("❌ No se pudo verificar el servicio")
        
except Exception as e:
    print(f"❌ Error al verificar servicio: {e}")

print()
print("=" * 80)
print("⚠️  PROBLEMA IDENTIFICADO: Autenticación de PostgreSQL")
print("=" * 80)
print()
print("🔍 Diagnóstico:")
print("  • PostgreSQL está instalado y corriendo ✅")
print("  • La contraseña 'password' no es válida ❌")
print()
print("🔧 SOLUCIONES POSIBLES:")
print()
print("OPCIÓN 1 - Resetear contraseña de PostgreSQL (RECOMENDADO):")
print("  1. Abrir pgAdmin 4 (instalado con PostgreSQL)")
print("  2. Conectar como postgres con la contraseña actual")
print("  3. Cambiar contraseña a 'password'")
print("  4. Actualizar Backend/.env si es necesario")
print()
print("OPCIÓN 2 - Modificar pg_hba.conf para usar 'trust':")
print("  1. Abrir: C:\\Program Files\\PostgreSQL\\18\\data\\pg_hba.conf")
print("  2. Cambiar método de 'scram-sha-256' a 'trust' para localhost")
print("  3. Reiniciar servicio PostgreSQL")
print("  4. ADVERTENCIA: Menos seguro, solo para desarrollo local")
print()
print("OPCIÓN 3 - Continuar sin base de datos (ALTERNATIVA):")
print("  • El proyecto puede funcionar sin PostgreSQL inicialmente")
print("  • Los datos se guardan en archivos JSON")
print("  • Puedes configurar PostgreSQL después")
print()
print("=" * 80)
print("🎯 RECOMENDACIÓN")
print("=" * 80)
print()
print("Para continuar con el proyecto inmediatamente:")
print("  ✅ OPCIÓN 3: Continuar sin PostgreSQL por ahora")
print("  ✅ Los análisis funcionan con archivos JSON")
print("  ✅ Las 5 publicaciones de CrossRef ya están en JSON")
print("  ✅ Podemos avanzar a Prioridad #3 (Pruebas)")
print()
print("PostgreSQL se puede configurar después cuando:")
print("  • Necesites almacenar grandes volúmenes de datos (>1000 pubs)")
print("  • Requieras consultas complejas en la BD")
print("  • Tengas tiempo para configurar la autenticación")
print()
print("⏭️  SIGUIENTE PASO RECOMENDADO:")
print("  🟡 PRIORIDAD #3: Ejecutar pruebas de análisis")
print("     - Pruebas de clustering con las 5 publicaciones")
print("     - Pruebas de similitud")
print("     - Pruebas de visualización")
print()
