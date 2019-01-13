import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

'''
A Class used to create a web front end for viewing Hunch results. 
'''
class create_website:

    # The constructor, setting class variables
    # This takes in a list of dictionaries for the individuals to be profiled.
    def __init__(self, list_of_individuals_to_display = []):
        self.list_of_individuals = []
        self.list_of_individuals.extend(list_of_individuals_to_display)

    # This is the main bulk of the class. Defining the necessary setting to load the page.
    # This function loads the titles, dropdown and graph.
    def generate_page(self):

        #This is used to loop through the individuals and create a list for them
        list_for_dropdown = []
        for individual in self.list_of_individuals:
            list_for_dropdown.append({'label': individual["name"], 'value': individual["name"]})

        #Sets what the HTML page will look like.
        app.layout = html.Div(children=[
            html.H1(children='Hunch!'),

            html.Div(children='''
                A NLP powered predictive policing framework.
            '''),

            dcc.Dropdown(
                id='my-dropdown',
                options=list_for_dropdown,
                multi=True
            ),

            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [],
                    'layout': {
                        'title': 'Profiled Individuals'
                    }
                }
            ),

        html.Div(id='output-container')
        ])

        #A callback for when a user selects on item in the drop down
        @app.callback(
            dash.dependencies.Output('output-container', 'children'),
            [dash.dependencies.Input('my-dropdown', 'value')])
        def update_output(value):
            if value:
                if type(value) is not list:
                    value = [value]
                #This checks if the indivudals that have been selected in the dropdown are in the list of individuals
                # and if so adds their data to the graph.
                list_for_graph = []
                for user in value:
                    for people in self.list_of_individuals:
                        if  people["name"] == user:
                                list_for_graph.append({'x': ["Likelihood", "Impact", "Risk"], 'y': [people["likelihood"], people["impact"], people["risk"]], 'type': 'bar', 'name': people["name"]})

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
            else:
                return None

        #Renders the website
        app.run_server(debug=True)