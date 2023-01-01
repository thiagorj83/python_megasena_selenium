# python_megasena_selenium
Algoritmo em python que efetua webscrapping na página de resultados da Mega Sena utilizando Selenium.

Este algoritmo efetua o web scraping , também conhecido como extração de dados da web, que é um processo de coleta de dados estruturados da web de maneira automatizada.
A página alvo é a de resultados da Mega Sena, sorteio realizado pela Caixa Econômica Federal aqui no Brasil.
Selenium é um framework portátil para testar aplicativos web. Ele fornece uma ferramenta de reprodução para a criação de testes 
funcionais sem a necessidade de aprender uma linguagem de script de teste (Selenium IDE).

## Instalação do Selenium

Eu utilizei o **ChromeDriver**, uma ferramenta opensource para efetuar testes automatizados em páginas na internet específica para o navegador
**Chrome**, da Google.
Para efetuar o download, visite a página ***https://chromedriver.chromium.org/downloads*** e baixe a versão de mesmo número da versão de seu navegador
**Chrome**.


## Descrição do algoritmo

O algoritmo começa com a **importação das bibliotecas necessárias** ao funcionamento das funções e métodos utilizados.

          from selenium import webdriver
          import time
          from selenium.webdriver.common.by import By
          from selenium.webdriver.support.ui import WebDriverWait
          from selenium.webdriver.support import expected_conditions as EC
          import csv
          import math
          import queue
          import multiprocessing
          from datetime import datetime
          
A primeira função, ***get_table_len()***, efetua a captura do número do último sorteio realizado até o momento.
Isso permite saber quantas linhas há na tabela para que posteriormente se efetue a iteração na leitura de cada linha presente nela.

          def get_table_len():

              start_time=datetime.now().strftime("%H:%M:%S")
              print('start time:',start_time)
              load_failed=False
              tentativas=5
              # Configura o webdriver.chrome em uma variável chamada browser

              try:
                  browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
              except Exception as e:
                  print(e)

              # Este método define um tempo limite fixo para esperar 
              # implicitamente que um elemento seja encontrado ou que um comando seja concluído.
              browser.implicitly_wait(10)


              # Acessa a página da megasena

              MEGASENA_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx" 
              browser.get(MEGASENA_URL)

              # Maximiza a página atualmente aberta
              browser.maximize_window()

              # Este trecho espera 10 segundos para detectar se um elemento da tela já se encontra visível
              # Caso esteja, indica indiretamente que a tela foi carregada;senão, lança uma excessão e aguarda mais 10 segundos.
              timeout = 10 
              try:
                  element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
                  WebDriverWait(browser, timeout).until(element_present)
              except :
                  print("Timed out waiting for page to load - 1")
                  time.sleep(10)

              # Efetua clique em "aceitar" no banner aberto sobre a página principal com objetivo de fechá-lo e permitir
              # o controle remoto da página pelo selenium

              clicar=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/button[3]') 
              time.sleep(5)
              clicar.click()


              # Efetua o clique no link de resultados de jogos anteriores da megasena
              RESULTADOS_URL=browser.find_element(By.CSS_SELECTOR, "#resultados > div > ul > li > a")
              time.sleep(3)
              RESULTADOS_URL.click()
              time.sleep(5)
              # Muda a target screen para a página de resultados que acabou de ser carregada
              browser.switch_to.window(browser.window_handles[1])

              # Este trecho tenta detectar por 10 segundos um elemento da tabela de resultados;
              # Em caso negativo, lança uma excessão e muda a variável load_failed para True.
              timeout = 10
              try:
                  element_present = EC.presence_of_element_located((By.ID, 'ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c'))
                  WebDriverWait(browser, timeout).until(element_present)
              except:
                  load_failed=True

              # Após a excessão anterior, este loop tenta detectar por 10 vezes um elemento da tabela de resultados
              # Para cada tentativa falha, atualiza a tela com o objetivo de que ela seja recarregada.
              while load_failed==True and tentativas > 0 :

                  timeout = 10
                  try:
                      element_present = EC.presence_of_element_located((By.ID, 'ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c'))
                      WebDriverWait(browser, timeout).until(element_present)

                  except:
                      browser.refresh()
                      tentativas = tentativas - 1
                  finally:
                      load_failed=False

              # Coleta os nomes das colunas da tabela
              HEADERS = browser.find_elements(By.TAG_NAME, "th")
              time.sleep(2)

              # Extrai cada nome de coluna para a variável cols
              cols = []
              for h in HEADERS:
                  cols.append(h.text)

              # Verifica qual é o número do último sorteio registrado na tabela de resultados para saber quantas linhas há no total.

              last_element = browser.find_elements(
                  By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/tbody[last()]/tr/td[1]')
              time.sleep(2)
              # Recupera o número do último sorteio.

              total_len = int(str(last_element[0].text).replace('[', '').replace(']', '').replace('\'', ''))

              time.sleep(2)
              # Salva em arquivo de texto os nomes das colunas
              with open(r'C:\\Users\\thiag\\Desktop\\new_data\\HEADERS_test.txt', 'w') as fp:
                  fp.write("\n".join(str(item) for item in cols))
                  fp.close()

              browser.close()
              browser.quit()
              return total_len
            
total_len = get_table_len()
