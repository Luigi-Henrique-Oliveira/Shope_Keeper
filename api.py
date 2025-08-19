from flask import Flask, jsonify
import pandas as pd 
import requests 
from bs4 import BeautifulSoup
import html

app = Flask(__name__) 


def get_items():
    url = "https://bindingofisaacrebirth.fandom.com/wiki/Items" 
    pagina = requests.get(url) 
    tables1 = pd.read_html(url)
    df1 = tables1[0] 
    Name1 = df1["Name"]
    QY1 = df1["Quality"]

    tables2 = pd.read_html(url) 
    df2 = tables2[1] 
    Name2 = df2["Name"] 
    QY2 = df2["Quality"] 

    Name_final = pd.concat([Name1 , Name2], ignore_index=True)
    QY_final = pd.concat([QY1 , QY2], ignore_index=True) 



    df_final = df_final.applymap(lambda x: html.unescape(str(x)).strip())

    list_dict = df_final.to_dict(orient="records")


    dados = BeautifulSoup(pagina.text, "html.parser" ) 
    todas_img = dados.find_all("img" , class_ ="mw-file-element lazyloaded") 
    img_list = [img["src"] for img in todas_img if img.get("src")]


    df_final = pd.DataFrame({ 
        "Name": Name_final, 
        "QY": QY_final, 
        "Img": img_list
    }) 

    for item in list_dict:
        item["img_urls"] = img_list

    return list_dict


@app.route("/")
def home():
    data = get_items()
    return  jsonify(data)


app.run(debug=True,host="0.0.0.0")