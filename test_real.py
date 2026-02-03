"""
TEST REAL DEL SISTEMA
Verifica si realmente funciona la renovación
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurar navegador VISIBLE (no headless) para ver qué pasa
options = Options()
options.add_argument("--window-size=1200,800")
# options.add_argument("--headless")  # COMENTADO para ver qué pasa

driver = webdriver.Chrome(options=options)

try:
    print("1. Yendo a login...")
    driver.get("https://www.revolico.com/auth/signin")
    time.sleep(3)
    
    print("2. Haciendo login...")
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    
    email.send_keys("anielvarela6@gmail.com")
    time.sleep(1)
    password.send_keys("hesoyam2")
    time.sleep(1)
    
    boton = driver.find_element(By.XPATH, "//button[contains(text(), 'Iniciar sesión')]")
    boton.click()
    time.sleep(5)
    
    print(f"3. URL después login: {driver.current_url}")
    
    print("4. Yendo a un anuncio de prueba...")
    # PON AQUÍ LA URL DE UN ANUNCIO QUE SÍ SEA TUYO
    driver.get("https://www.revolico.com/item/51214616/_/manage")
    time.sleep(5)
    
    print("5. Buscando botón de renovar...")
    botones = driver.find_elements(By.TAG_NAME, "button")
    for i, b in enumerate(botones):
        if b.text:
            print(f"   Botón {i}: '{b.text}'")
    
    input("\n⚠️ MIRA LA PANTALLA: ¿Ves botón 'Renovar'? Presiona Enter...")
    
    print("6. Tomando screenshot...")
    driver.save_screenshot("test_real.png")
    print("✅ Screenshot guardado: test_real.png")
    
finally:
    driver.quit()