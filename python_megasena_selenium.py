from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import math
import queue
import multiprocessing
from datetime import datetime

def get_table_len():

    start_time=datetime.now().strftime("%H:%M:%S")
    print('start time:',start_time)
    load_failed=False
    tentativas=15


    try:
        browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    except Exception as e:
        print(e)

    MEGASENA_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx" 
    browser.get(MEGASENA_URL)

    timeout = 10 
    try:
        element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
        WebDriverWait(browser, timeout).until(element_present)
    except :
        print("Timed out na tentativa de carregamento da página principal em get_table_len")
        time.sleep(2)
        load_failed=True

    while load_failed==True and tentativas > 0 :
        browser.refresh()
        time.sleep(10)
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas de carregamento da pagina falharam...')
                exit()
        else:
            load_failed=False

    tentativas=15

    browser.maximize_window()


    timeout = 10 
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/button[3]'))
        WebDriverWait(browser, timeout).until(element_present)
    except :
        print("Botão de aceite não localizado na página principal.")
        time.sleep(2)
        load_failed=True

    while load_failed==True and tentativas > 0 :
        browser.refresh()
        time.sleep(10)
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/button[3]'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas falharam...')
                exit()
        else:
            load_failed=False

    tentativas=15

    clicar=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/button[3]') 
    time.sleep(2)
    clicar.click()


    
    RESULTADOS_URL=browser.find_element(By.CSS_SELECTOR, "#resultados > div > ul > li > a")
    time.sleep(2)
    RESULTADOS_URL.click()
    time.sleep(2)

    browser.switch_to.window(browser.window_handles[1])

    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/thead/tr/th[1]/small'))
        WebDriverWait(browser, timeout).until(element_present)
    except:
        print('Link dos resultados anteriores não encontrado.')
        load_failed=True
        browser.refresh()

    while load_failed==True and tentativas > 0 :
        browser.refresh()
        time.sleep(10)
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/thead/tr/th[1]/small'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas falharam...')
                exit()
        else:
            load_failed=False

    HEADERS = browser.find_elements(By.TAG_NAME, "th")
    time.sleep(2)

    cols = []
    for h in HEADERS:
        cols.append(h.text)

    last_element = browser.find_elements(
        By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/tbody[last()]/tr/td[1]')

    time.sleep(2)

    total_len = int(str(last_element[0].text).replace('[', '').replace(']', '').replace('\'', ''))
    time.sleep(2)

    with open(r'C:\\Users\\thiag\\Desktop\\new_data\\HEADERS_test.txt', 'w') as fp:
        fp.write("\n".join(str(item) for item in cols))
        fp.close()

    browser.close()
    browser.quit()
    return total_len
            
total_len = get_table_len()

def return_p(total_processes,total_len):
    if (total_len % total_processes)== 0:
        p=int(total_len / total_processes)
        p1=int(total_len / total_processes)
        
    else:
        
        p1=total_len - (((math.floor(total_len /total_processes ) * (total_len % total_processes))))
        p=(math.floor(total_len /total_processes ))
    return p1,p


p1, p = return_p(10, total_len)

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

def get_megasena_results(f_p,t_p, sufix):

    start_time=datetime.now().strftime("%H:%M:%S")
    print('start time:',start_time)
    load_failed=False
    tentativas=15

    try:
        browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    except Exception as e:
        print(e)
        

    MEGASENA_URL = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx" 
    browser.get(MEGASENA_URL)

    timeout = 10 
    try:
        element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
        WebDriverWait(browser, timeout).until(element_present)
    except :
        print("Timed out na tentativa de carregamento da página principal em get_table_len")
        print('Processo:',sufix)
        time.sleep(2)
        load_failed=True

    while load_failed==True and tentativas > 0 :
        browser.refresh()
        time.sleep(40)
        timeout = 40
        try:
            element_present = EC.presence_of_element_located((By.ID, 'PlaceHolderMain_g_8948ce2c_ab1a_4e3c_95ec_8eb3565a1df1'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas de carregamento da pagina falharam...')
                exit()
        else:
            load_failed=False

    tentativas=15

    browser.maximize_window()


    timeout = 10 
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/button[3]'))
        WebDriverWait(browser, timeout).until(element_present)
    except :
        print("Botão de aceite não localizado na página principal.")
        time.sleep(2)
        load_failed=True

    while load_failed==True and tentativas > 0 :
        browser.refresh()
        time.sleep(40)
        timeout = 40
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/button[3]'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas falharam...')
                exit()
        else:
            load_failed=False

    tentativas=15
   
    clicar=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/button[3]') 
    time.sleep(2)
    clicar.click()



    RESULTADOS_URL=browser.find_element(By.CSS_SELECTOR, "#resultados > div > ul > li > a")
    time.sleep(2)
    RESULTADOS_URL.click()
    time.sleep(2)

    browser.switch_to.window(browser.window_handles[1])

    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/thead/tr/th[1]/small'))
        WebDriverWait(browser, timeout).until(element_present)
    except:
        print('Link dos resultados anteriores não encontrado.')
        load_failed=True
        browser.refresh()

    while load_failed==True and tentativas > 0 :
        print('while')
        browser.refresh()
        time.sleep(40)
        timeout = 40
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/thead/tr/th[1]/small'))
            WebDriverWait(browser, timeout).until(element_present)
            
        except:
            if tentativas > 0:
                tentativas = tentativas - 1
                print('Tentando novamente...')

            else:
                print('Todas as tentativas falharam...')
                exit()

        else:
            load_failed=False
            
    data_el = []
    for i in range(f_p, t_p + 1):
        for z in range(1, 22):
            data_el.append(browser.find_element(
                By.XPATH, '//*[@id="ctl50_g_cf05b8d5_fd75_46b5_bdfa_a623e654362c"]/div/div/table/tbody['+str(i)+']/tr/td['+str(z)+']').text)

    time.sleep(2)
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
