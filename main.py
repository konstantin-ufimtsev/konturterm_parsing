import konturterm
import megapolys
import td_stroitel
import baucenter
import time

def main():
    start = time.perf_counter()
    konturterm.main()
    td_stroitel.main()
    megapolys.main()
    baucenter.main()
    end = time.perf_counter()
    print('Время выполнения:', end - start)
if __name__ == '__main__':
    main()

