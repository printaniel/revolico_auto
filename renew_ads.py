"""
AUTOMATIZADOR REVOLICO - Versión Simple para Cuba
Autor: Automatización Cuba
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import random
from datetime import datetime

# ============================================================
# CONFIGURACIÓN - EDITA SOLO ESTA PARTE
# ============================================================

# LISTA DE TUS ANUNCIOS (CAMBIA ESTAS URLs)
TUS_ANUNCIOS = [
    "https://www.revolico.com/item/51214616/_/manage ",  # REEMPLAZA CON TU URL REAL
    "https://www.revolico.com/item/51214605/_/manage?action=created",  # REEMPLAZA CON TU URL REAL
]

# NO CAMBIES ESTAS LÍNEAS
USER_REVOLICO = os.getenv('REVOLICO_USER')
PASS_REVOLICO = os.getenv('REVOLICO_PASS')

# ============================================================
# NO EDITES NADA DEBAJO (a menos que sepas lo que haces)
# ============================================================

def esperar_tiempo(min=2, max=4):
    """Espera tiempo aleatorio como humano"""
    tiempo = random.uniform(min, max)
    time.sleep(tiempo)

def imprimir(mensaje):
    """Muestra mensajes con hora"""
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {mensaje}")

def setup_chrome():
    """Configura Chrome para evitar detección"""
    imprimir("🛠️ Configurando navegador...")
    
    opciones = Options()
    
    # Modo invisible
    opciones.add_argument("--headless")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    
    # Evitar detección
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option('useAutomationExtension', False)
    
    # User-agent real
    opciones.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(options=opciones)

def hacer_login(driver, usuario, password):
    """Intenta login en Revolico"""
    imprimir("🔐 Intentando login en Revolico...")
    
    try:
        driver.get("https://www.revolico.com/login")
        esperar_tiempo(3, 5)
        
        # Buscar campo usuario
        try:
            campo_user = driver.find_element(By.NAME, "username")
        except:
            campo_user = driver.find_element(By.NAME, "email")
        
        campo_user.send_keys(usuario)
        esperar_tiempo(1, 2)
        
        # Buscar campo password
        campo_pass = driver.find_element(By.NAME, "password")
        campo_pass.send_keys(password)
        esperar_tiempo(1, 2)
        
        # Buscar botón login
        botones = driver.find_elements(By.TAG_NAME, "button")
        for boton in botones:
            if boton.text.lower() in ["iniciar sesión", "entrar", "login"]:
                boton.click()
                break
        
        esperar_tiempo(4, 6)
        imprimir("✅ Login completado")
        return True
        
    except Exception as e:
        imprimir(f"❌ Error en login: {e}")
        return False

def renovar_anuncio(driver, url, numero):
    """Renueva un anuncio específico"""
    imprimir(f"🔄 Procesando anuncio {numero}: {url[:50]}...")
    
    try:
        # Ir al anuncio
        driver.get(url)
        esperar_tiempo(3, 5)
        
        # Buscar TODOS los botones posibles
        todos_botones = driver.find_elements(By.TAG_NAME, "button")
        todos_links = driver.find_elements(By.TAG_NAME, "a")
        todos_inputs = driver.find_elements(By.TAG_NAME, "input")
        
        elementos = todos_botones + todos_links + todos_inputs
        
        # Palabras clave para buscar
        palabras_clave = [
            "renovar", "Renovar", "RENOVAR",
            "subir", "Subir", "SUBIR",
            "publicar", "Publicar", "PUBLICAR",
            "actualizar", "Actualizar", "ACTUALIZAR"
        ]
        
        # Buscar elemento que contenga alguna palabra clave
        elemento_encontrado = None
        for elemento in elementos:
            texto = elemento.text.strip()
            valor = elemento.get_attribute("value") or ""
            
            for palabra in palabras_clave:
                if palabra in texto or palabra in valor:
                    elemento_encontrado = elemento
                    break
            
            if elemento_encontrado:
                break
        
        if elemento_encontrado:
            # Hacer clic
            elemento_encontrado.click()
            imprimir(f"✅ Clic en botón encontrado")
            esperar_tiempo(2, 4)
            
            # Verificar éxito (mensajes comunes)
            pagina = driver.page_source.lower()
            if any(palabra in pagina for palabra in ['éxito', 'exito', 'renovado', 'actualizado']):
                imprimir("✅ Renovación confirmada")
            else:
                imprimir("⚠️ Renovación posible (sin confirmación explícita)")
            
            return True
        else:
            imprimir("❌ No se encontró botón de renovación")
            return False
            
    except Exception as e:
        imprimir(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    imprimir("="*50)
    imprimir("🚀 INICIANDO AUTORENOVADOR REVOLICO")
    imprimir("="*50)
    
    # Verificar config
    if "tu-anuncio-1" in TUS_ANUNCIOS[0]:
        imprimir("❌ ERROR: No has configurado tus URLs")
        imprimir("   Edita el archivo y pon tus URLs reales")
        return
    
    # Verificar credenciales
    if not USER_REVOLICO or not PASS_REVOLICO:
        imprimir("❌ ERROR: No hay credenciales configuradas")
        imprimir("   Configura los secrets en GitHub")
        return
    
    driver = None
    try:
        # 1. Configurar navegador
        driver = setup_chrome()
        
        # 2. Login
        if not hacer_login(driver, USER_REVOLICO, PASS_REVOLICO):
            imprimir("❌ Falló el login. Abortando.")
            return
        
        # 3. Renovar cada anuncio
        total = len(TUS_ANUNCIOS)
        exitos = 0
        
        for i, url in enumerate(TUS_ANUNCIOS, 1):
            imprimir(f"📊 Progreso: {i}/{total}")
            
            if renovar_anuncio(driver, url, i):
                exitos += 1
            
            # Esperar entre anuncios
            if i < total:
                espera = random.uniform(8, 15)
                imprimir(f"⏳ Esperando {int(espera)}s...")
                time.sleep(espera)
        
        # 4. Resultado final
        imprimir("="*50)
        imprimir(f"📈 RESUMEN FINAL:")
        imprimir(f"   Total anuncios: {total}")
        imprimir(f"   Renovados: {exitos}")
        imprimir(f"   Fallados: {total - exitos}")
        imprimir("="*50)
        
        if exitos == total:
            imprimir("🎉 ¡TODOS LOS ANUNCIOS RENOVADOS!")
        else:
            imprimir("⚠️  Algunos anuncios no se pudieron renovar")
        
    except Exception as e:
        imprimir(f"💥 ERROR GRAVE: {e}")
    finally:
        if driver:
            driver.quit()
            imprimir("👋 Navegador cerrado")

if __name__ == "__main__":
    main()