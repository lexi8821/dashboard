from flask import Flask, render_template, url_for, request
from projects import get_projects, get_names, get_values, splitter, vals
from market import market_data, types, leaders, values, leader_value, leader_percentage
from llama import get_protocols, sort_protocols
import os
from history import get_history, create_dataset
from lending import get_lending_tokens, get_rates, transform_rates, get_lending_projects
app = Flask(__name__)

def tranform_projects(original_data):
    new_projects = list()
    for p in original_data:
        if not p['logo']:
            # So we can make our own logos -> use prinscreen and MS paint to resize and save
            if os.path.isfile(f"static\\img\\{p['name'].lower().strip().replace(' ', '-')}.png"):
                p['img'] = f"static\\img\\{p['name'].lower().strip().replace(' ', '-')}.png"
            else:
            # For cases where there is no logo and we did not created or own
                p['img'] = 'static\\img\\na.png'
        else:
            file_name = p['logo'].split('/')[-1]
            file_path = 'static\\img\\' + file_name
            p['img'] = file_path
        p['tvl'] = format(int(p['tvl']), ',d')
        p['lnk'] = f"/project/{p['name'].lower().replace(' ', '-')}"
        if p['description']:
            if isinstance(p['description'], list):
                p['description'] = ''.join(p['description']).strip()
            else:
                p['descripton'] = p['description'].strip()
        else:
            p['description'] = 'Description not available.'
        new_projects.append(p)
    return new_projects

def sort_projects(projects_dataset):
    pass

@app.route('/')
def index():
    return render_template('index.html')

def make_sorted(protocols, selection):
    if selection == 1:
        return sort_protocols(protocols, 'name', reverse=False)
    elif selection == 2:
        return sort_protocols(protocols, 'name', reverse=True)
    elif selection == 3:
        return sort_protocols(protocols, 'tvl', reverse=True)
    elif selection == 4:
        return sort_protocols(protocols, 'tvl', reverse=False)
    elif selection == 5:
        return sort_protocols(protocols, 'symbol', reverse=False)
    elif selection == 6:
        return sort_protocols(protocols, 'symbol', reverse=True)
    else:
        return sort_protocols(protocols, 'name', reverse=False)


@app.route('/protocols', methods = ['POST', 'GET'])
def protocols():
    old_projects = get_protocols(update=False)
    sorting_options = [[1,'Name A to Z'], [2,'Name Z to A'], [3,'TVL High to Low'],
        [4,'TVL Low to High'], [5,'Symbol A to Z'], [6,'Symbol Z to A']]
    if request.method == 'POST':
        selection = int(request.form.get('sorter_form'))
        old_projects = make_sorted(old_projects, selection)
        new_projects = tranform_projects(old_projects)
        return render_template('protocols.html', projects = new_projects,
            sorting_options=sorting_options, selection=selection)
    else:
        o_projects = make_sorted(old_projects, 3)
        n_projects = tranform_projects(old_projects)
        return render_template('protocols.html', projects = n_projects,
            sorting_options=sorting_options, selection=3)

@app.route('/project/<project_name>')
def project_details(project_name):
    old_projects = get_protocols()
    new_projects = tranform_projects(old_projects)
    projects = dict()
    for item in new_projects:
        name = item['name'].lower().replace(' ', '-')
        projects[name] = item
    return render_template('profile.html', project = projects[project_name])

@app.route('/projects', methods = ['POST', 'GET'])
def dashboard():
    denominations = ['BTC', 'ETH', 'USD']
    projects = get_projects()
    if request.method == 'POST':
        selection = request.form.get('f_denom_form')
        sel_denom = vals(projects, selection)
        labels = [i[0] for i in sel_denom]
        final_denom = [i[1] for i in sel_denom]
        labels = splitter(labels, 4)
        final_denom = splitter(final_denom, 4)
        return render_template('projects.html', names=labels, usds=final_denom, denominations=denominations, selection=selection)
    else:
        values_dict = get_values(projects)
        usds = splitter([i[2] for i in values_dict.values()], 4)
        labels = splitter(list(values_dict.keys()), 4)
        return render_template('projects.html', names=labels, usds=usds, denominations=denominations, selection='USD')

@app.route('/market')
def market():
    data = market_data()
    md_leaders = leaders(data)
    md_types = types(data)
    md_values = values(data)
    md_lvalue = leader_value(data)
    md_lperc = leader_percentage(data)
    return render_template('market.html', types = md_types, values= md_values)

@app.route('/tvl', methods = ['POST', 'GET'])
def tvl():
    projects = get_projects()
    names = [i['name'].lower().strip().replace(' ', '-') for i in projects]
    if request.method == 'POST':
        selection = request.form.get('protSelect')
        h = get_history(selection, 'all')
        h_dataset = create_dataset(h)
        labels = [i[0] for i in list(reversed(h_dataset))]
        values = [i[1] for i in list(reversed(h_dataset))]
        return render_template("tvl.html", protocols=names, selection=selection,
        labels = labels, values= values)
    else:
        return render_template("tvl.html", protocols=names, selection='none')

@app.route('/lending')
def lending():
    projects = get_lending_projects()
    projects_names = [i['name'] for i in projects]
    outstandings = [i['outstanding']['total']['valueUSD'] for i in projects]
    b_rates = [i['borrow_rates']['composite'] for i in projects]
    l_rates = [i['lend_rates']['composite'] for i in projects]
    return render_template("lending.html", projects=projects, names=projects_names)

@app.route('/rates', methods=['GET', "POST"])
def rates():
    tokens = get_lending_tokens()
    if request.method == 'POST':
        selection = request.form.get('t_picker')
        amount = request.form.get('t_amount')
        if not amount:
            amount = 1000
        rates = get_rates(selection, amount)
        rates = transform_rates(rates)
        return render_template("rates.html", tokens=tokens, selection=selection, rates=rates)
    else:
        return render_template("rates.html", tokens=tokens, selection='', rates='')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/learning')
def learning():
    return render_template("learning.html")

if __name__ == '__main__':
    app.run(debug=True)
