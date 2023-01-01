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
Após isso, extraia o arquivo baixado **chromedriver.exe** e o coloque na pasta ***C:\Program Files (x86)***.

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
              
No trecho acima, a variável **start_time** recebe a hora atual para que se tenha o controle de quanto tempo o algoritmo consumiu ao
final de sua execução.
A função **load_failed** é inicializada com o valor 5. Isso rserá usado, posteriormente, no loop que tenta verificar se determinada 
página carregou completamente.

Abaixo temos o tratamento de excessão que verifica se a variável **browser** foi carregada apropriadamente e configurou o webdriver.

              try:
                  browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
              except Exception as e:
                  print(e)
Agora temos o método **implicitly_wait** que aguarda, neste caso, dez (10) segundos até que um elemento seja encontrado ou que um comando seja concluído.

              browser.implicitly_wait(10)


A variável **MEGASENA_URL** recebe o endereço da página específica da Mega Sena.
O método **browser.get** efetua o acesso a página citada.

              MEGASENA_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx" 
              browser.get(MEGASENA_URL)
              
O método **maximize_window** maximiza a página anteriormente aberta.
              
              browser.maximize_window()

A seguir,  cria-se a espera de dez (10) segundos para detectar se um elemento no final da tela já se encontra visível. Isso cria a 
garantia indireta de que se o elemento está visível, a página está carregada. Senão, lança-se a excessão que informa o **timeout** atingido e
espera mais dez (10) segundos.

              timeout = 10 
              try:
                  element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
                  WebDriverWait(browser, timeout).until(element_present)
              except :
                  print("Timed out waiting for page to load - 1")
                  time.sleep(10)
Neste ponto,efetua-se o clique em "aceitar" no banner aberto sobre a página principal com objetivo de fechá-lo e permitir o controle remoto da página pelo selenium.


              clicar=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/button[3]') 
              time.sleep(5)
              clicar.click()
Agora, a variável **RESULTADOS_URL** recebe o resultado do clique sobre o link ***Resultados da Mega-Sena por ordem crescente.***, localizado na seção
**DOWNLOAD DE RESULTADOS**, próximo do fim da página.
Isso abre a página que contém todos os resultados dos concursos anteriores da **Mega sena**.

              RESULTADOS_URL=browser.find_element(By.CSS_SELECTOR, "#resultados > div > ul > li > a")
              time.sleep(3)
              RESULTADOS_URL.click()
              time.sleep(5)
Seguindo, tem-se o método **witch_to.window** que muda a **target screen** para a página recém aberta, de forma que o 
Selenium a tenha como a página alvo.

              browser.switch_to.window(browser.window_handles[1])

Mais uma vez, um tratamento de exceção ocorre. Se em dez (10) segundos um elemento específico da tabela ainda não estiver visível na tela
(**presence_of_element_located**), a variável **load_failed** recebe o valor True. 

              timeout = 10
              try:
                  element_present = EC.presence_of_element_located((By.ID, 'ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c'))
                  WebDriverWait(browser, timeout).until(element_present)
              except:
                  load_failed=True

Após a excessão anterior, o loop **while** tenta detectar por dez (10) vezes um elemento da tabela de resultados a cada dez (10) segundos.
Para cada tentativa falha, atualiza a tela através do método **refresh**  com o objetivo de que ela seja recarregada e o elemento se torne visível.

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
Após a tabela estar complemente visível, efetua-se a coleta dos nomes das colunas.

              HEADERS = browser.find_elements(By.TAG_NAME, "th")
              time.sleep(2)

Aqui cada nome é extraído para a variável **cols**.

              cols = []
              for h in HEADERS:
                  cols.append(h.text)

A variável **last_element** recebe o número do último sorteio registrado na tabela de resultados para saber quantas linhas há no total.

              last_element = browser.find_elements(
                  By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/tbody[last()]/tr/td[1]')
              time.sleep(2)

Na linha a seguir, retira-se símbolos que impediriam a **conversão de tipo** de **string** para **int** e salva o resultado na variável
**total_len**.

              total_len = int(str(last_element[0].text).replace('[', '').replace(']', '').replace('\'', ''))

              time.sleep(2)
              
Chegando ao final, salvam-se os nomes das colunas em um arquivo de texto para posterior consulta.

              with open(r'C:\\Users\\thiag\\Desktop\\new_data\\HEADERS_test.txt', 'w') as fp:
                  fp.write("\n".join(str(item) for item in cols))
                  fp.close()
                  
Por fim, encerra-se o webdriver e retorna o valor do total de sorteios registrados.

              browser.close()
              browser.quit()
              return total_len
            
total_len = get_table_len()
