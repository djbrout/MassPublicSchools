import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from glob import glob
import dash_bootstrap_components as dbc

# TO DO:
# modifier (year over year)
# rank (only amongst selected schools unless just one selected)
# custom equation.
# more data
# dollars data non category
# housing cost


DISTRICTS = {
    int("00490000"): "Cambridge",
    int("00460000"): "Brookline",
    int("02070000"): "Newton",
}
DISTRICTS_LIST = tuple(DISTRICTS.keys())


DISTRICTS_LIST = [
"Abby Kelley Foster Charter Public (District)",
"Abington",
"Academy Of the Pacific Rim Charter Public (District)",
"Acton-Boxborough",
"Acushnet",
"Advanced Math and Science Academy Charter (District)",
"Agawam",
"Alma del Mar Charter School (District)",
"Amesbury",
"Amherst",
"Amherst-Pelham",
"Andover",
"Argosy Collegiate Charter School (District)",
"Arlington",
"Ashburnham-Westminster",
"Ashland",
"Assabet Valley Regional Vocational Technical",
"Athol-Royalston",
"Atlantis Charter (District)",
"Attleboro",
"Auburn",
"Avon",
"Ayer Shirley School District",
"Barnstable",
"Baystate Academy Charter Public School (District)",
"Bedford",
"Belchertown",
"Bellingham",
"Belmont",
"Benjamin Banneker Charter Public (District)",
"Benjamin Franklin Classical Charter Public (District)",
"Berkley",
"Berkshire Arts and Technology Charter Public (District)",
"Berkshire Hills",
"Berlin-Boylston",
"Beverly",
"Billerica",
"Blackstone Valley Regional Vocational Technical",
"Blackstone-Millville",
"Blue Hills Regional Vocational Technical",
"Boston",
"Boston Collegiate Charter (District)",
"Boston Day and Evening Academy Charter (District)",
"Boston Green Academy Horace Mann Charter School (District)",
"Boston Preparatory Charter Public (District)",
"Boston Renaissance Charter Public (District)",
"Bourne",
"Boxford",
"Braintree",
"Brewster",
"Bridge Boston Charter School (District)",
"Bridgewater-Raynham",
"Brimfield",
"Bristol County Agricultural",
"Bristol-Plymouth Regional Vocational Technical",
"Brockton",
"Brooke Charter School (District)",
"Brookfield",
"Brookline",
"Burlington",
"Cambridge",
"Canton",
"Cape Cod Lighthouse Charter (District)",
"Cape Cod Regional Vocational Technical",
"Carlisle",
"Carver",
"Central Berkshire",
"Chelmsford",
"Chelsea",
"Chesterfield-Goshen",
"Chicopee",
"Christa McAuliffe Charter Public (District)",
"City on a Hill Charter Public School Circuit Street (District)",
"Clarksburg",
"Clinton",
"Codman Academy Charter Public (District)",
"Cohasset",
"Collegiate Charter School of Lowell (District)",
"Community Charter School of Cambridge (District)",
"Community Day Charter Public School - Gateway (District)",
"Community Day Charter Public School - Prospect (District)",
"Community Day Charter Public School - R. Kingman Webster (District)",
"Concord",
"Concord-Carlisle",
"Conservatory Lab Charter (District)",
"Conway",
"Danvers",
"Dartmouth",
"Dedham",
"Deerfield",
"Dennis-Yarmouth",
"Dighton-Rehoboth",
"Douglas",
"Dover",
"Dover-Sherborn",
"Dracut",
"Dudley Street Neighborhood Charter School (District)",
"Dudley-Charlton Reg",
"Duxbury",
"East Bridgewater",
"East Longmeadow",
"Eastham",
"Easthampton",
"Easton",
"Edgartown",
"Edward M. Kennedy Academy for Health Careers (Horace Mann Charter) (District)",
"Erving",
"Essex North Shore Agricultural and Technical School District",
"Everett",
"Excel Academy Charter (District)",
"Fairhaven",
"Fall River",
"Falmouth",
"Farmington River Reg",
"Fitchburg",
"Florida",
"Four Rivers Charter Public (District)",
"Foxborough",
"Foxborough Regional Charter (District)",
"Framingham",
"Francis W. Parker Charter Essential (District)",
"Franklin",
"Franklin County Regional Vocational Technical",
"Freetown-Lakeville",
"Frontier",
"Gardner",
"Gateway",
"Georgetown",
"Gill-Montague",
"Global Learning Charter Public (District)",
"Gloucester",
"Grafton",
"Granby",
"Greater Fall River Regional Vocational Technical",
"Greater Lawrence Regional Vocational Technical",
"Greater Lowell Regional Vocational Technical",
"Greater New Bedford Regional Vocational Technical",
"Greenfield",
"Greenfield Commonwealth Virtual District",
"Groton-Dunstable",
"Hadley",
"Halifax",
"Hamilton-Wenham",
"Hampden Charter School of Science East (District)",
"Hampden Charter School of Science West (District)",
"Hampden-Wilbraham",
"Hampshire",
"Hancock",
"Hanover",
"Harvard",
"Hatfield",
"Haverhill",
"Hawlemont",
"Helen Y. Davis Leadership Academy Charter Public (District)",
"Hill View Montessori Charter Public (District)",
"Hilltown Cooperative Charter Public (District)",
"Hingham",
"Holbrook",
"Holland",
"Holliston",
"Holyoke",
"Holyoke Community Charter (District)",
"Hoosac Valley Regional",
"Hopedale",
"Hopkinton",
"Hudson",
"Hull",
"Innovation Academy Charter (District)",
"Ipswich",
"KIPP Academy Boston Charter School (District)",
"KIPP Academy Lynn Charter (District)",
"King Philip",
"Kingston",
"Lawrence",
"Lawrence Family Development Charter (District)",
"Learning First Charter Public School (District)",
"Lee",
"Leicester",
"Lenox",
"Leominster",
"Leverett",
"Lexington",
"Libertas Academy Charter School (District)",
"Lincoln",
"Lincoln-Sudbury",
"Littleton",
"Longmeadow",
"Lowell",
"Lowell Community Charter Public (District)",
"Lowell Middlesex Academy Charter (District)",
"Ludlow",
"Lunenburg",
"Lynn",
"Lynnfield",
"MATCH Charter Public School (District)",
"Malden",
"Manchester Essex Regional",
"Mansfield",
"Map Academy Charter School (District)",
"Marblehead",
"Marblehead Community Charter Public (District)",
"Marion",
"Marlborough",
"Marshfield",
"Martha's Vineyard",
"Martha's Vineyard Charter (District)",
"Martin Luther King Jr. Charter School of Excellence (District)",
"Masconomet",
"Mashpee",
"Mattapoisett",
"Maynard",
"Medfield",
"Medford",
"Medway",
"Melrose",
"Mendon-Upton",
"Methuen",
"Middleborough",
"Middleton",
"Milford",
"Millbury",
"Millis",
"Milton",
"Minuteman Regional Vocational Technical",
"Mohawk Trail",
"Monomoy Regional School District",
"Monson",
"Montachusett Regional Vocational Technical",
"Mount Greylock",
"Mystic Valley Regional Charter (District)",
"Nahant",
"Nantucket",
"Narragansett",
"Nashoba",
"Nashoba Valley Regional Vocational Technical",
"Natick",
"Nauset",
"Needham",
"Neighborhood House Charter (District)",
"New Bedford",
"New Heights Charter School of Brockton (District)",
"New Salem-Wendell",
"Newburyport",
"Newton",
"Norfolk",
"Norfolk County Agricultural",
"North Adams",
"North Andover",
"North Attleborough",
"North Brookfield",
"North Middlesex",
"North Reading",
"Northampton",
"Northampton-Smith Vocational Agricultural",
"Northboro-Southboro",
"Northborough",
"Northbridge",
"Northeast Metropolitan Regional Vocational Technical",
"Northern Berkshire Regional Vocational Technical",
"Norton",
"Norwell",
"Norwood",
"Oak Bluffs",
"Old Colony Regional Vocational Technical",
"Old Rochester",
"Old Sturbridge Academy Charter Public School (District)",
"Orange",
"Orleans",
"Oxford",
"Palmer",
"Pathfinder Regional Vocational Technical",
"Paulo Freire Social Justice Charter School (District)",
"Peabody",
"Pelham",
"Pembroke",
"Pentucket",
"Petersham",
"Phoenix Academy Public Charter High School Lawrence (District)",
"Phoenix Academy Public Charter High School Springfield (District)",
"Phoenix Charter Academy (District)",
"Pioneer Charter School of Science (District)",
"Pioneer Charter School of Science II (PCSS-II) (District)",
"Pioneer Valley",
"Pioneer Valley Chinese Immersion Charter (District)",
"Pioneer Valley Performing Arts Charter Public (District)",
"Pittsfield",
"Plainville",
"Plymouth",
"Plympton",
"Prospect Hill Academy Charter (District)",
"Provincetown",
"Quabbin",
"Quaboag Regional",
"Quincy",
"Ralph C Mahar",
"Randolph",
"Reading",
"Revere",
"Richmond",
"Rising Tide Charter Public (District)",
"River Valley Charter (District)",
"Rochester",
"Rockland",
"Rockport",
"Rowe",
"Roxbury Preparatory Charter (District)",
"Sabis International Charter (District)",
"Salem",
"Salem Academy Charter (District)",
"Sandwich",
"Saugus",
"Savoy",
"Scituate",
"Seekonk",
"Sharon",
"Shawsheen Valley Regional Vocational Technical",
"Sherborn",
"Shrewsbury",
"Shutesbury",
"Silver Lake",
"Sizer School: A North Central Charter Essential (District)",
"Somerset",
"Somerset Berkley Regional School District",
"Somerville",
"South Hadley",
"South Middlesex Regional Vocational Technical",
"South Shore Charter Public (District)",
"South Shore Regional Vocational Technical",
"Southampton",
"Southborough",
"Southbridge",
"Southeastern Regional Vocational Technical",
"Southern Berkshire",
"Southern Worcester County Regional Vocational Technical",
"Southwick-Tolland-Granville Regional School District",
"Spencer-E Brookfield",
"Springfield",
"Springfield Preparatory Charter School (District)",
"Stoneham",
"Stoughton",
"Sturbridge",
"Sturgis Charter Public (District)",
"Sudbury",
"Sunderland",
"Sutton",
"Swampscott",
"Swansea",
"TEC Connections Academy Commonwealth Virtual School District",
"Tantasqua",
"Taunton",
"Tewksbury",
"Tisbury",
"Topsfield",
"Tri-County Regional Vocational Technical",
"Triton",
"Truro",
"Tyngsborough",
"UP Academy Charter School of Boston (District)",
"UP Academy Charter School of Dorchester (District)",
"Up-Island Regional",
"Upper Cape Cod Regional Vocational Technical",
"Uxbridge",
"Veritas Preparatory Charter School (District)",
"Wachusett",
"Wakefield",
"Wales",
"Walpole",
"Waltham",
"Ware",
"Wareham",
"Watertown",
"Wayland",
"Webster",
"Wellesley",
"Wellfleet",
"West Boylston",
"West Bridgewater",
"West Springfield",
"Westborough",
"Westfield",
"Westford",
"Westhampton",
"Weston",
"Westport",
"Westwood",
"Weymouth",
"Whately",
"Whitman-Hanson",
"Whittier Regional Vocational Technical",
"Williamsburg",
"Wilmington",
"Winchendon",
"Winchester",
"Winthrop",
"Woburn",
"Worcester",
"Worthington",
"Wrentham"]

TEACHER_COLUMNS = ['District Name','District Code','Total # of Teachers (FTE)','Student / Teacher Ratio','Percent of Experienced Teachers']
EXPENDITURES_COLUMNS = ['District Name','District Code','In-District Expenditures per Pupil']
ENROLLMENT_COLUMNS = ['District Name','District Code','K','1','2','3','4','5','6','7','8','9','10','11','12']
ATTENDANCE_COLUMNS = ['District Name','District Code','Attendance Rate','Chronically Absent (10% or more)','Chronically Absent (20% or more)']
DISCIPLINE_COLUMNS = ['District Name','District Code','Students','% In-School Suspension','% Out-of-School Suspension']

def get_teacherdata(tickers=DISTRICTS_LIST,columns=TEACHER_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/teacherdata*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        df = df[columns]
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        #df = df[df['District Code'].isin(DISTRICTS_LIST)]
        df['Student / Teacher Ratio'][df['Student / Teacher Ratio']=='Not Reported'] = 'NAN to NAN'
        df['Student / Teacher Ratio'] = df['Student / Teacher Ratio'].str.split("to").str.get(0).astype(float)
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        # df['Total # of Teachers (FTE)'] = df['Total # of Teachers (FTE)'].astype(float)
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_expendituredata(tickers=DISTRICTS_LIST,columns=EXPENDITURES_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/PerPupilExpenditures*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        df = df[columns]
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        #df = df[df['District Code'].isin(DISTRICTS_LIST)]
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['In-District Expenditures per Pupil'] = df['In-District Expenditures per Pupil'].str.replace(',', '').str.replace('$', '').astype('float')
        df['In-District Expenditures per Pupil ($)'] = df['In-District Expenditures per Pupil']
        df_list.append(df)

    bigdf = pd.concat(df_list)
        
    return bigdf


def get_enrollmentdata(tickers=DISTRICTS_LIST,columns=ENROLLMENT_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/enrollmentbygrade*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        df = df[columns]
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        #df = df[df['District Code'].isin(DISTRICTS_LIST)]
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Elementary School Enrollment'] = df['K'] + df['1'] + df['2'] + df['3'] + df['4']
        df['Middle School Enrollment'] = df['5'] + df['6'] + df['7'] + df['8']
        df['High School Enrollment'] = df['9'] + df['10'] + df['11'] + df['12']
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_attendancedata(tickers=DISTRICTS_LIST,columns=ATTENDANCE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/attendance*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        df = df[columns]
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_disciplinedata(tickers=DISTRICTS_LIST,columns=DISCIPLINE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/StudentDisciplineDataReport*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        df = df[columns]
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

data_df = get_teacherdata()
print('got teacherdata_df')
# expendituresdata_df = get_expendituredata()
# print('got expendituresdata_df')
enrollmentdata_df = get_enrollmentdata()
print('got enrollmentdata_df')
attendancedata_df = get_attendancedata()
print('got attendancedata_df')
disciplinedata_df = get_disciplinedata()
print('got disciplinedata_df')
# data_df = pd.merge(data_df,expendituresdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
# print('done merge1')
data_df = pd.merge(data_df,enrollmentdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
print('done merge2')
data_df = pd.merge(data_df,attendancedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
print('done merge3')
data_df = pd.merge(data_df,disciplinedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
print('done merge4')


ylist = ['Student / Teacher Ratio', 
'Students',
'Total # of Teachers (FTE)',
'Percent of Experienced Teachers',
# 'In-District Expenditures per Pupil ($)',
'Elementary School Enrollment',
'Middle School Enrollment',
'High School Enrollment',
'Attendance Rate',
"Chronically Absent (10% or more)",
"Chronically Absent (20% or more)",
'% In-School Suspension',
'% Out-of-School Suspension',
]


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

print('sidebar')
sidebar = html.Div(
    [
        html.H2(""),
        html.Hr(),
        dbc.Nav(
            [
                html.H2(" School District", className="lead",style = {'margin-left':'7px'}),
                dcc.Dropdown(data_df['District Name'].dropna().unique(), '', id='dropdown-selection',multi=True, maxHeight=500, style = {'margin-left':'7px'}),
                html.Br(),
                html.H2(" Data to Plot", className="lead", style = {'margin-left':'7px'}),
                dcc.Dropdown(ylist, 'Student / Teacher Ratio', id='ycol', maxHeight=500, style = {'margin-left':'7px'}),
                html.Br(),
                html.H2(" Modifier", className="lead", style = {'margin-left':'7px'}),
                dcc.Dropdown(['None','Rank (overall)','Rank (only selected)'], 'None', id='modifier', style = {'margin-left':'7px'}),
                html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
            ],
            vertical=True,
            pills=True,
            style = {'margin-left':'7px'}
        ),
    ],
    # style=SIDEBAR_STYLE,
)

print('equation')

equation = html.Div([
    dbc.Nav( [

    html.Div([html.A('Student / Teacher Ratio x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='stratio')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Total Students x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='studets')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Percent of Experienced Teachers x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='experience')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Attendance Rate x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='attendance')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Total Enrollment x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='totenrollment')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Chronically Absent (10% or more) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='absent10')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % In-School Suspension x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='issuspension')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % Out-of-School Suspension x '),
    dcc.Input(placeholder='Enter weight (0 to 100)',size='23', type='text', value='', id='ossuspension')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    ],
    vertical=False,
    pills=True,
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}
    ),
    ],
)

print('app')

app = Dash(external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = html.Div(children = [
                dbc.Row([
                    dbc.Col(),
                    dbc.Col(html.H1(' Massachusetts Public Schools'), width = 8, style = {'margin-left':'7px','margin-top':'7px'})
                    ]),
                dbc.Row([
                    dbc.Col(),
                    dbc.Col(html.A(' Based on data from profiles.doe.mass.edu', href='profiles.doe.mass.edu', target="_blank"), width = 8, style = {'margin-left':'7px','margin-top':'7px'})
                    ]),
                dbc.Row(
                    [dbc.Col(sidebar),
                    dbc.Col(dcc.Graph(id='graph-content'), width = 8, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'})
                    ]),
                dbc.Row(html.Hr()),
                dbc.Row(html.H2(" Custom Weighted Evaluation (NOT FUNCTIONAL YET)", className="lead", style = {'margin-left':'7px'})),
                dbc.Row( equation ),
                ])

def getrank(schools=None):
    return ranks

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
    Input('ycol', 'value'),
    Input('modifier', 'value')]
)
def update_graph(value,yvalue,modifier):
    ww = data_df['District Name']== 'asdf' 
    if not isinstance(value, list):
        ww = (data_df['District Name']==value)
    else:
        for v in value:
            ww = ww | (data_df['District Name']==v)
    print(value)
    print(yvalue)
    
    if yvalue is None:
        return px.line()
    if modifier == 'None':
        dff = data_df[ww].sort_values('Year')
        return px.line(dff, x='Year', y=yvalue, range_x=[2011,2023], line_group='District Name', color='District Name')
    if modifier == 'Rank (overall)':
        data_df[yvalue+' Rank (overall)'] = data_df.groupby("Year")[yvalue].rank(method='max',na_option='bottom')
        dff = data_df[ww].sort_values('Year')
        return px.line(dff, x='Year', y=yvalue+' Rank (overall)', range_x=[2011,2023], line_group='District Name', color='District Name')
    if modifier == 'Rank (only selected)':
        dff = data_df[ww].sort_values('Year')
        dff[yvalue+' Rank (only selected)'] = dff.groupby("Year")[yvalue].rank(method='max',na_option='bottom')
        return px.line(dff, x='Year', y=yvalue+' Rank (only selected)', range_x=[2011,2023], line_group='District Name', color='District Name')

if __name__ == '__main__':
    app.run_server(debug=True)
























