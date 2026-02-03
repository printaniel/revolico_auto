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
    """Login DIRECTO a Revolico - Con debugging mejorado"""
    imprimir("🔐 INTENTANDO LOGIN - MODO DEBUG")
    
    try:
        # 1. IR A LA PÁGINA Y VER QUÉ HAY
        imprimir(f"🌐 Navegando a: https://www.revolico.com/auth/signin")
        driver.get("https://www.revolico.com/auth/signin")
        
        # Esperar y guardar PRIMER screenshot
        esperar_tiempo(3, 5)
        driver.save_screenshot("01_pagina_inicial.png")
        imprimir("📸 Screenshot 1: 01_pagina_inicial.png")
        
        # 2. VER QUÉ HAY EN LA PÁGINA
        imprimir("🔍 ANALIZANDO PÁGINA...")
        imprimir(f"📏 Tamaño página: {len(driver.page_source)} caracteres")
        imprimir(f"📍 URL actual: {driver.current_url}")
        imprimir(f"📄 Título página: {driver.title}")
        
        # Ver si estamos en la página correcta
        if "signin" not in driver.current_url:
            imprimir(f"⚠️ ADVERTENCIA: No estamos en signin. URL actual: {driver.current_url}")
            imprimir("🔄 Redirigiendo manualmente a signin...")
            driver.get("https://www.revolico.com/auth/signin")
            esperar_tiempo(2, 3)
        
        # 3. BUSCAR TODOS LOS INPUTS para ver qué hay realmente
        imprimir("🔍 BUSCANDO TODOS LOS ELEMENTOS INPUT...")
        todos_inputs = driver.find_elements(By.TAG_NAME, "input")
        imprimir(f"📊 Encontrados {len(todos_inputs)} elementos <input>")
        
        for i, input_elem in enumerate(todos_inputs):
            try:
                input_type = input_elem.get_attribute("type") or "sin-type"
                input_name = input_elem.get_attribute("name") or "sin-name"
                input_id = input_elem.get_attribute("id") or "sin-id"
                input_placeholder = input_elem.get_attribute("placeholder") or "sin-placeholder"
                
                imprimir(f"   Input {i}: type='{input_type}', name='{input_name}', id='{input_id}', placeholder='{input_placeholder}'")
            except:
                imprimir(f"   Input {i}: Error al obtener info")
        
        # 4. BUSCAR FORMULARIO ESPECÍFICO
        imprimir("🎯 BUSCANDO FORMULARIO DE LOGIN...")
        
        # ESTRATEGIA: Buscar por placeholder común
        placeholder_email = None
        placeholder_password = None
        
        placeholders_comunes = [
            "Correo electrónico", "correo electrónico", "Email", "email",
            "E-mail", "e-mail", "Correo", "correo"
        ]
        
        placeholders_password = [
            "Contraseña", "contraseña", "Password", "password",
            "Clave", "clave"
        ]
        
        for input_elem in todos_inputs:
            placeholder = input_elem.get_attribute("placeholder") or ""
            
            for placeholder_buscado in placeholders_comunes:
                if placeholder_buscado.lower() in placeholder.lower():
                    placeholder_email = placeholder
                    imprimir(f"✅ POSIBLE campo email: placeholder='{placeholder}'")
                    campo_email = input_elem
                    break
            
            for placeholder_buscado in placeholders_password:
                if placeholder_buscado.lower() in placeholder.lower():
                    placeholder_password = placeholder
                    imprimir(f"✅ POSIBLE campo password: placeholder='{placeholder}'")
                    campo_password = input_elem
                    break
        
        # 5. SI NO ENCONTRÓ POR PLACEHOLDER, BUSCAR POR TYPE
        if 'campo_email' not in locals():
            imprimir("🔍 Buscando por type='email'...")
            try:
                campo_email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                imprimir("✅ Encontrado input[type='email']")
            except:
                imprimir("❌ No hay input[type='email']")
        
        if 'campo_password' not in locals():
            imprimir("🔍 Buscando por type='password'...")
            try:
                campo_password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                imprimir("✅ Encontrado input[type='password']")
            except:
                imprimir("❌ No hay input[type='password']")
        
        # 6. VERIFICAR SI TENEMOS LOS CAMPOS
        campos_encontrados = []
        
        if 'campo_email' in locals():
            campos_encontrados.append(("email", campo_email))
        
        if 'campo_password' in locals():
            campos_encontrados.append(("password", campo_password))
        
        if len(campos_encontrados) < 2:
            imprimir("❌ NO SE ENCONTRARON AMBOS CAMPOS")
            imprimir("📸 Tomando screenshot detallado...")
            driver.save_screenshot("02_error_campos.png")
            
            # Mostrar HTML de la página (primeros 2000 chars)
            imprimir("📄 HTML (primeros 2000 caracteres):")
            imprimir(driver.page_source[:2000])
            
            return False
        
        # 7. LLENAR CAMPOS
        imprimir("📝 LLENANDO CAMPOS...")
        
        for nombre, campo in campos_encontrados:
            if nombre == "email":
                campo.clear()
                campo.send_keys(usuario)
                imprimir(f"✅ Email escrito: {usuario}")
                esperar_tiempo(1, 2)
            elif nombre == "password":
                campo.clear()
                campo.send_keys(password)
                imprimir("✅ Password escrito")
                esperar_tiempo(1, 2)
        
        # 8. BUSCAR BOTÓN - ESTRATEGIA AGGRESIVA
        imprimir("🔍 BUSCANDO BOTÓN DE SUBMIT...")
        
        # Tomar screenshot ANTES del clic
        driver.save_screenshot("03_antes_del_login.png")
        
        # Intentar todos los métodos
        boton_encontrado = False
        
        # Método 1: Buscar por texto en botones
        try:
            botones = driver.find_elements(By.TAG_NAME, "button")
            imprimir(f"📊 Encontrados {len(botones)} botones")
            
            for i, boton in enumerate(botones):
                texto = boton.text.strip()
                imprimir(f"   Botón {i}: '{texto}'")
                
                if texto and len(texto) > 0:
                    texto_lower = texto.lower()
                    if any(palabra in texto_lower for palabra in ['iniciar', 'entrar', 'login', 'sign', 'continuar', 'siguiente']):
                        imprimir(f"✅ HACIENDO CLIC en botón: '{texto}'")
                        boton.click()
                        boton_encontrado = True
                        break
        except Exception as e:
            imprimir(f"❌ Error buscando botones: {e}")
        
        # Método 2: Buscar input type="submit"
        if not boton_encontrado:
            try:
                inputs_submit = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
                if inputs_submit:
                    imprimir(f"✅ HACIENDO CLIC en input[type='submit']")
                    inputs_submit[0].click()
                    boton_encontrado = True
            except:
                pass
        
        # Método 3: Usar ENTER
        if not boton_encontrado:
            imprimir("⚠️ No se encontró botón, usando ENTER...")
            from selenium.webdriver.common.keys import Keys
            campo_password.send_keys(Keys.RETURN)
            boton_encontrado = True
        
        # 9. ESPERAR Y VERIFICAR
        imprimir("⏳ ESPERANDO RESPUESTA...")
        esperar_tiempo(6, 10)
        
        # Tomar screenshot DESPUÉS
        driver.save_screenshot("04_despues_del_login.png")
        imprimir(f"📍 URL después: {driver.current_url}")
        imprimir(f"📄 Título después: {driver.title}")
        
        # 10. VERIFICAR SI ESTAMOS LOGUEADOS
        # Buscar texto que indique éxito
        page_text = driver.page_source.lower()
        
        indicadores_exito = ['mis anuncios', 'mi cuenta', 'cerrar sesión', 'salir', 'mis-anuncios']
        indicadores_fracaso = ['contraseña incorrecta', 'email incorrecto', 'error', 'invalid']
        
        exito = False
        for indicador in indicadores_exito:
            if indicador in page_text or indicador in driver.current_url.lower():
                imprimir(f"✅ INDICADOR DE ÉXITO: '{indicador}' encontrado")
                exito = True
        
        for indicador in indicadores_fracaso:
            if indicador in page_text:
                imprimir(f"❌ INDICADOR DE FRACASO: '{indicador}' encontrado")
                exito = False
        
        if exito:
            imprimir("🎉 LOGIN EXITOSO (según indicadores)")
            return True
        else:
            imprimir("⚠️ LOGIN INCIERTO - Revisar screenshots")
            return True  # Intentar continuar de todas formas
        
    except Exception as e:
        imprimir(f"💥 ERROR CRÍTICO: {str(e)}")
        imprimir("📸 Guardando screenshot de error...")
        try:
            driver.save_screenshot("error_final.png")
        except:
            pass
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