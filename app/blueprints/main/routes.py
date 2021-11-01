from flask import render_template, request
import requests
from .forms import EnterPokemonForm
from flask_login import login_required
from .import bp as main

@main.route('/')
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = EnterPokemonForm()
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        pokemon = response.json()
        if response.ok:
            stats = {
                "name": pokemon["forms"][0]["name"],
                "hp": pokemon["stats"][0]["base_stat"],
                "defense": pokemon["stats"][2]["base_stat"],
                "attack": pokemon["stats"][1]["base_stat"],
                "shiny": pokemon["sprites"]["front_shiny"]
                }
            return render_template('search.html.j2', stats=stats, form=form)
    return render_template('search.html.j2', form=form)