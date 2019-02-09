import operator
import re
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Hunch'

'''
A Class used to create a web front end for viewing Hunch results. 
'''
class create_website:

    # The constructor, setting class variables
    # This takes in a list of dictionaries for the individuals to be profiled.
    def __init__(self, list_of_individuals_to_display=[]):
        self.list_of_individuals = []
        self.list_of_individuals_being_scanned = []
        self.list_of_individuals.extend(list_of_individuals_to_display)

    # The function generates the undelaying layout for the whole front end.
    def generate_layout(self):

        # This is used to loop through the individuals and create a list for them
        list_for_dropdown = []
        for individual in self.list_of_individuals:
            list_for_dropdown.append({'label': individual["name"], 'value': individual["name"]})

        # Sets what the HTML page will look like.
        app.layout = app.layout = html.Div([
            html.H1(children='Hunch!'),
            html.Div(
                children='''A Predictive Policing and Threat Aggregation toolset, powered by Natural Language Processing and Open Source Intelligence.'''),
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Prioritization', children=[
                    html.H2(children='Individual Risk Profiles'),
                    html.Div([
                        html.Div([
                            html.Div([dcc.Markdown(
                                "\nA section to view all profiled individuals, sorted and prioritised on their risk.\n"),
                                self.return_prioritised_table()], className="six columns"),

                            html.Div([self.return_prioritised_risk_graph()], className="six columns"),
                        ], className="row")
                    ])
                ]),

                dcc.Tab(label='Profile', children=[
                    html.H2(children='Profile An Individual'),
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Markdown("\nAdd the specifications for an individual to be profiled.\n"),
                                dcc.Input(id='name_input-box', type='text', placeholder='Name...'),
                                dcc.Input(id='handle_and_source_input_box', type='text', placeholder='Handle and Source...'),
                                dcc.Input(id='impact_input_box', type='text',placeholder='Impact...'),
                                html.Button('Submit', id='button'),
                                html.Div(id='output-container-button',
                                         children='Enter a value and press submit')
                            ])
                        ]),
                        html.Div([self.return_inprogress_individuals_table()])
                    ])
                ]),

                # Generates the Third tab, used to compare individuals
                dcc.Tab(label='Analysis', children=[
                    html.Div([
                        html.H2(children="Individuals' Data Comparison"),
                        html.Div(
                            children='''Select an assortment of individuals from the dropdown to dive deeper into their profiles.\n'''),
                        dcc.Dropdown(
                            id='my-dropdown',
                            options=list_for_dropdown,
                            multi=True
                        ),

                        html.Div(id='output-container')]),
                ])
            ], colors={
                "primary": "gold"}
                     )
        ])


    # This function should be moved to a core function. e.g. core profile. Lazy Profile
    def profile_individual(self, list_of_dictionary_individuals, individual_name, impact):

        import Core_Aggregator
        import Core_Individual

        my_aggrigator = Core_Aggregator.WebsiteToCrawl(list_of_dictionary_individuals, individual_name, impact)
        print(
            "\n\nCreated Aggrigator for  " + my_aggrigator.name + ": " + str(my_aggrigator.list_of_dictionary_sources))

        my_individual = Core_Individual.Individual(my_aggrigator.aggregate_data(), my_aggrigator.name)
        print("Beginning profiling " + my_individual.name + "'s " + str(
            len(my_individual._text_to_be_profiled)) + " samples.")

        # Adds individuals name to the list that is used to show the current scans in progress, then re draws the layout
        self.list_of_individuals_being_scanned.append([my_individual.name, datetime.now()])
        self.generate_layout()

        self.list_of_individuals.append(my_individual.profile())


        for item in self.list_of_individuals_being_scanned:
            if item[0] == my_individual.name:
                self.list_of_individuals_being_scanned.remove(item)
                break

        print("Finished adding to list : " + str(self.list_of_individuals))

        #When the profile/ scan is finished the layout is re drawn with the new data
        self.generate_layout()

    # A function used to return a table of all of the profiled individuals prioritised on the highest risk
    def return_inprogress_individuals_table(self):

        # Creates a series of lists that will later be used as colums for the table.
        names = []
        dates = []
        # The below loops through the individuals and assigns their values to each colum
        for individual in self.list_of_individuals_being_scanned:
            names.append(individual[0])
            dates.append(individual[1])

        # This is used to create the table.
        d = {"Profile's In Progress": names, "Date started": dates}
        dataframe = pd.DataFrame(data=d)

        # Returns and generates a html data frame object with the above attributes
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), len(dataframe)))]
        )

    # A function used to return a table of all of the profiled individuals prioritised on the highest risk
    def return_prioritised_table(self):

        # Sorts the list of individuals in order of lower risk first then flips it.
        self.list_of_individuals.sort(key=operator.itemgetter('risk'))
        self.list_of_individuals.reverse()

        # Creates a series of lists that will later be used as colums for the table.
        names = []
        risks = []
        likelihoods = []
        impacts = []

        # The below loops through the individuals and assigns their values to each colum
        for individual in self.list_of_individuals:
            names.append(individual["name"])
            risks.append(individual["risk"])
            likelihoods.append(individual["likelihood"])
            impacts.append(individual["impact"])

        # This is used to create the table.
        d = {'Name': names, 'Risk': risks, 'Likelihood': likelihoods, 'Impact': impacts}
        dataframe = pd.DataFrame(data=d)

        # Returns and generates a html data frame object with the above attributes
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), len(dataframe)))]
        )

    # A function that returns a graph of risk and likelihood for every profiled individual
    def return_prioritised_risk_graph(self):

        # Loops through all profiled individuals and adds their likelihood and risk to a list
        list_for_graph = []
        for individual in self.list_of_individuals:
            list_for_graph.append({'x': [individual["likelihood"]],
                                   'y': [individual["risk"], ],
                                   'type': 'log', 'name': individual["name"],
                                   'mode': 'markers',
                                   'opacity': 0.7,
                                   'marker': {
                                       'size': 15,
                                       'line': {'width': 0.5, 'color': 'white'}
                                   }
                                   })

        # Returns the new graph object, using the aformentioned list
        return dcc.Graph(
            id='graph-1-tabs',
            figure={
                'data': list_for_graph,
                'layout': {
                    'title': "Individuals' Risk Scores"
                }
            }
        )

    # This function returns the analysis graph
    def return_graph(self, value):
        if value:
            if type(value) is not list:
                value = [value]
            # This checks if the indivudals that have been selected in the dropdown are in the list of individuals
            # and if so adds their data to the graph.
            list_for_graph = []
            for user in value:
                for people in self.list_of_individuals:
                    if people["name"] == user:
                        list_for_graph.append({'x': ["Likelihood", "Impact", "Risk"],
                                               'y': [people["likelihood"], people["impact"], people["risk"]],
                                               'type': 'bar', 'name': people["name"]})

            # Returns the new graph object
            return dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': list_for_graph,
                    'layout': {
                        'title': 'Profiled Individuals'
                    }
                }
            )

        # If the value parsed in is not valid returns none
        else:
            return None

    # This function is used to return a populated table with the keywords, name and text in
    def return_table(self, value):
        if value:
            if type(value) is not list:
                value = [value]
            # This checks if the indivudals that have been selected in the dropdown are in the list of individuals
            # and if so adds their data to the graph.
            list_of_extras = []
            for user in value:
                # Loops through each individual finds the extra colum loops through that finding each of their extras, and takes the ectras from the list.

                for people in self.list_of_individuals:
                    for item in people["extra"]:
                        # Createa a list of dictionaries containing a name, type and text for the keywords used.
                        for extra in item["extra"]:
                            if people["name"] == user:
                                extra["name"] = people["name"]
                                if extra not in list_of_extras:
                                    list_of_extras.append(extra)
            names = []
            types = []
            texts = []
            keywords = []
            times = []
            sentiments = []
            # The below adds the aformentioned list to individual colums for a data frame structure
            for item in list_of_extras:
                names.append(item["name"])
                types.append(item["Type"])
                keywords.append(item["Keyword"])
                times.append(item["Time"])
                texts.append(re.sub('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '',
                       item["Text"]))
                sentiments.append(item["sentiment"])

            # This is used to create the table.
            d = {'Name': names, 'Type': types, 'Keyword': keywords, 'Gathered At': times, 'Text': texts,
                 'Sentiment': sentiments}
            dataframe = pd.DataFrame(data=d)

            # Returns and generates a html data frame object with the above attributes
            return html.Table(
                # Header
                [html.Tr([html.Th(col) for col in dataframe.columns])] +

                # Body
                [html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), len(dataframe)))]
            )

        # If the value parsed in is not valid returns none
        else:
            return None

    # This is the main bulk of the class. Defining the necessary setting to load the page.
    # This function loads the titles, dropdown and graph.
    def generate_page(self):

        self.generate_layout()

        # A callback for when a user selects on item in the drop down
        @app.callback(
            dash.dependencies.Output('output-container', 'children'),
            [dash.dependencies.Input('my-dropdown', 'value')])
        def update_output(value):
            return [self.return_graph(value), self.return_table(value)]

        @app.callback(
            dash.dependencies.Output('output-container-button', 'children'),
            [dash.dependencies.Input('button', 'n_clicks')],
            [dash.dependencies.State('name_input-box', 'value'),
             dash.dependencies.State('impact_input_box', 'value'),
            dash.dependencies.State('handle_and_source_input_box', 'value')])
        def update_output(n_clicks, name, impact, handles_and_sources):
            try:
                if name and impact and handles_and_sources:

                        if "," in handles_and_sources:
                            handles_and_sources = handles_and_sources.split(",")
                        else:
                            handles_and_sources = [handles_and_sources]

                        list_of_dictionaries = []

                        for handle_and_source in handles_and_sources:
                            handle, source = handle_and_source.split(":")
                            list_of_dictionaries.append({source:handle})

                        self.profile_individual(list_of_dictionaries,name, impact)
                else:
                    return "Please fill all boxes..."

            except:
                return "Sorry, something went wrong with that profile..."

        # Displays the website
        app.run_server()