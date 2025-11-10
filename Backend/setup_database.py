"""
Script para configurar PostgreSQL
PRIORIDAD CRÍTICA #2
"""
import asyncio
import asyncpg
import sys
from pathlib import Path

async def setup_database():
    """Configura la base de datos PostgreSQL"""
    
    print("=" * 80)
    print("🔴 PRIORIDAD CRÍTICA #2: Configuración de PostgreSQL")
    print("=" * 80)
    print()
    
    # Configuración de conexión
    DB_USER = "postgres"
    DB_PASSWORD = "password"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "bibliometric_analysis"
    
    print("📋 Configuración:")
    print(f"  • Host: {DB_HOST}:{DB_PORT}")
    print(f"  • Usuario: {DB_USER}")
    print(f"  • Base de datos objetivo: {DB_NAME}")
    print()
    
    try:
        # Paso 1: Conectar a la base de datos por defecto (postgres)
        print("🔌 Paso 1: Verificando conexión a PostgreSQL...")
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database='postgres'
        )
        print("   ✅ Conexión exitosa a PostgreSQL")
        
        # Paso 2: Verificar si la base de datos existe
        print(f"\n🔍 Paso 2: Verificando si '{DB_NAME}' existe...")
        result = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)",
            DB_NAME
        )
        
        if result:
            print(f"   ✅ La base de datos '{DB_NAME}' ya existe")
        else:
            print(f"   ⚠️  La base de datos '{DB_NAME}' NO existe")
            print(f"   🔧 Creando base de datos '{DB_NAME}'...")
            
            # Crear base de datos
            await conn.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"   ✅ Base de datos '{DB_NAME}' creada exitosamente")
        
        await conn.close()
        
        # Paso 3: Conectar a la nueva base de datos
        print(f"\n🔌 Paso 3: Conectando a '{DB_NAME}'...")
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        print(f"   ✅ Conectado a '{DB_NAME}'")
        
        # Paso 4: Crear tabla de publicaciones si no existe
        print("\n🗄️  Paso 4: Verificando tablas...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS publications (
            id VARCHAR(255) PRIMARY KEY,
            title TEXT NOT NULL,
            abstract TEXT,
            authors JSONB,
            keywords TEXT[],
            doi VARCHAR(255),
            publication_year INTEGER,
            publication_date DATE,
            journal VARCHAR(500),
            source VARCHAR(100),
            url TEXT,
            citation_count INTEGER DEFAULT 0,
            publisher VARCHAR(500),
            publication_type VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        await conn.execute(create_table_sql)
        print("   ✅ Tabla 'publications' verificada/creada")
        
        # Crear índices
        print("\n📊 Paso 5: Creando índices...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_publications_doi ON publications(doi);",
            "CREATE INDEX IF NOT EXISTS idx_publications_year ON publications(publication_year);",
            "CREATE INDEX IF NOT EXISTS idx_publications_source ON publications(source);",
            "CREATE INDEX IF NOT EXISTS idx_publications_title ON publications USING gin(to_tsvector('english', title));"
        ]
        
        for idx_sql in indices:
            await conn.execute(idx_sql)
        
        print("   ✅ Índices creados")
        
        # Paso 6: Verificar datos existentes
        print("\n📈 Paso 6: Verificando datos existentes...")
        count = await conn.fetchval("SELECT COUNT(*) FROM publications")
        print(f"   📊 Publicaciones en base de datos: {count}")
        
        await conn.close()
        
        # Resumen final
        print()
        print("=" * 80)
        print("✅ CONFIGURACIÓN DE POSTGRESQL COMPLETADA")
        print("=" * 80)
        print()
        print("📊 Resumen:")
        print(f"  ✅ PostgreSQL corriendo en {DB_HOST}:{DB_PORT}")
        print(f"  ✅ Base de datos '{DB_NAME}' lista")
        print(f"  ✅ Tabla 'publications' creada con índices")
        print(f"  📊 Publicaciones almacenadas: {count}")
        print()
        print("🎯 Próximos pasos:")
        print("  1. Guardar las 5 publicaciones de CrossRef en la BD")
        print("  2. Verificar consultas")
        print("  3. Continuar con Prioridad #3 (Pruebas)")
        print()
        
        return True
        
    except asyncpg.InvalidPasswordError:
        print()
        print("❌ ERROR: Contraseña incorrecta")
        print()
        print("🔧 SOLUCIÓN:")
        print("  1. Verificar contraseña de PostgreSQL")
        print("  2. Actualizar en Backend/.env: DATABASE_PASSWORD")
        print()
        return False
        
    except asyncpg.CannotConnectNowError:
        print()
        print("❌ ERROR: No se puede conectar a PostgreSQL")
        print()
        print("🔧 SOLUCIÓN:")
        print("  1. Verificar que PostgreSQL esté corriendo:")
        print("     Get-Service | Where-Object { $_.Name -like '*postgres*' }")
        print("  2. Si no está corriendo, iniciarlo:")
        print("     Start-Service postgresql-x64-18")
        print()
        return False
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERROR EN LA CONFIGURACIÓN")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        import traceback
        print("Stack trace:")
        traceback.print_exc()
        print()
        return False

if __name__ == "__main__":
    result = asyncio.run(setup_database())
    sys.exit(0 if result else 1)
