import time

tentativas=10


while tentativas > 0:
        print('tentativa de número ',tentativas)
        time.sleep(3)

        if tentativas == 5:
            print('saindo')
            exit()
        tentativas= tentativas - 1
