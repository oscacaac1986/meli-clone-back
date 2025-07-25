import json
import os
from pathlib import Path


def create_directories():
    """Crear directorios necesarios"""
    directories = ["static", "static/images", "static/images/products"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio: {directory}")

def create_svg_images():
    """Crear imágenes SVG simples y atractivas"""
    images_dir = Path("static/images/products")
    
    # Template SVG mejorado con gradientes
    svg_template = '''<svg width="600" height="600" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad{id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
        </linearGradient>
    </defs>
    <rect width="600" height="600" fill="url(#grad{id})"/>
    
    <!-- Elementos decorativos -->
    <circle cx="150" cy="150" r="80" fill="rgba(255,255,255,0.1)"/>
    <circle cx="450" cy="450" r="60" fill="rgba(255,255,255,0.1)"/>
    
    <!-- Contenido principal -->
    <rect x="50" y="220" width="500" height="160" rx="20" fill="rgba(255,255,255,0.15)"/>
    
    <!-- Texto principal -->
    <text x="300" y="270" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="white" text-anchor="middle">{title}</text>
    <text x="300" y="310" font-family="Arial, sans-serif" font-size="18" fill="rgba(255,255,255,0.9)" text-anchor="middle">{subtitle}</text>
    <text x="300" y="340" font-family="Arial, sans-serif" font-size="14" fill="rgba(255,255,255,0.8)" text-anchor="middle">MercadoLibre Clone</text>
    
    <!-- Badge de producto -->
    <rect x="200" y="420" width="200" height="40" rx="20" fill="rgba(255,255,255,0.2)"/>
    <text x="300" y="445" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="white" text-anchor="middle">PRODUCTO OFICIAL</text>
    
    <!-- Elemento de smartphone -->
    <rect x="270" y="480" width="60" height="100" rx="15" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
    <rect x="280" y="490" width="40" height="70" rx="5" fill="rgba(255,255,255,0.1)"/>
    <circle cx="300" cy="570" r="8" fill="rgba(255,255,255,0.4)"/>
</svg>'''
    
    # Configuración de imágenes con gradientes atractivos
    images = [
        # Galaxy A55 - Producto principal
        ("Samsung Galaxy A55", "5G Dual SIM 128GB", "#667eea", "#764ba2", "galaxy_a55_1.svg", 1),
        ("Galaxy A55", "Vista Trasera", "#764ba2", "#667eea", "galaxy_a55_2.svg", 2),
        ("Galaxy A55", "Vista Lateral", "#f093fb", "#f5576c", "galaxy_a55_3.svg", 3),
        ("Galaxy A55", "Características", "#4facfe", "#00f2fe", "galaxy_a55_4.svg", 4),
        
        # Productos relacionados
        ("Samsung Galaxy A54", "5G 128GB", "#5f27cd", "#a29bfe", "galaxy_a54_1.svg", 5),
        ("Galaxy A54", "Cámara Triple", "#a29bfe", "#6c5ce7", "galaxy_a54_2.svg", 6),
        
        ("Samsung Galaxy A35", "5G Dual SIM", "#00d2d3", "#00cec9", "galaxy_a35_1.svg", 7),
        ("Galaxy A35", "Pantalla AMOLED", "#00cec9", "#55a3ff", "galaxy_a35_2.svg", 8),
        
        ("Samsung Galaxy A25", "5G Negro", "#ff7675", "#fd79a8", "galaxy_a25_1.svg", 9),
        ("Galaxy A25", "Alto Rendimiento", "#fd79a8", "#fdcb6e", "galaxy_a25_2.svg", 10),
        
        ("Samsung Galaxy A15", "5G Azul", "#74b9ff", "#0984e3", "galaxy_a15_1.svg", 11),
        ("Galaxy A15", "Batería Duradera", "#0984e3", "#74b9ff", "galaxy_a15_2.svg", 12),
        
        # Imagen por defecto
        ("Imagen No Disponible", "Producto", "#ddd", "#bbb", "default.svg", 13),
    ]
    
    print(f"🎨 Creando {len(images)} imágenes SVG...")
    
    success_count = 0
    for title, subtitle, color1, color2, filename, img_id in images:
        try:
            svg_content = svg_template.format(
                title=title, 
                subtitle=subtitle, 
                color1=color1, 
                color2=color2,
                id=img_id
            )
            file_path = images_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✅ Creado: {filename}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error creando {filename}: {e}")
    
    print(f"\n🎉 Imágenes creadas: {success_count}/{len(images)}")
    return success_count > 0

def update_products_json():
    """Actualizar products.json con URLs de imágenes SVG"""
    products_file = Path("app/data/products.json")
    
    if not products_file.exists():
        print("❌ products.json no encontrado")
        return False
    
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        base_url = "http://localhost:8000/static/images/products"
        
        # Mapear productos a imágenes
        image_mapping = {
            "MLA123456789": ["galaxy_a55_1.svg", "galaxy_a55_2.svg", "galaxy_a55_3.svg", "galaxy_a55_4.svg"],
            "MLA123456790": ["galaxy_a54_1.svg", "galaxy_a54_2.svg"],
            "MLA123456791": ["galaxy_a35_1.svg", "galaxy_a35_2.svg"],
            "MLA123456792": ["galaxy_a25_1.svg", "galaxy_a25_2.svg"],
            "MLA123456793": ["galaxy_a15_1.svg", "galaxy_a15_2.svg"]
        }
        
        # Actualizar imágenes para productos relacionados también
        for product in data.get("products", []):
            product_id = product["id"]
            if product_id in image_mapping:
                product["images"] = [f"{base_url}/{img}" for img in image_mapping[product_id]]
            else:
                product["images"] = [f"{base_url}/default.svg"]
        
        # Guardar archivo actualizado
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("✅ products.json actualizado con URLs de imágenes SVG")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando products.json: {e}")
        return False

def verify_setup():
    """Verificar que todo esté configurado correctamente"""
    print("\n🔍 Verificando configuración...")
    
    # Verificar directorios
    images_dir = Path("static/images/products")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.svg"))
        print(f"   ✅ Directorio de imágenes: {len(image_files)} archivos SVG")
        
        # Mostrar algunas imágenes
        for file in image_files[:3]:
            print(f"      • {file.name}")
        if len(image_files) > 3:
            print(f"      • ... y {len(image_files) - 3} más")
    else:
        print("   ❌ Directorio de imágenes no encontrado")
        return False
    
    # Verificar products.json
    products_file = Path("app/data/products.json")
    if products_file.exists():
        print("   ✅ products.json existe")
    else:
        print("   ❌ products.json no encontrado")
        return False
    
    return True

def main():
    """Función principal"""
    print("🎨 CREANDO IMÁGENES SVG PARA MERCADOLIBRE")
    print("=" * 50)
    
    # Verificar ubicación
    if not Path("app").exists():
        print("❌ Error: Ejecuta este script desde la raíz del backend")
        print("   Ubicación actual:", Path.cwd())
        print("   Ejecuta: cd C:\\Users\\oscar\\Documents\\MercadoLibre\\meli-clone-back")
        return
    
    print("✅ Ubicación correcta detectada")
    
    # Paso 1: Crear directorios
    print("\n📁 Paso 1: Creando directorios...")
    create_directories()
    
    # Paso 2: Crear imágenes SVG
    print("\n🎨 Paso 2: Creando imágenes SVG...")
    if not create_svg_images():
        print("❌ Error creando imágenes")
        return
    
    # Paso 3: Actualizar JSON
    print("\n📝 Paso 3: Actualizando products.json...")
    if not update_products_json():
        print("❌ Error actualizando JSON")
        return
    
    # Paso 4: Verificar configuración
    if not verify_setup():
        print("❌ Verificación fallida")
        return
    
    # Éxito
    print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
    print("\n🔗 URLs para probar:")
    print("   • Imagen ejemplo: http://localhost:8000/static/images/products/galaxy_a55_1.svg")
    print("   • API de imágenes: http://localhost:8000/api/images")
    print("   • Documentación: http://localhost:8000/docs")
    print("   • Frontend: http://localhost:3000")
    
    print("\n💡 Pasos siguientes:")
    print("   1. Reinicia el servidor backend:")
    print("      uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    print("   2. Abre el frontend en http://localhost:3000")
    print("   3. ¡Las imágenes deberían cargar correctamente!")

if __name__ == "__main__":
    main()