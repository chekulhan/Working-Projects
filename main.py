import flet as ft
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
    Image
)

import requests
import json
def main(page: ft.Page):
    lv = ft.ListView(expand=True, spacing=10)
    
    txt_country = ft.TextField(label="My country is ...")
    txt_capital = ft.TextField(label="and the capital city is ...")
    color_dropdown = ft.Dropdown(
        width=100,
        options=[ft.dropdown.Option("Red"),
        ft.dropdown.Option("Green"),
        ft.dropdown.Option("Blue")],
    )

    def getUsers(e):
        sURL = "https://d9291055.eu-gb.apigw.appdomain.cloud/main/contacts" #"https://jsonplaceholder.typicode.com/todos"
        response = requests.get(sURL)
        users = response.json()
  
        for user in users: # list of dictionaries)
            lv.controls.append(ft.Text(user["title"]),
           # icon=Image(src="https://cdn-icons-png.flaticon.com/512/1384/1384033.png", fit="contain"),
                )
        
        page.update()

    def getCloudCountries(e):
        sURL = "https://d9291055.eu-gb.apigw.appdomain.cloud/creativity/countries" 

        header = {"content-type": "application/json"}
        #params={'q': 'requests+language:python'}
        response = requests.get(sURL, headers=header)

        response_data_raw = response.json()
        countries_raw = response_data_raw["countries"]
        if int(countries_raw["total_rows"]) > 0:
            countries = countries_raw["rows"]
            for country in countries: # list of dictionaries
                country_obj = country["doc"]
                lv.controls.append(ft.Text(country_obj["capital"]))

            page.update()

    def saveCloudCountries(country, capital):
        sURL = "https://d9291055.eu-gb.apigw.appdomain.cloud/creativity/countries" 

        header = {"content-type": "application/json"}
        params={"country": country}
        response = requests.post(sURL, headers=header, data=params)
        print(response)


    def btn_save(e):
        if not txt_country.value:
            txt_country.error_text = "Please enter a name for a country. Be creative!"
            page.update()

        else:
            country = txt_country.value
            capital = txt_capital.value
            saveCloudCountries(country, capital)
            #selected_colour=color_dropdown.value
            #page.clean()
            page.add(ft.Text(f"{country} is a great name for a country!"))

    
    page.add(txt_country, txt_capital, lv, ft.ElevatedButton("Save your creativity!", on_click=btn_save), ft.ElevatedButton("See other people's creativity", on_click=getCloudCountries))

#ft.app(target=main)
ft.app(port=8550, target=main)