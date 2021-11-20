from flask import Flask, jsonify, request as flask_request
from bs4 import BeautifulSoup
import requests
import os

app = Flask('app')

@app.route('/')
def api_wikipedia():
    """
    Rota que devolve dados de uma página no wikipedia.
    :return:  jsonify
    """
    search = flask_request.args.get('search', None)
    data = []
    url = flask_request.url
    if search:
        search = search.split(',')
        for argument in search:
            search_index = search.index(argument)
            api_wikipedia = 'https://pt.wikipedia.org/wiki/{}'.format(argument)
            r_api = requests.get(api_wikipedia)
            if r_api.status_code != 200:
                return jsonify({'detail': 'Não conseguimos encontrar nada com o parametro indicado.'})
            r_api_bs = BeautifulSoup(r_api.text, 'html.parser')
            title = r_api_bs.find(id='firstHeading')
            body = r_api_bs.find(id='bodyContent')
            div_class_table = r_api_bs.find_all('div', attrs={'class': 'mw-parser-output'})
            div_class_table = div_class_table[0]
            p_from_table = div_class_table.find('p')
            data.append({
                'titulo': title.text,
                'description': p_from_table.text,
                'index': search_index,
            })
        return jsonify(data)
    else:
        return jsonify({
            'detail': 'Erro, você precisa informar um parametro de busca!',
            'example': '{}?search=<SUA_BUSCA_AQUI>'.format(url),
            'detail2': 'Você pode inserir varias buscas, separando por virgula.'
        })


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
