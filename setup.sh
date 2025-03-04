#!/bin/bash

echo "🛠️  Instalando dependencias con Poetry..."
poetry install

echo "📦  Creando la base de datos..."
poetry run init-db

echo "✅  Instalación completada."
echo "Para usar el CLI, ejecutá: poetry run taskcli show"
