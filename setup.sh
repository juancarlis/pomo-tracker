#!/bin/bash

# Función para instalar dependencias y crear la DB
install() {
    echo "🛠️  Instalando dependencias con Poetry..."
    poetry install

    echo "📦  Creando la base de datos..."
    poetry run init-db

    echo "✅  Instalación completada."
    echo "Para usar el CLI, ejecutá: poetry run taskcli show"
}

# Función para insertar datos de prueba
seed() {
    echo "🌱  Insertando tareas de prueba..."

    tasks=(
        "Revisar reporte financiero"
        "Escribir artículo sobre IA"
        "Estudiar álgebra lineal"
        "Optimizar código del side project"
        "Planificar viaje de vacaciones"
        "Preparar presentación para cliente"
        "Leer paper sobre machine learning"
        "Resolver ejercicios de estadística"
        "Implementar nueva feature en app"
        "Organizar archivos personales"
    )

    categories=(1 2 3 4 5)  # IDs de categorías

    for i in {0..9}; do
        task="${tasks[$i]}"
        category="${categories[$((RANDOM % ${#categories[@]}))]}"  # Selecciona una categoría aleatoria
        echo "➕  Agregando tarea: '$task' en categoría $category..."
        poetry run taskcli task add "$task" "$category"
    done

    echo "✅  Se insertaron tareas de prueba correctamente."
}

# Si no se pasa un argumento, ejecuta la instalación normal
if [[ "$1" == "seed" ]]; then
    seed
else
    install
fi
