import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from glob import glob
import dash_bootstrap_components as dbc

# TO DO:
# modifier (year over year)
# rank (only amongst selected schools unless just one selected)
# custom equation.
# more data
# dollars data non category
# housing cost

init = False

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

TEACHER_COLUMNS = ['UNIQ','Year','District Name','District Code','Total # of Teachers (FTE)','Student / Teacher Ratio','Percent of Experienced Teachers']
EXPENDITURES_COLUMNS = ['UNIQ','Year','District Name','District Code','In-District Expenditures per Pupil']
ENROLLMENT_COLUMNS = ['UNIQ','Year','District Name','District Code','Elementary School Enrollment','Middle School Enrollment','High School Enrollment']
ATTENDANCE_COLUMNS = ['UNIQ','Year','District Name','District Code','Attendance Rate','Chronically Absent (10% or more)','Chronically Absent (20% or more)']
DISCIPLINE_COLUMNS = ['UNIQ','Year','District Name','District Code','Students','% In-School Suspension','% Out-of-School Suspension']
RETENTION_COLUMNS = ['UNIQ','Year','District Name','District Code','Teacher % Retained']
SALARY_COLUMNS = ['UNIQ','Year','District Name','District Code']#,'Average Teacher Salary']
ADVANCED_COLUMNS = ['UNIQ','Year','District Name','District Code','% Students Completing AP']
ARTS_COLUMNS = ['UNIQ','Year','District Name','District Code','Arts Participation % (High School)']
MATH_COLUMNS = ['UNIQ','Year','District Name','District Code','Average Class Size (Math Only)']
CLASSSIZE_COLUMNS = ['UNIQ','Year','District Name','District Code','Average Class Size (All Classes)']
POPULATION_COLUMNS = ['UNIQ','Year','District Name','District Code','']
NINE_COLUMNS = ['UNIQ','Year','District Name','District Code','% Passing All 9th Grade Courses']
SPENDING_COLUMNS = ['UNIQ','Year','District Name','District Code','Spending as % of Required']
SAT_COLUMNS = ['UNIQ','Year','District Name','District Code','Total SAT Score']
LISAT_COLUMNS = ['UNIQ','Year','District Name','District Code','Total SAT Score (ED Students)']
AP_COLUMNS = ['UNIQ','Year','District Name','District Code','AP Test Score 3-5 %','Tests Taken']
COLLEGE_COLUMNS = ['UNIQ','Year','District Name','District Code','High School Graduates (#)','Attending Coll./Univ. %']
LICOLLEGE_COLUMNS = ['UNIQ','Year','District Name','District Code','Attending Coll./Univ. % (ED Students)']

def get_teacherdata(tickers=DISTRICTS_LIST,columns=TEACHER_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/teacherdata*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        #df = df[df['District Code'].isin(DISTRICTS_LIST)]
        df['Student / Teacher Ratio'][df['Student / Teacher Ratio']=='Not Reported'] = 'NAN to NAN'
        df['Student / Teacher Ratio'] = df['Student / Teacher Ratio'].str.split("to").str.get(0).astype(float)
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        # df['Total # of Teachers (FTE)'] = df['Total # of Teachers (FTE)'].astype(float)
        df = df[columns]
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
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        #df = df[df['District Code'].isin(DISTRICTS_LIST)]
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Elementary School Enrollment'] = df['K'] + df['1'] + df['2'] + df['3'] + df['4']
        df['Middle School Enrollment'] = df['5'] + df['6'] + df['7'] + df['8']
        df['High School Enrollment'] = df['9'] + df['10'] + df['11'] + df['12']
        df = df[columns]
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
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_retentiondata(tickers=DISTRICTS_LIST,columns=RETENTION_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/staffingretention*.xlsx")
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
        df['Teacher % Retained'][df['Teacher % Retained'] == 'NR'] = 'NAN'
        df['Teacher % Retained'] = df['Teacher % Retained'].astype(float)
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_salarydata(tickers=DISTRICTS_LIST,columns=SALARY_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/TeacherSalaries*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        # df['Average Teacher Salary'] = df['Average Salary'].str.replace('$','').replace(',','').astype(float)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_advanceddata(tickers=DISTRICTS_LIST,columns=ADVANCED_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/AdvancedCourseCompletion*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['% Students Completing AP'] = df['% Students Completing Advanced']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_artsdata(tickers=DISTRICTS_LIST,columns=ARTS_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/artcourse*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Arts Participation % (High School)'] = (df['09']+df['10']+df['11']+df['12'])/4.
        df = df[columns]
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
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
        
    return bigdf

def get_mathclassdata(tickers=DISTRICTS_LIST,columns=MATH_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/MathClassSizebyGenPopulation*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Average Class Size (Math Only)'] = df['Average Class Size']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_allclassdata(tickers=DISTRICTS_LIST,columns=CLASSSIZE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/ClassSizebyGenPopulation*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Average Class Size (All Classes)'] = df['Average Class Size']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_ninedata(tickers=DISTRICTS_LIST,columns=NINE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/gradeninecoursepasss*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['% Passing All 9th Grade Courses'] = df['% Passing All Courses']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_spendingdata(tickers=DISTRICTS_LIST,columns=SPENDING_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/NetSchoolSpending*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Spending as % of Required'] = df['Actual NSS as % of Required'].astype(float)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_satdata(tickers=DISTRICTS_LIST,columns=SAT_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/sat_performance*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        if year < 2017:
            df['Reading / Writing'] = (df['Reading']+df['Writing'])/2.

        df['Total SAT Score'] = df['Reading / Writing'] + df['Math']
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_LIsatdata(tickers=DISTRICTS_LIST,columns=LISAT_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/LOWINCOMEsat_performance*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        if year < 2017:
            df['Reading / Writing'] = (df['Reading']+df['Writing'])/2.

        df['Total SAT Score (ED Students)'] = df['Reading / Writing'] + df['Math']
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_apdata(tickers=DISTRICTS_LIST,columns=AP_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/ap_performance*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['AP Test Score 3-5 %'] = df['% Score 3-5']
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_collegedata(tickers=DISTRICTS_LIST,columns=COLLEGE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/Gradsattendingcollege*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Attending Coll./Univ. %'] = df['Attending Coll./Univ. (%)']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

def get_licollegedata(tickers=DISTRICTS_LIST,columns=LICOLLEGE_COLUMNS):
    """imports data from xlsx"""
    files = glob(f"../DATA/Gradsattendingcollege*.xlsx")
    df_list = []
    for file in files:
        df = pd.read_excel(file,skiprows=1, thousands=',')
        for col in columns:
            if not col in df.columns:
                df[col] = np.nan
        year = int('20'+file.split('.xlsx')[0][-2:])
        df['Year'] = year
        df['UNIQ'] = df['District Code'].astype(str)+df['Year'].astype(str)
        df['Attending Coll./Univ. % (ED Students)'] = df['Attending Coll./Univ. (%)']
        df = df[columns]
        df_list.append(df)
    bigdf = pd.concat(df_list)
    return bigdf

if init:
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
    retentiondata_df = get_retentiondata()
    print('got retentiondata_df')
    salarydata_df = get_salarydata()
    print('got salarydata_df')
    advanceddata_df = get_advanceddata()
    print('got advanceddata_df')
    artsdata_df = get_artsdata()
    print('got artsdata_df')
    disciplinedata_df = get_disciplinedata()
    print('got disciplinedata_df')
    mathclassdata_df = get_mathclassdata()
    print('got mathclassdata_df')
    allclassdata_df = get_allclassdata()
    print('got allclassdata_df')
    ninedata_df = get_ninedata()
    print('got ninedata_df')
    spendingdata_df = get_spendingdata()
    print('got spendingdata_df')
    satdata_df = get_satdata()
    print('got satdata_df')
    LIsatdata_df = get_LIsatdata()
    print('got LIsatdata_df')
    apdata_df = get_apdata()
    print('got apdata_df')
    collegedata_df = get_collegedata()
    print('got collegedata_df')
    licollegedata_df = get_licollegedata()
    print('got licollegedata_df')
    # data_df = get_data()
    # print('got data_df')
    # data_df = get_data()
    # print('got data_df')

    # data_df = pd.merge(data_df,expendituresdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    # print('done merge1')
    data_df = pd.merge(data_df,enrollmentdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge2')
    data_df = pd.merge(data_df,attendancedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge3')
    data_df = pd.merge(data_df,disciplinedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge4')
    data_df = pd.merge(data_df,retentiondata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge5')
    data_df = pd.merge(data_df,salarydata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge6')
    data_df = pd.merge(data_df,advanceddata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge7')
    data_df = pd.merge(data_df,artsdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge8')
    data_df = pd.merge(data_df,disciplinedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge9')
    data_df = pd.merge(data_df,mathclassdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge10')
    data_df = pd.merge(data_df,allclassdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge11')
    data_df = pd.merge(data_df,ninedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge12')
    data_df = pd.merge(data_df,spendingdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge13')
    data_df = pd.merge(data_df,satdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge14')
    data_df = pd.merge(data_df,LIsatdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge15')
    data_df = pd.merge(data_df,apdata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge')
    data_df = pd.merge(data_df,collegedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge')
    data_df = pd.merge(data_df,licollegedata_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    print('done merge')
    # data_df = pd.merge(data_df,data_df,on='UNIQ',suffixes=('','_extra'),how='outer')
    # print('done merge')

    data_df.to_pickle("./data_df.pkl")    
      
else:
    data_df = pd.read_pickle("./data_df.pkl")  

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
'Teacher % Retained',
# 'Average Teacher Salary',
'% Students Completing AP',
'AP Test Score 3-5 %',
'Arts Participation % (High School)',
'Average Class Size (Math Only)',
'Average Class Size (All Classes)',
'% Passing All 9th Grade Courses',
'Total SAT Score',
'Total SAT Score (ED Students)',
'Spending as % of Required',
'Attending Coll./Univ. %',
'Attending Coll./Univ. % (ED Students)',
'Custom Weighted Evaluation'
]

rankinvert = {
'Student / Teacher Ratio':True,
'Students':False,
'Total # of Teachers (FTE)':False,
'Percent of Experienced Teachers':False,
# 'In-District Expenditures per Pupil ($)':False,
'Elementary School Enrollment':False,
'Middle School Enrollment':False,
'High School Enrollment':False,
'Attendance Rate':False,
"Chronically Absent (10% or more)":True,
"Chronically Absent (20% or more)":True,
'% In-School Suspension':True,
'% Out-of-School Suspension':True,
'Teacher % Retained':True,
# 'Average Teacher Salary':False,
'% Students Completing AP':False,
'AP Test Score 3-5 %':False,
'Arts Participation % (High School)':False,
'Average Class Size (Math Only)':True,
'Average Class Size (All Classes)':True,
'% Passing All 9th Grade Courses':False,
'Total SAT Score':False,
'Total SAT Score (ED Students)':False,
'Spending as % of Required':False,
'Attending Coll./Univ. %':False,
'Attending Coll./Univ. % (ED Students)':False,
'Custom Weighted Evaluation':True,
}


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
                dcc.Dropdown(['None','Include Full Distribution','Rank (overall)','Rank (only selected)'], 'None', id='modifier', style = {'margin-left':'7px'}),
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
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='students')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Percent of Experienced Teachers x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='experience')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Attendance Rate x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='attendance')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Chronically Absent (10% or more) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='absent10')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % In-School Suspension x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='issuspension')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % Out-of-School Suspension x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='ossuspension')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Teacher % Retained x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='retained')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % Students Completing AP x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='apperc')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % AP Scores 3-5 x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='apresults')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Arts Participation % x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='arts')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Average Class Size (Math Only) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='mathclasssize')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Average Class Size (All Classes) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='classsize')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ % Passing All 9th Grade Courses x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='nine')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Total SAT Score x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='sat')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Total SAT Score (ED Students) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='lisat')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Spending as % of Required x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='spending')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),
    
    html.Div([html.A('+ Attending Coll./Univ. % x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='college')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    html.Div([html.A('+ Attending Coll./Univ. % (ED Students) x '),
    dcc.Input(placeholder='Enter weight (-100 to 100)',size='23', type='text', value='', id='licollege')],
    style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),

    # html.Div([html.A('+ ASDF x '),
    # dcc.Input(placeholder='Enter weight (0 to 100)',size='23', type='text', value='', id='asdf')],
    # style = {'margin-left':'7px','margin-right':'7px','padding': '10px'}),


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
                    dbc.Col(html.A(' Based on data from profiles.doe.mass.edu', href='profiles.doe.mass.edu', target="profiles.doe.mass.edu"), width = 8, style = {'margin-left':'7px','margin-top':'7px'})
                    ]),
                dbc.Row(
                    [dbc.Col(sidebar),
                    dbc.Col(dcc.Graph(id='graph-content'), width = 8, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'})
                    ]),
                dbc.Row(html.Hr()),
                dbc.Row(html.H2(" Custom Weighted Evaluation", className="lead", style = {'margin-left':'7px'})),
                dbc.Row( equation ),
                # dbc.Row(html.A(" Note: Default values for weights are 0.", className="lead", style = {'margin-left':'7px'})),
                dbc.Row(html.A(" Note: Before applying your custom weighting, each variable is normalized to a number between 0 and 1.", className="lead", style = {'margin-left':'7px'})),
                dbc.Row(html.Br()),
                dbc.Row(html.A(" Tip: When to make the value negative? When smaller values are more desireable. For Example: smaller Student/Teacher ratios are better, so make that negative.", className="lead", style = {'margin-left':'7px'})),
                dbc.Row(html.Br()),
                ])

# def z_score(df):
#     # copy the dataframe
#     # apply the z-score method
#     grouped = df.groupby('Year')
#     for column in df.columns:
#         df[column+' normed'] = (df[column] - df[column].mean()) / df[column].std()
        
#     return df

def zscore(x):
    try:
        return x / max(np.abs(x.dropna()))
    except:
        return x

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
    Input('ycol', 'value'),
    Input('modifier', 'value'),
    Input('stratio', 'value'),
    Input('students', 'value'),
    Input('experience', 'value'),
    Input('attendance', 'value'),
    Input('absent10', 'value'),
    Input('issuspension', 'value'),
    Input('ossuspension', 'value'),
    Input('retained', 'value'),
    Input('apperc', 'value'),
    Input('apresults', 'value'),
    Input('arts', 'value'),
    Input('mathclasssize', 'value'),
    Input('classsize', 'value'),
    Input('nine', 'value'),
    Input('sat', 'value'),
    Input('lisat', 'value'),
    Input('spending', 'value'),
    Input('college', 'value'),
    Input('licollege', 'value'),
    # Input('', 'value'),
    # Input('', 'value'),
    ]
)
def update_graph(value,yvalue,modifier,stratio,students,experience,attendance,absent10,
                    issuspension,ossuspension,retained,apperc,apresults,arts,mathclasssize,
                    classsize,nine,sat,lisat,spending,college,licollege):
    
    customdict = {'Student / Teacher Ratio':stratio,
    'Students':students,
    'Percent of Experienced Teachers':experience,
    'Attendance Rate':attendance,
    'Chronically Absent (10% or more)':absent10,
    '% In-School Suspension':issuspension,
    '% Out-of-School Suspension':ossuspension,
    'Teacher % Retained':retained,
    '% Students Completing AP':apperc,
    'AP Test Score 3-5 %':apresults,
    'Arts Participation % (High School)':arts,
    'Average Class Size (Math Only)':mathclasssize,
    'Average Class Size (All Classes)':classsize,
    '% Passing All 9th Grade Courses':nine,
    'Total SAT Score':sat,
    'Total SAT Score (ED Students)':lisat,
    'Spending as % of Required':spending,
    'Attending Coll./Univ. %':college,
    'Attending Coll./Univ. % (ED Students)':licollege,
    # '':,
    # '':,
    }

    ww = data_df['District Name']== 'asdf' 
    if not isinstance(value, list):
        ww = (data_df['District Name']==value)
    else:
        for v in value:
            ww = ww | (data_df['District Name']==v)    
    if yvalue is None:
        return px.line()        

    if yvalue == "Custom Weighted Evaluation":
        normed_data_df = data_df.groupby('Year').transform(zscore)

        try:
        # if True:
            data_df['Custom Weighted Evaluation'] = normed_data_df['District Code']*0
            for key,v in customdict.items():
                if v == '': continue
                data_df['Custom Weighted Evaluation'] += normed_data_df[key].astype(float)*float(v)
        except:
            print('could not convert string to float')
            return

    if modifier == 'None':
        dff = data_df[ww].sort_values('Year')
        return px.line(dff, x='Year', y=yvalue, range_x=[2011,2023], line_group='District Name', color='District Name')
    if modifier == 'Include Full Distribution':

        dff = data_df[ww].sort_values('Year')

        line = px.line(dff, x='Year', y=yvalue, range_x=[2011,2023], line_group='District Name', color='District Name')
        hist = px.histogram(data_df,y = yvalue)

        figures = [ line, hist ]

        fig = make_subplots(rows=1, cols=2, shared_yaxes=True, column_widths=[0.8, 0.2], horizontal_spacing=0.02) 
        for i, figure in enumerate(figures):
            for trace in range(len(figure["data"])):
                fig.append_trace(figure["data"][trace], row=1, col=i+1)
        fig.update_xaxes(showticklabels=False, row=1, col=2)
        fig.update_xaxes(title_text='Year',row=1,col=1)
        fig.update_yaxes(title_text=yvalue,row=1,col=1) 

        return fig

    if modifier == 'Rank (overall)':
        data_df[yvalue+' Rank (overall)'] = data_df.groupby("Year")[yvalue].rank(method='max',ascending=~rankinvert[yvalue])#,na_option='bottom')
        dff = data_df[ww].sort_values('Year')
        return px.line(dff, x='Year', y=yvalue+' Rank (overall)', range_x=[2011,2023], range_y=[450, 0], line_group='District Name', color='District Name')
    if modifier == 'Rank (only selected)':
        dff = data_df[ww].sort_values('Year')
        dff[yvalue+' Rank (only selected)'] = dff.groupby("Year")[yvalue].rank(method='max',ascending=~rankinvert[yvalue])#,na_option='bottom')
        return px.line(dff, x='Year', y=yvalue+' Rank (only selected)', range_x=[2011,2023], range_y=[len(value)+.5, .5], line_group='District Name', color='District Name')



if __name__ == '__main__':
    app.run_server(debug=True)
























