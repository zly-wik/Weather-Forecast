import sys
import json
from datetime import datetime

import requests
from geopy.geocoders import Nominatim


class GetMeteoData:    
    def get_meteo_data(city: str | None=None, date: str | None=None) -> None:
        city, date = GetMeteoData.validate_input_data(city, date)
        
        try:
            latitude, longitude = GetMeteoData.get_coordinates_of_city(city)
        
            if not latitude and not longitude:
                return
            latitude = round(latitude, 2)
            longitude = round(longitude, 2)
        
            api_data = GetMeteoData.get_data_from_api(latitude, longitude, date)
            if api_data:
                GetMeteoData.print_data(data=api_data, city=city, date=date)
        except:
            print('Failed to find given location.')
    
    
    def get_coordinates_of_city(city: str) -> tuple:
        geolocator = Nominatim(user_agent='ZlyWik')
        
        location = geolocator.geocode(city)
        return (location.latitude, location.longitude)
          

    def validate_input_data(city: str, date: str) -> tuple:
        if not city:
            city = 'Wrocław'
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        else:
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                date = date.strftime('%Y-%m-%d')
            except:
                print('Failed to read date, using default (today)\n')
                date = datetime.today().strftime('%Y-%m-%d')
    
        return city, date
    
    
    def get_data_from_api(latitude: float, longitude: float, date: str) -> str|None:
        url: str = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation&start_date={date}&end_date={date}'
            
        req = requests.get(url)
        if req.status_code != 200:
            print('Failed to reach the open-meteo.com API\n')
            return None
        
        return req.content

    
    def print_data(data: str, city: str, date: str) -> None:
        formatted_data = GetMeteoData.format_data(data, city, date)
        print(formatted_data)
        
    
    
    def extract_data(time_array, temperature_array, precipitation_array) -> list[tuple[str]]:
        extracted_data: list[tuple[str]] = list()

        for time, temperature, precipitation in zip(time_array, temperature_array, precipitation_array):
            time = datetime.strptime(time, '%Y-%m-%dT%H:%M').strftime('%H:%M')
            temperature = GetMeteoData.format_temperature(str(temperature))
            extracted_data.append((time, temperature, str(precipitation)+'mm'))
            
        return extracted_data
    
        
    def format_data(data: str, city: str, date: str) -> str:
        json_data: str = json.loads(data)
        json_data: str = json_data['hourly']
        
        extracted_data = GetMeteoData.extract_data(json_data['time'], json_data['temperature_2m'], json_data['precipitation'])
        
        formatted_data = f'\n{city}, {date}\n'
        formatted_data += f"Hour{' '*5}Temp{' '*7}Precipitation{' '*5}"
        formatted_data += f"Hour{' '*5}Temp{' '*5}Precipitation\n"
        
        for i in range(0, 12):
            formatted_data += f"{extracted_data[i][0]}{(' '*(9-len(extracted_data[i][1])))}{extracted_data[i][1]}{' '*(11-len(extracted_data[i][2]))}{extracted_data[i][2]}{' '*10}|{' '*2}{extracted_data[12+i][0]}{(' '*(9-len(extracted_data[12+i][1])))}{extracted_data[12+i][1]}{' '*(9-len(extracted_data[i][2]))}{extracted_data[12+i][2]}\n"
        
        return formatted_data
    
    
    def format_temperature(temperature_str: str) -> str:
        temperature_str =  temperature_str if temperature_str[0] == '-' else ' ' + temperature_str
        return temperature_str + '*C'