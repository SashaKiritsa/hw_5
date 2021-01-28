from flask import Flask
from flask import render_template
# from faker import Faker
import requests
import csv
from base58 import b58decode, b58encode

# fake = Faker()

app = Flask (__name__)


@app.route('/')
@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

"""
1. Возвращать содержимое файла с Python пакетами (requirements.txt)
"""
@app.route('/requirements/', methods=['GET', 'POST'])
def requirements():
    with open('requirements.txt') as File:
        data = File.read()
        requirements=[]
        for word in data.split():
            requirements.append(word)
    return render_template('requirements.html', requirements=requirements)

"""
4. Вывести количество космонавтов, находящихся в настоящий момент на орбите
"""

# @app.route('/mail_generate/', methods = ['GET', 'POST'])
# def mail_generate():
#     name = fake.name()
#     email = fake.email()


@app.route('/cosmo/', methods = ['GET', 'POST'])
def cosmo():
    r = requests.get('http://api.open-notify.org/astros.json')
    count = (r.json()["number"])
    return render_template('cosmo.html', count=count)




"""
3.Вернуть значения среднего роста (в сантиметрах) и среднего веса (в килограммах)
Необходимые данные расположены в файле hw05.csv
Анализировать файл hw.csv нужно при каждом вызове
"""
@app.route('/file_csv/', methods = ['GET', 'POST'])
def file_csv():
    with open('hw05.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True, delimiter= ',')
        middle_height = 0
        middle_weight = 0
        count_str = 0
        i = 0

        for row in reader:
            if count_str == 0:
                count_str += 1
                
            else:
                try:
                    middle_height += round(float(row[1]))
                    middle_weight += round(float(row[2]))
                    i += 1
                except IndexError:
                    break
           
        middle_height = round(middle_height/i, 2)
        middle_weight = round(middle_weight/i ,2)
    return render_template('file_csv.html', middle_height=middle_height, middle_weight=middle_weight, i=i)

"""
5. Закодировать входную строку `STRING` в формате base58
"""
@app.route('/base58/<string:s>/', methods= ['GET', 'POST'])
def base58(s):
    
    if ' ' in s:
        return '<h1>В этом запросе не должно быть пробелов</h1>'
    else:
        return b58encode(s)
    return render_template ('base58.html', s=s)


"""
6. Преобразовать строку `STRING_IN_BASE58` в формате *base58* в исходную строку
"""
@app.route('/base58decode/<string:s>/', methods= ['GET', 'POST'])
def base58decode(s):
    if ' ' in s:
        return '<h1>В этом запросе не должно быть пробелов</h1>'
    else:
        return b58decode(s)
    return render_template ('base58decode.html', s=s)
    













if __name__ == '__main__':
    app.run(debug=True)
    





