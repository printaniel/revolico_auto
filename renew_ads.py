"""
AUTOMATIZADOR REVOLICO - Versión Simple para Cuba
Autor: Automatización Cuba
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
    """Login CON VERIFICACIÓN REAL de sesión"""
    imprimir("🔐 Login con verificación de sesión...")
    
    try:
        # 1. Ir a login
        driver.get("https://www.revolico.com/auth/signin")
        esperar_tiempo(3, 4)
        
        # 2. Verificar que estamos en la página correcta
        if "signin" not in driver.current_url:
            imprimir(f"❌ ERROR: No estamos en signin. URL: {driver.current_url}")
            return False
        
        # 3. Tomar screenshot inicial
        driver.save_screenshot("login_inicial.png")
        
        # 4. Llenar campos (sabemos que existen)
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        pass_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        email_field.send_keys(usuario)
        esperar_tiempo(1, 2)
        pass_field.send_keys(password)
        esperar_tiempo(1, 2)
        
        # 5. Hacer clic en login
        boton = driver.find_element(By.XPATH, "//button[contains(text(), 'Iniciar sesión')]")
        boton.click()
        
        # 6. Esperar respuesta
        esperar_tiempo(5, 7)
        driver.save_screenshot("login_despues.png")
        
        # 7. VERIFICACIÓN CRÍTICA: ¿Realmente estamos logueados?
        imprimir("🔍 Verificando sesión activa...")
        
        # Intento 1: Ir a "Mis anuncios"
        driver.get("https://www.revolico.com/my-ads")
        esperar_tiempo(3, 4)
        
        # Verificar contenido de "Mis anuncios"
        page_source = driver.page_source.lower()
        
        # Posibles textos en "Mis anuncios"
        if any(texto in page_source for texto in ['mis anuncios', 'mis-anuncios', 'my ads', 'tus anuncios']):
            imprimir("✅ VERIFICADO: Acceso a 'Mis anuncios' exitoso")
            return True
        
        # Intento 2: Verificar elementos de usuario logueado
        driver.get("https://www.revolico.com/")
        esperar_tiempo(2, 3)
        
        # Buscar menú de usuario
        try:
            elementos_usuario = driver.find_elements(By.XPATH, "//*[contains(text(), '@') or contains(text(), 'Cuenta') or contains(text(), 'Perfil') or contains(text(), 'Salir')]")
            if elementos_usuario:
                imprimir(f"✅ VERIFICADO: Encontrado menú de usuario ({len(elementos_usuario)} elementos)")
                return True
        except:
            pass
        
        # Intento 3: Verificar cookies de sesión
        cookies = driver.get_cookies()
        cookies_sesion = [c for c in cookies if 'session' in c['name'].lower() or 'token' in c['name'].lower()]
        
        if cookies_sesion:
            imprimir(f"✅ VERIFICADO: Cookies de sesión encontradas ({len(cookies_sesion)})")
            return True
        
        # SI LLEGAMOS AQUÍ: Login falló
        imprimir("❌ FALLA CRÍTICA: No hay evidencia de sesión activa")
        imprimir(f"📍 URL actual: {driver.current_url}")
        imprimir(f"📏 Tamaño página: {len(page_source)} caracteres")
        
        # Mostrar fragmento de HTML para debug
        imprimir("📄 HTML fragmento:")
        imprimir(page_source[:1000])
        
        return False
        
    except Exception as e:
        imprimir(f"💥 Error crítico en login: {str(e)}")
        return False

def renovar_anuncio(navegador, url, numero, total):
    """Renueva un anuncio CON VERIFICACIÓN REAL"""
    imprimir(f"🔄 Procesando anuncio {numero}/{total}")
    imprimir(f"📍 URL: {url}")
    
    try:
        # Ir al anuncio
        navegador.get(url)
        esperar_tiempo(3, 5)
        
        # 1. VERIFICAR SI TENEMOS ACCESO
        page_source = navegador.page_source.lower()
        
        # Mensajes de ERROR que deberían aparecer si no tenemos acceso
        mensajes_acceso_denegado = [
            'acceso denegado',
            'no tienes permisos',
            'no autorizado',
            'este anuncio no es tuyo',
            'no puedes editar este anuncio',
            'error 403',
            'forbidden'
        ]
        
        for mensaje in mensajes_acceso_denegado:
            if mensaje in page_source:
                imprimir(f"❌ ACCESO DENEGADO: {mensaje}")
                return False
        
        # 2. TOMAR SCREENSHOT ANTES para debug
        navegador.save_screenshot(f"anuncio_{numero}_antes.png")
        imprimir(f"📸 Screenshot: anuncio_{numero}_antes.png")
        
        # 3. BUSCAR BOTÓN REALMENTE VISIBLE
        botones = navegador.find_elements(By.TAG_NAME, "button")
        imprimir(f"🔍 Encontrados {len(botones)} botones")
        
        boton_encontrado = None
        for i, boton in enumerate(botones):
            texto = boton.text.strip()
            if texto:
                imprimir(f"   Botón {i}: '{texto}'")
                if any(palabra in texto.lower() for palabra in ['renovar', 'subir', 'actualizar', 'publicar']):
                    boton_encontrado = boton
                    imprimir(f"✅ Posible botón: '{texto}'")
                    break
        
        if not boton_encontrado:
            imprimir("❌ No se encontró botón de renovación")
            return False
        
        # 4. HACER CLIC Y VER QUÉ PASA
        imprimir("🖱️ Haciendo clic...")
        boton_encontrado.click()
        esperar_tiempo(3, 5)
        
        # 5. TOMAR SCREENSHOT DESPUÉS
        navegador.save_screenshot(f"anuncio_{numero}_despues.png")
        
        # 6. VERIFICAR RESULTADO REAL
        page_source_despues = navegador.page_source.lower()
        
        # Buscar mensajes de ÉXITO reales
        mensajes_exito = [
            'anuncio renovado',
            'renovado exitosamente', 
            'actualizado correctamente',
            'publicado nuevamente',
            'subido exitosamente',
            'renovación exitosa'
        ]
        
        # Buscar mensajes de ERROR reales
        mensajes_error = [
            'error',
            'no se pudo',
            'inténtalo de nuevo',
            'algo salió mal',
            'ocurrió un error'
        ]
        
        exito = False
        for mensaje in mensajes_exito:
            if mensaje in page_source_despues:
                imprimir(f"✅ CONFIRMADO: '{mensaje}'")
                exito = True
                break
        
        if not exito:
            # Verificar si hay error
            for mensaje in mensajes_error:
                if mensaje in page_source_despues:
                    imprimir(f"❌ ERROR: '{mensaje}' encontrado")
                    return False
            
            imprimir("⚠️ Sin confirmación explícita - revisar screenshots")
            # Mostrar un fragmento del HTML para debug
            imprimir("📄 Fragmento HTML después del clic:")
            imprimir(page_source_despues[:500])
        
        return exito
        
    except Exception as e:
        imprimir(f"💥 Error renovando: {str(e)}")
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