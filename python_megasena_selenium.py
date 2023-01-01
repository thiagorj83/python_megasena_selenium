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

# Esta função calcula quantas linhas serão lidas por cada computação paralela
def return_p(total_processes,total_len):
    if (total_len % total_processes)== 0:
        p=int(total_len / total_processes)
        p1=int(total_len / total_processes)
        
    else:
        
        p1=total_len - (((math.floor(total_len /total_processes ) * (total_len % total_processes))))
        p=(math.floor(total_len /total_processes ))
    return p1,p




p1, p = return_p(10, total_len)

# Esta função cria duas FIFO com 10 elementos cada: uma para o elemento inicial e outra para o elemento final
# de cada linha que deverá ser lida da tabela de resultados da mega sena
def gen_from_to(p1, p, total_processes):
    from_p = queue.Queue(total_processes)
    to_p = queue.Queue(total_processes)
    y = 0
    z = 0
    for i in range(total_processes):

        if i < 2:
            from_p.put((p1 * y) + (z * p)+1)
            to_p.put(p1 + (i * p) )
            y = y+1
        else:
            from_p.put(p1 + ((i - 1) * p)+1)
            to_p.put(p1 + (i * p) )

    return from_p, to_p

from_p, to_p = gen_from_to(p1, p, 10)

# Esta função acessa a tabela de resultados e recupera os nomes das colunas e os dados de cada linha
def get_megasena_results(f_p,t_p, sufix):

    start_time=datetime.now().strftime("%H:%M:%S")
    print('start time:',start_time)
    load_failed=False
    tentativas=10
    # Configura o webdriver.chrome em uma variável chamada browser

    try:
        browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    except Exception as e:
        print(e)
        
    browser.implicitly_wait(10)


    # Acessa a página da megasena

    MEGASENA_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx" 
    browser.get(MEGASENA_URL)

    # Maximiza a página atualmente aberta
    browser.maximize_window()

    timeout = 45 
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
    # Muda a target screen para a página resultados recentemente aberta  
    browser.switch_to.window(browser.window_handles[1])

    timeout = 15
    try:
        element_present = EC.presence_of_element_located((By.ID, 'ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c'))
        WebDriverWait(browser, timeout).until(element_present)
    except:
        print("Timed out waiting for page to load - 2 in process"+str(sufix))
        load_failed=True

    while load_failed==True and tentativas > 0 :

        timeout = 15
        try:
            element_present = EC.presence_of_element_located((By.ID, 'ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            print("Timed out waiting for page to load - 2 in process"+str(sufix))
            browser.refresh()
            tentativas = tentativas - 1
        finally:
            load_failed=False
            
    # De posse do número total de linhas, efetua-se a raspagem dos dados de todos os sorteios já realizados
    # Cria data frame com os dados obtidos
    data_el = []
    for i in range(f_p, t_p + 1):
        for z in range(1, 22):
            data_el.append(browser.find_element(
                By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/tbody['+str(i)+']/tr/td['+str(z)+']').text)

    time.sleep(5)
    with open('C:\\Users\\thiag\\Desktop\\new_data\\megasena_data' + str(sufix) + '.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(data_el)
    finish_time=datetime.now().strftime("%H:%M:%S")
    print('Finish time:',finish_time)


processes = []

for x in range(10):
    f_p = from_p.get()
    t_p = to_p.get()
    procx = multiprocessing.Process(target=get_megasena_results,args=[f_p,t_p,x])
    if __name__ == "__main__":

        procx.start()
        processes.append(procx)

for procx in processes:
    procx.join()
