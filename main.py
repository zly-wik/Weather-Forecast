import sys
import requests_cache
from GetMeteoData import GetMeteoData


def main():
    requests_cache.install_cache('cache', backend='sqlite', expire_after=300)
    
    city: str = ''
    date: str = ''
    
    if len(sys.argv) > 1:
        city = sys.argv[1]
        if len(sys.argv) > 2:
            date = sys.argv[2]
    else:
        city = input('Enter city (default: Wrocław): ')
        date = input('Enter date [YYYY-mm-dd] (default: today): ')

    GetMeteoData.get_meteo_data(city=city, date=date)
    
    
if __name__ == '__main__':
    main()