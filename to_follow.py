import time
import random
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import logging
import traceback


class InstagramBot:
    def __init__(self, username, password, cookies_path="cookies.pkl"):
        self.username = username
        self.password = password
        self.cookies_path = cookies_path
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(3, 5))

        # Tenta carregar cookies
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, "rb") as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                # Corrige erro de domínio
                if 'sameSite' in cookie:
                    if cookie['sameSite'] == 'None':
                        cookie['sameSite'] = 'Strict'
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    pass
            driver.refresh()
            time.sleep(random.uniform(3, 5))
            # Verifica se está logado
            if self.is_logged_in():
                print("[+] Login via cookies!")
                return

        # Login manual
        # user_input = driver.find_element(By.NAME, "username")
        # pass_input = driver.find_element(By.NAME, "password")

        # user_input.send_keys(self.username)
        # time.sleep(random.uniform(1, 2))
        # pass_input.send_keys(self.password)

        # pass_input.send_keys(Keys.RETURN)
        # time.sleep(random.uniform(4, 7))  # espera login
        # time.sleep(35)

        # # Salva cookies após login
        # with open(self.cookies_path, "wb") as f:
        #     pickle.dump(driver.get_cookies(), f)
        # print("[+] Cookies salvos!")


    def is_logged_in(self):
        driver = self.driver
        try:
            driver.find_element(By.XPATH, "//img[contains(@alt, 'Foto do perfil')]" )
            return True
        except Exception:
            return False


    def acessar_perfil(self, url_perfil):
        self.driver.get(url_perfil)
        time.sleep(random.uniform(3, 6))


    def abrir_seguidores(self):
        driver = self.driver
        # Clica no número de seguidores
        seguidores_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "seguidores")
        seguidores_btn.click()
        time.sleep(random.uniform(3, 5))


    def seguir_pessoas(self, qtd):
        driver = self.driver

        # Encontra o modal principal
        modal = driver.find_element(By.XPATH, "//div[@role='dialog']")

        seguidos = 0
        while seguidos < qtd:
            # Dentro do modal, pegar todos botões com texto "Seguir"
            botoes = modal.find_elements(By.XPATH, ".//button[normalize-space()='Seguir']")

            for botao in botoes:
                if seguidos >= qtd:
                    break
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                    time.sleep(random.uniform(1, 2))
                    botao.click()
                    seguidos += 1
                    print(f"[+] Seguiu {seguidos} pessoas as {time.strftime('%H:%M:%S')}")
                    time.sleep(random.uniform(60, 120))  # delay aleatório
                except Exception as e:
                    print("Erro ao clicar:", e)

            # Scroll no modal para carregar mais perfis
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", modal)
            time.sleep(random.uniform(2, 4))


    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    user= os.environ.get("IG_USERNAME") or input("Digite seu usuário do Instagram: ")
    pw= os.environ.get("IG_PASSWORD") or input("Digite sua senha: ")

    #qtd = int(input("Quantas pessoas deseja seguir? ( We recommend up to 35 per session ): "))

    bot = InstagramBot(user, pw)
    bot.login()
    bot.acessar_perfil("https://www.instagram.com/mundolingo/")
    bot.abrir_seguidores()
    #bot.seguir_pessoas(qtd)
    bot.close()