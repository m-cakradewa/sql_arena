import sqlite3
import pandas as pd
import streamlit as st
from streamlit import session_state as ss
import io
import pyzipper
import json
from supabase import create_client, Client

supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_key

if "db" not in ss:
    ss.db = "ecommerce"

if "scorecard_df" not in ss:
    ss["scorecard_df"] = pd.DataFrame(columns = ["database","challenge_number"])

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo, Democratic Republic of the",
    "Congo, Republic of the",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe"
]

databases = ["ecommerce",
             "flight_booking",
             "university",
             "social_media",
             "retail_pos",
             "supply_chain",
             "hospital",
             "hr",
             "event_roi",
             "call_center",
             "banking",
             "uber"]

password = st.secrets.password

def read_solutions(password):
    with pyzipper.AESZipFile("solutions.zip") as zf:
        zf.setpassword(password.encode())
        with zf.open("solutions.json") as f:
            ss["solutions"] = json.load(f)

if "solutions" not in ss:
    read_solutions(password)

if "score_list" not in ss:
    ss.score_list = []

if "title_list" not in ss:
    ss.title_list = []

def submit_entry(name,title,country,score,linkedin):
    url = st.secrets.supabase_url
    key = st.secrets.supabase_key
    supabase: Client = create_client(url, key)
    player = {
    "name": name,
    "title": title,
    "country": country,
    "score": score,
    "linkedin": linkedin}
    if ((name != "") and (country != "") and (title != "") and (linkedin != "") and linkedin.startswith("https://www.linkedin.com/") and (score > 0)):
        supabase.table("leaderboard").upsert(player, on_conflict="linkedin").execute()
        st.success("Your score is locked in. 🔥 Check the leaderboard to see how you rank.")
    else:
        st.success("Please fill the required data to submit your score. :\)")

titles_1_dict = {databases[0]:"E-Commerce Data Analyst",
          databases[1]:"Airline Revenue & Booking Data Specialist",
          databases[2]:"Academic Insights & Enrollment Analyst",
          databases[3]:"Social Media Engagement Data Specialist",
          databases[4]:"Retail Fraud Detection & Insights Analyst",
          databases[5]:"Supply Chain Data Analyst",
          databases[6]:"Healthcare Operations Data Specialist",
          databases[7]:"Workforce & HR Data Analyst",
          databases[8]:"Event ROI & Impact Analyst",
          databases[9]:"Customer Support Performance Analyst",
          databases[10]:"Financial Data Analyst",
          databases[11]:"Service Operations Analyst"}

titles_1 = pd.DataFrame(columns = ["database","title"])
titles_1.database = databases
titles_1.title = list(titles_1_dict.values())
titles_2 = pd.read_csv("achievements.csv")

import streamlit as st

def go_to_link_button(label: str, url: str, width: int = 30, height: int = 30):
    st.markdown(f"""
    <div style="text-align: center;">
        <a href="{url}" target="_blank">
            <button style="
                width: {width}px;
                height: {height}px;
                background-color: #0a66c2;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 20px;
                font-weight: bold;
                cursor: pointer;
            ">{label}</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

@st.dialog("Check My Progress")
def check_my_progress():
    if "score_list" not in ss:
        ss.score_list = []

    if "title_list" not in ss:
        ss.title_list = []
    
    if "scorecard_df" not in ss:
        ss["scorecard_df"] = pd.DataFrame(columns = ["database","challenge_number"])

    score = 0
    # title for completing one theme
    for db in set(ss.scorecard_df.database.tolist()):
        if ss.scorecard_df[ss.scorecard_df["database"] == db].shape[0] == 15:
            ss.title_list.append(titles_1["title"][titles_1["database"]==db].values[0])
    ss.title_list = list(set(ss.title_list))
    score = 6*len(ss.title_list)
    length = ss.scorecard_df.shape[0]
    score = (score + length)
    # title for milestones
    milestones = [1,5,10,20,50,75,100,125,150,180]
    for i in milestones:
        if length>=i:
            ss.title_list.append(titles_2.title[titles_2.req == i].values.tolist()[0])
            score += titles_2.plus_points[titles_2.req == i].values.tolist()[0]

    c1,c2 = st.columns([1,1])
    with c1:
        progress = st.radio("What do you want to check?",["Score Card","Titles","Submit Score","Leaderboards"])
        st.write("")
        st.write("")
    with c2:
        st.write("")
        st.write("")
        st.image("achievements_2.jpeg")

    if progress == "Score Card":
        if st.checkbox("View Score"):
            st.metric(label = "Your Score:",value = score, border=1)
        st.write("")
        try:
            st.dataframe(ss.scorecard_df)
        except:
            pass
    elif progress == "Titles":
        st.write("")
        st.write("### Here are the `TITLES` you've gathered so far.")
        st.write("")
        ss.title_list = list(set(ss.title_list))
        for title in ss.title_list:
            if title in titles_1.title.tolist():
                text = "Successfully finished all challenges in the `"+title+"` field."
            elif title in titles_2.title.tolist():
                text = titles_2["details"][titles_2["title"] == title].values.tolist()[0]
            with st.container(border=1):
                st.write("#### "+title)
                c,c1,c = st.columns([.005,1,.1])
                with c1:
                    st.write('*"'+text+'"*')
    elif progress == "Submit Score":
        cs1,cs2=st.columns(2)
        with cs1:
            name = st.text_input("*Name/Nickname:")
        with cs2:
            country = st.selectbox("*Country:",countries,placeholder="Indonesia")
        title = st.selectbox("*Pick your fav title:", list(set(ss.title_list)),placeholder="")
        linkedin = st.text_input("*Put your linkedin profile to compete with others!")
        st.write("")
        st.write("")
        submit = st.button("Submit!")
        if submit:
            submit_entry(name,title,country,score,linkedin)
    elif progress == "Leaderboards":
        url = st.secrets.supabase_url
        key = st.secrets.supabase_key
        supabase: Client = create_client(url, key)
        leaderboard = supabase.table("leaderboard").select("*").order("score", desc=True).execute()
        # leaderboard = pd.DataFrame(leaderboard.data)
        # st.dataframe(leaderboard)
        for row in leaderboard.data:
            with st.container(border=1):
                c0,c1= st.columns([.8,5])
                with c0:
                    st.write("")
                    go_to_link_button("in", row["linkedin"])
                with c1:
                    st.write("### *"+row["name"]+" (score: "+str(row["score"])+")*")
                    st.write("*"+row["title"]+" from "+row["country"]+"*")
                    
                
def check_answer(df_user,df_solution,db,n):
    if "scorecard_df" not in ss:
        ss["scorecard_df"] = pd.DataFrame(columns = ["database","challenge_number"])
    try:
        # Sort both if order doesn't matter
        df_user_sorted = df_user.sort_values(by=list(df_user.columns)).reset_index(drop=True)
        df_solution_sorted = df_solution.sort_values(by=list(df_solution.columns)).reset_index(drop=True)
    except Exception:
        # If sorting fails (e.g. unorderable types), skip sorting
        df_user_sorted = df_user.reset_index(drop=True)
        df_solution_sorted = df_solution.reset_index(drop=True)
    if df_user_sorted.equals(df_solution_sorted):
        st.success("You solved this question. Good job!")
        newrow = pd.DataFrame([{"database":db,"challenge_number":n}])
        ss["scorecard_df"] = pd.concat([ss["scorecard_df"],newrow], ignore_index = True)
        ss["scorecard_df"] = ss["scorecard_df"].drop_duplicates(subset=["database","challenge_number"]).sort_values(by=["database","challenge_number"])
        if st.checkbox("Mark as solved", key = "mark_as_solved"+db+str(n)):
            pass
        
    else:
        st.error("Result doesn't match the expected output.")
    if st.toggle("See expected output", key = "see_solution"+db+str(n)):
        st.dataframe(df_solution)

def get_answers(query,db):
    conn = sqlite3.connect(db)
    return pd.read_sql_query(query, conn)

def get_formattings(df):
    colnames = ""
    for i in df.columns.tolist():
        colnames += "`"+i+"`"+", "
    colnames = colnames[:-2]
    rows = df.shape[0]
    return [colnames, rows]

def get_table_names(db):
    conn = sqlite3.connect(db)
    tables = pd.read_sql("select name from sqlite_master where type = 'table';",conn)
    table_text = ""
    for i,j in zip(tables.index, tables.name):
        if j != db:
            table_text += "`"+j+"`"
            if i != tables.index[-1]:
                table_text += " | "
    conn.close()
    return table_text

def write_questions(db,n,t):
    if "solutions" not in ss:
        read_solutions(password)
    df_solution = get_answers(ss.solutions[db][str(n)],db+".db")
    c0,c1,c2,c0,c3 = st.columns([.1,.5,5,.5,.1])
    with c1:
        st.subheader(str(n))
    with c2:
        with st.container(border = 0):
            st.markdown("<h7>"+t+"</h7>", unsafe_allow_html=True)
    with c3:
        pass
        
    with st.expander("Write your query here:"):
        st.write(get_table_names(db+".db"))
        query = st.text_area("", key="box"+db+str(n))
        if (len(query) != 0) or (st.button("Run", key = "run"+db+str(n))):
            try:
                df_user = get_answers(query,db+".db")
                st.dataframe(df_user)
                st.write("Expected columns in the output: "+ get_formattings(df_solution)[0])
                st.write("Expected number of rows: `"+str(get_formattings(df_solution)[1])+"`")
                st.write("Your number of rows: `"+str(df_user.shape[0])+"`")
                check_answer(df_user,df_solution,db,n)
            except Exception as e:
                st.error(f"❌ SQL Error: {e}")
    st.write("")
    st.write("")

def create_save_file(password):
    csv_buffer = io.StringIO()
    ss["scorecard_df"].to_csv(csv_buffer, index = False)
    csv_data =csv_buffer.getvalue().encode("utf-8")
    
    zip_buffer = io.BytesIO()
    with pyzipper.AESZipFile(zip_buffer,mode="w",compression=pyzipper.ZIP_LZMA,encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode("utf-8"))
        zf.writestr("scorecard.csv",csv_data)

    zip_buffer.seek(0)
    st.download_button(
        label="Download Save Data",
        data = zip_buffer,
        file_name = "savefile.zip",
        mime = "application/zip"
    )

def open_save_file(uploaded_file):
    zip_bytes = uploaded_file.getvalue()
    try:
        with pyzipper.AESZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.setpassword(password.encode())
            for file_name in zf.namelist():
                if file_name.endswith(".csv"):
                    with zf.open(file_name) as csv_file:
                        loaded_df = pd.read_csv(csv_file)
                        ss.scorecard_df = loaded_df.copy()
                        st.success("Successfully loaded your saved data.")
                        break
            else:
                st.error("CSV file not found inside the ZIP.")
    except RuntimeError as e:
        st.error(f"Failed to open ZIP file: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

descriptions = {
    databases[0]:"You work as a data analyst at a growing e-commerce company that sells electronics and lifestyle products. The company tracks everything from website traffic to customer orders and product returns. Recently, leadership wants to understand key conversion bottlenecks, seasonal purchase behavior, and which product categories drive the highest profit. Your job is to make sense of customer journeys, product performance, and revenue trends.",
    databases[1]:"You’re part of the analytics team at an online travel agency that specializes in flight bookings. The company aggregates flights from hundreds of airlines and handles millions of booking records per year. Recently, customer complaints about cancellations, price inconsistencies, and search delays have increased. You’re tasked with analyzing booking trends, customer satisfaction metrics, and identifying underperforming routes and airline partners.",
    databases[2]:"You're a data analyst at a mid-sized private university. The institution wants to better understand student performance, enrollment patterns, course demand, and dropout rates. You’re working with data from departments, course registrations, exam results, and faculty assignments. Your insights will guide decisions about curriculum redesign, instructor effectiveness, and student support programs.",
    databases[3]:"You work for a social media platform that’s gaining traction among Gen Z users. The product team wants to understand user engagement patterns, post virality, and network growth. You’re analyzing data on posts, likes, comments, shares, and user profiles. The marketing team also wants help identifying influencers and content categories that drive the most interaction.",
    databases[4]:"You work in the analytics department of a national retail chain with hundreds of stores. The company uses a modern POS (Point-of-Sale) system to track transactions, customer loyalty, and returns. Lately, leadership suspects discount abuse and inventory mismatches. Your job is to detect anomalies, understand purchasing behavior, and recommend improvements to pricing and stock management.",
    databases[5]:"You're part of the supply chain analytics team at a manufacturing company with a global distribution network. Lately, the company is facing delayed restocks, high transportation costs, and overloaded distribution centers. You need to analyze shipment data, inventory levels, warehouse capacity, and vendor reliability to help reduce bottlenecks and optimize logistics.",
    databases[6]:"You work as a data analyst for a multi-department hospital. Management wants to improve patient throughput, reduce wait times, and better allocate medical staff. You’re working with patient admissions, diagnosis data, treatment plans, and doctor schedules. Your analysis will inform improvements in operational efficiency and patient care quality.",
    databases[7]:"You’re working in the People Analytics team of a fast-growing startup. With headcount doubling every year, HR leadership wants to identify early signs of burnout, understand promotion bottlenecks, and reduce turnover. You’re working with employee profiles, performance reviews, leave data, and exit surveys to support data-driven workforce planning.",
    databases[8]:"You’re hired by a marketing agency that organizes large-scale events like conferences and expos. The agency wants to evaluate the ROI of each event based on ticket sales, sponsor engagement, and attendee feedback. Your role is to analyze event costs, revenue sources, registration funnels, and post-event surveys to advise which event types are truly worth the investment.",
    databases[9]:"You’re part of the quality assurance team at a customer service call center. Complaints are rising and first-call resolution rates are dropping. Your job is to analyze call logs, agent performance, customer sentiment, and resolution outcomes to identify training needs and improve service KPIs across the team.",
    databases[10]:"You work as a junior data analyst at a retail bank. The risk team wants your help to monitor account activity, detect fraudulent transactions, and understand loan default patterns. You’ll be analyzing data from customer accounts, credit card usage, loans, and transaction histories, with a focus on risk scoring and early warning indicators.",
    databases[11]:"You work at a ride-sharing company looking to optimize driver allocation and pricing. Recent feedback suggests frequent delays during peak hours and poor service coverage in suburban areas. You’re tasked with analyzing trip logs, driver behavior, customer ratings, and city zones to propose operational changes and improve rider satisfaction.",
}

questions = {databases[0]:
    {
    1: "The Head of Operations needs to keep a close eye on how order volume fluctuates throughout 2024. They ask you to provide a detailed monthly breakdown of how many orders were placed to help with staffing and resource planning.",
    2: "Marketing is gearing up for a new campaign and wants to focus on best-selling products. Identify the top 10 products sold in the highest quantities in 2024 to maximize promotional impact.",
    3: "To boost customer loyalty, the company plans to reward its highest spenders. Find the 5 customers who spent the most money in 2024 so they can receive exclusive coupons or branded gifts.",
    4: "Customer Support has flagged delays as a major pain point. Report how many orders are still marked as `Pending` and identify the customers involved to prioritize follow-up actions.",
    5: "Category Managers want to evaluate product profitability. Calculate the average order value (AOV) for each product category to benchmark their performance.",
    6: "The logistics team is investigating return rates to improve processes. Which products have the highest proportion of returned shipments relative to their total shipped quantity?",
    7: "Procurement suspects some suppliers may not be maintaining inventory well. Identify the suppliers whose products most frequently have zero stock in the warehouse.",
    8: "The Product team suspects that orders placed on weekends might be less reliable. Analyze if orders created on Saturdays and Sundays have a higher cancellation rate than those on weekdays.",
    9: "International logistics wants to reduce cancellations abroad. Determine which countries have the highest order cancellation rates and identify any patterns to inform targeted solutions.",
    10: "Finance is exploring partnerships with payment providers. Find out which payment method generates the highest average transaction value to prioritize collaboration efforts.",
    11: "Customer Experience is tasked with improving delivery speed. Calculate the typical number of days between shipment and delivery, and see how this varies by country to pinpoint bottlenecks.",
    12: "Marketing wants to target highly engaged customers. Find customers who have increased their purchase frequency month over month in 2024, signaling growing loyalty.",
    13: "Product Management wants to identify risk areas. Highlight product categories that have strong sales volumes but poor average customer review ratings, so quality issues can be addressed.",
    14: "Management is concerned about inventory mismanagement. Estimate potential revenue lost for products that were out of stock for more than 10 days, based on recent sales velocity.",
    15: "With a limited restock budget, Operations must prioritize wisely. Considering current stock levels, sales velocity, and supplier reliability, recommend which products should be reordered first to maximize availability and sales."
    },
    databases[1]:
    {
    1:"Our operations team noticed some flights have been consistently late. They want you to identify the top 5 flights with the highest average delay in 2024 so management can investigate causes and improve punctuality.",
    2:"The marketing team plans to launch a loyalty program. They ask you to find the top 10 passengers who flew the most flights this year to reward them with exclusive perks.",
    3:"Finance wants a breakdown of total ticket sales revenue by airline for 2024 to compare performance across carriers and adjust contracts accordingly.",
    4:"Customer service reported some complaints about overbooked flights. Your task is to list flights where total tickets sold exceed the airplane’s capacity, to help them prevent future overbooking issues.",
    5:"The route planning team is analyzing how well flights are filled. They ask for the average load factor (seat occupancy rate) per origin-destination pair during 2024 to optimize scheduling.",
    6:"HR needs to monitor pilot workload to comply with regulations. Find all pilots who flew more than 50 flights in 2024 to ensure their schedules are safe and balanced.",
    7:"The customer relations team wants to identify passengers with more than 3 cancelled bookings this year to understand cancellation behavior and possibly offer better booking options.",
    8:"Marketing is curious about booking habits. Calculate the average lead time between booking date and flight departure per airline to tailor promotional campaigns.",
    9:"Sales want to understand preferences. Provide counts of tickets sold by travel class (economy, business, first) for all flights in 2024.",
    10:"Operations is concerned about lost luggage. Determine which airlines have the highest percentage of lost baggage incidents to focus on improving handling processes.",
    11:"Pricing strategy needs data on expensive routes. List the top 5 origin-destination pairs with the highest average ticket price for potential pricing adjustments.",
    12:"The marketing team wants to know the distribution of passenger nationalities for better regional targeting and language support.",
    13:"Finance wants to optimize payment processing. Calculate the percentage share of each payment method used for bookings in 2024.",
    14:"Airport operations want to pinpoint delay causes. Calculate the average flight delay (in minutes) grouped by departure airport.",
    15:"Crew scheduling managers want to ensure no one is overworked. Identify crew members assigned to more than 100 flights in 2024 for workload balancing."
    },
    databases[2]:
    {
    1:"As part of a long-term institutional report, the Academic Affairs office is examining trends in student enrollment. They ask you to summarize how many students enrolled in each academic year to observe growth or decline over time.",
    2:"The Dean is preparing a curriculum optimization proposal. They need to know which courses consistently attract high student interest. Can you identify the 10 most popular courses by enrollment count across all students?",
    3:"An instructor wants to understand student performance trends across their course. To help them and others like them, you’re tasked with calculating the average grade given in each course offered at the university.",
    4:"Advisors have raised concerns that some students may be overloading themselves with too many classes. To help identify potential burnout risks, generate a list of students who are currently enrolled in more than 5 courses.",
    5:"The HR department is auditing teaching assignments. They want to know how many distinct courses each instructor has taught — this will be used in performance reviews and contract renewals.",
    6:"Facilities Management is reviewing space utilization to guide future infrastructure investments. They ask you to determine which classrooms have the highest average occupancy, calculated by comparing scheduled capacity usage to total room capacity.",
    7:"Student Services is launching a recognition program for highly engaged students. They ask you to identify students who have both submitted all of their assignments and never missed an attendance record — model students worth spotlighting.",
    8:"The Psychology department is conducting an internal evaluation to compare academic performance across departments. Your task is to calculate the average grade for all students in the Psychology department across all of their courses.",
    9:"The university wants to assess how academic advisors might be impacting student outcomes. For each instructor serving as an advisor, calculate the average GPA of the students they advise.",
    10:"The Academic Integrity Committee is investigating grading fairness. They ask you to flag any courses where more than 50% of enrolled students received the exact same grade, which may indicate lack of grading variance.",
    11:"The Library is proposing extended study hours on Fridays, but needs data to back it up. Provide a comparison of how many scheduled classes take place on Fridays versus Mondays to estimate campus activity levels on those days.",
    12:"IT Services is scaling up cloud storage and wants to prioritize students with the heaviest submission activity. Identify the students who have submitted the highest number of assignments overall, across all their courses.",
    13:"To better allocate classroom availability, the Scheduling Office is looking for usage patterns. What are the most common time slots (start and end times) used across the weekly course schedules?",
    14:"The Diversity & Inclusion office is doing a fairness check across departments. They ask for an analysis of average grades by department to see if certain departments are grading harder or easier than others.",
    15:"The Admissions team is curating success stories to share with prospective students. They need a list of current students who have maintained a perfect academic record — those who received only 'A' grades in all their courses."
    },
    databases[3]:
    {
    1: "The engagement analytics team is reviewing how post activity has evolved over the last year. They’ve asked for a breakdown of how many new posts were created each month.",
    2: "Management is looking to identify influential users based on audience reactions. They want to know which 10 users have received the highest number of likes across all their posts.",    
    3: "To better understand user interaction, the platform team is analyzing who contributes most to discussions. They need a list of the top 5 users based on total comments made.",
    4: "Marketing is planning a case study on viral content. They want to find the 5 posts that generated the most buzz — measured by the combined total of likes and comments.",
    5: "Community managers are launching a creator partnership program. They're looking for users who not only have more than 100 followers but have also posted actively (over 20 posts).",
    6: "Moderators have flagged some unusual behavior. They're investigating whether any users have liked their own posts — a potential indicator of spam or manipulation.",
    7: "The product team is evaluating the popularity of group features. They need to know how many users are in each group, highlighting the 10 most active ones.",
    8: "Internal research is focused on private messaging usage. Analysts want to calculate the average number of messages sent per user and identify the top 5 most active senders.",
    9: "The advertising team is reviewing campaign performance. They’re particularly interested in campaigns that attracted the widest reach — measured by the number of unique users who clicked on each ad.",
    10: "With several events recently created, the events team is reviewing participation trends. They need a status breakdown (Going, Interested, Not Going) for each event scheduled in the last 30 days.",
    11: "User experience researchers are analyzing notification fatigue. They’d like to know which 10 users received the most notifications in the past 60 days.",
    12: "The growth team is identifying power users who have been consistently active. They're focusing on users who joined more than a year ago and have posted at least once every month this year.",
    13: "A report on suspicious account behavior is underway. Security analysts want to know if any users are following themselves — which shouldn't be possible under normal use.",
    14: "The community operations team is auditing group engagement. They’re looking for groups that have at least 5 members but show no posting activity from any of those members in the last 60 days.",
    15: "To better allocate infrastructure resources, the platform reliability team is identifying peak usage patterns. They need to know which single day in the past year saw the highest combined number of posts, comments, and likes."
    },
    databases[4]:
    {
    1: "The store manager wants to review monthly sales performance. Provide a breakdown of total sales revenue per month over the past 6 months.",
    2: "Marketing is planning a seasonal promotion and needs to know which 10 products sold the most in terms of quantity across all stores.",
    3: "Finance wants to identify the top 5 customers by total spending. This will be used to offer loyalty rewards.",
    4: "A store supervisor is investigating low-stock products. List all products in Store #3 that currently have stock levels under 5 units.",
    5: "The operations team wants to detect supplier dependency. Show which suppliers provide the most unique products.",
    6: "Human Resources is reviewing store staffing. Provide the number of employees working at each store.",
    7: "To detect possible pricing issues, product managers need to find the 5 products with the largest difference between their price and cost.",
    8: "A customer filed a complaint about delayed payment records. Find all sales where the payment was made more than 1 day after the sale date.",
    9: "Inventory analysts are checking stock freshness. Identify products that haven’t been restocked in over 60 days, grouped by store.",
    10: "Store managers want to monitor employee activity. Find the number of shifts each employee has worked in the past 30 days.",
    11: "Finance is interested in evaluating payment method trends. Provide a breakdown of total payment amount by payment method.",
    12: "Procurement is trying to spot restocking trends. What are the top 10 most frequently purchased products (from suppliers) in the last 3 months?",
    13: "The pricing team is reviewing low-margin products. Identify all products where the profit margin (price - cost) is below 20%.",
    14: "Customer insights team is studying shopping behavior. Find customers who made purchases in at least 3 different stores.",
    15: "Loss prevention is conducting fraud checks. Identify any sales that contain the same product more than once in the same sale — which could signal duplicate scan errors."
    },
    databases[5]:
    {
    1: "Customer complaints about delayed deliveries have increased in recent weeks. To trace the source, operations leadership wants to see which distribution centers are responsible for the most late shipments and how large the issue is at each location.",
    2: "Finance suspects that transportation expenses are ballooning on certain shipping routes. They request a breakdown of routes generating the highest total costs based on distance and cost per kilometer to better control spending.",
    3: "During a stock review, leadership noticed some warehouses appear to be holding significantly more inventory than others. They ask you to identify which warehouses currently carry the largest inventory volumes.",
    4: "Incorrect product deliveries are frustrating buyers. Management wants to compare fulfillment accuracy across product categories by examining how much of what gets ordered actually gets successfully delivered.",
    5: "Logistics wants to rebalance outbound shipments across facilities. They need a snapshot showing what proportion of all recent shipments originated from each warehouse to determine if any location is over-utilized.",
    6: "To help plan procurement cycles, demand planners want to understand seasonality patterns by identifying which months in the past year saw the highest volume of orders placed.",
    7: "Bottlenecks are emerging at certain distribution centers, and leadership fears their inventories exceed what their warehouse capacities were designed to handle. Show which centers currently have inventory levels above their total storage capacity.",
    8: "Supplier delivery speed has become a competitive differentiator. Procurement wants to assess which suppliers are slowest by evaluating the average number of days between order placement and shipment.",
    9: "With transport contracts due for renegotiation, senior management wants to review the five costliest logistics routes this year — measured by distance multiplied by cost per kilometer — to target savings.",
    10: "Inventory planners believe some product categories are consistently over- or under-stocked. To verify this, they request the average quantity on hand per category across all warehouses.",
    11: "Executives want to compare performance between distribution centers by shipment status. Specifically, they’d like to review how many shipments marked 'Delivered' and 'In Transit' have originated from each center.",
    12: "Rapid restocking is often a sign of fast-moving or volatile products. Supply chain analysts want to know which products are restocked most frequently across the network.",
    13: "Some suppliers may be contributing to stock-outs on key products. Management asks for a ranking of suppliers associated with the highest number of zero-inventory products across warehouses.",
    14: "Workforce planning is under review. Leadership wants to know how many employees each distribution center has relative to their current order load in order to evaluate staffing efficiency.",
    15: "Product teams suspect some categories experience frequent under-delivery. They want to quantify which product categories have the largest gaps between what was ordered and what was actually shipped."
},
    databases[6]:
    {
    1: "Hospital management has noticed delays in patient discharges, which may affect room availability. They want to identify which departments have the longest average stay durations and quantify the delays.",
    2: "The finance team is reviewing outstanding bills. They want to know which patients have unpaid invoices and the total amount pending across the hospital.",
    3: "The emergency department is assessing patient influx. They request a summary of the top 5 doctors by number of visits attended in the past year.",
    4: "Hospital administrators are concerned about high-risk patients. They want to list patients who have multiple diagnoses to ensure follow-up care is adequate.",
    5: "The pharmacy wants to optimize inventory. They ask for the medications most frequently prescribed over the last 12 months.",
    6: "Surgery planning requires insight into operational success. The surgical team wants to see which surgery types had the highest complication rates.",
    7: "Departments want to ensure lab results are processed timely. They ask for a list of lab tests still pending and the number of pending results per department.",
    8: "Staffing coordinators are evaluating shift coverage. They need to know which departments had the most night shifts assigned over the past 6 months.",
    9: "Patient care coordination wants to monitor doctor workloads. They request average visits per doctor per month to identify overburdened staff.",
    10: "The admissions office wants to understand seasonal patient load. They ask for the number of admissions per department each month.",
    11: "Hospital leadership wants to evaluate patient follow-ups. They ask for patients who have had both a visit and a subsequent admission within 30 days.",
    12: "The radiology department wants to track abnormal test results. They need a summary of which test types most frequently returned 'Abnormal'.",
    13: "Insurance verification is a priority. The billing team wants to know the average coverage percentage per insurance provider for active patients.",
    14: "The hospital wants to recognize its busiest staff. They ask for a ranking of staff members by the total number of shifts worked in the last 6 months.",
    15: "Management wants to identify high-cost patients. They request a list of patients with the highest cumulative billing amounts in the past year."
},
    databases[7]:
    {
    1: "The HR department is planning workforce expansion and wants to understand current department sizes. They’re reviewing how many active employees each department has, to identify teams that might be understaffed compared to others.",
    2: "Management is reviewing the company’s age demographics to prepare for generational workforce shifts. They’d like to see the average age of employees per department and per gender, to understand where mentorship or succession planning may be needed.",
    3: "To assess internal growth, HR wants to review promotion activity. They are interested in how many promotions occurred in the past 2 years, broken down by department, and whether certain departments promote more often than others.",
    4: "Finance is analyzing payroll expenses and wants to compare the average salary by role level (Junior, Mid, Senior). This will help them plan the next year’s compensation budget.",
    5: "A high turnover rate has been observed in the Engineering department. HR wants to analyze the most common reasons for employee exits in that department over the last 12 months.",
    6: "To improve performance tracking, leadership is reviewing how performance ratings are distributed. They’re particularly interested in which departments or managers tend to give higher-than-average ratings.",
    7: "The COO is preparing a diversity report and wants to understand gender distribution across departments, including counts and percentages of each gender in each department.",
    8: "The CEO wants an overview of hiring trends over time. HR is asked to summarize how many employees were hired each year over the past 5 years, ideally with a breakdown by department.",
    9: "A new training initiative is being considered, but HR first wants to evaluate past participation. They want to know how many employees have completed each training course and what their pass rates were.",
    10: "Project delivery has slowed, and management suspects some employees are overloaded. They want to identify employees who are currently assigned to more than 3 active projects.",
    11: "The HR analytics team is benchmarking absenteeism. They’re looking for employees with unusually high absence rates over the past 30 days, to investigate potential burnout or morale issues.",
    12: "A report is being prepared on salary progression. HR wants to analyze how often employees receive salary increases and the typical gap (in months) between each raise.",
    13: "To identify potential mentors, the L&D team wants a list of employees who have worked in the company for over 8 years and have received at least 2 promotions.",
    14: "A cross-functional review team is evaluating project staffing efficiency. They want a count of employees assigned to each project and want to highlight any projects with fewer than 3 contributors.",
    15: "There is interest in understanding remote work behavior. HR wants to analyze which departments have the highest percentage of remote attendance records in the last month."
    },
    databases[8]:
    {
    1: "The marketing director wants to evaluate event types that attract the highest number of registrations. They’re preparing a presentation and need a breakdown of average registrations per event, grouped by event type.",
    2: "The CFO is assessing event profitability and needs a report showing which events have the highest post-event sales revenue relative to their total spend. This will help guide investment decisions for next year’s event calendar.",
    3: "The head of partnerships is curious about sponsor behavior. They want to know which sponsors have contributed the most across all events and how their contributions are distributed across event types.",
    4: "Marketing wants to understand channel effectiveness. They’re trying to see which marketing channels bring in the most attendees and whether certain channels are more effective for specific types of events.",
    5: "The event planning team wants to identify which cities have hosted the most events in the last 2 years and whether there’s a pattern in geographic popularity.",
    6: "The sales team is tracking high-value leads. They want to find all events that generated at least 5 leads with an estimated value over €10,000.",
    7: "The feedback team is analyzing satisfaction trends. They want to calculate the average attendee rating for each event and flag events with an average below 3.5 for quality review.",
    8: "A new marketing strategy is being proposed, and leadership wants to know how much has been spent on marketing across all events over time. They need a year-by-year breakdown of marketing spend.",
    9: "The analytics team is evaluating ROI patterns. They want a report showing events that had high spend but low sales, to spot underperforming campaigns.",
    10: "Finance wants to calculate the total revenue generated by each event type and compare that to total event spend, to understand which types tend to be most cost-effective.",
    11: "The CRM team is checking how many unique companies attended events. They want to count the number of distinct companies represented among attendees for each event.",
    12: "Event ops wants to find registrations that occurred after the event had already started, to understand how often late signups happen and in which types of events.",
    13: "The CEO is asking for a list of the top 10 events with the highest total number of registrations, regardless of type or location.",
    14: "A new sponsor wants to see examples of events with both high turnout and high satisfaction. The partnerships team needs events with over 200 attendees and an average feedback rating of at least 4.5.",
    15: "Leadership is reviewing cross-functional impact. They want a report that shows for each event: total spend, number of leads generated, total post-event sales, and average feedback rating — all in one view."
    },
    databases[9]:
    {
    1: "The call center manager wants to understand how many active agents are in each department and their current employment status to optimize staffing.",
    2: "To improve customer satisfaction, the quality team is reviewing average call durations by call type to identify which calls tend to take longer and may need process improvements.",
    3: "The operations team is investigating call outcomes to find which outcome categories are most common and to spot trends in unresolved or escalated calls.",
    4: "Management is tracking agent productivity by counting how many calls each agent handled in the past month, highlighting top performers and those needing support.",
    5: "To enhance training programs, HR wants to analyze which agents completed specific training courses and their pass rates over the last two years.",
    6: "The escalation team is analyzing calls that were escalated to higher-level agents, including reasons and how often each escalation reason occurs.",
    7: "Customer experience analysts are looking into feedback ratings to determine which agents consistently receive high satisfaction scores from customers.",
    8: "Scheduling coordinators want to understand agent shift coverage by department to ensure that key departments have sufficient staffing during peak hours.",
    9: "The sales department wants to identify how many outbound sales calls were made, their outcomes, and which agents achieved the most successful sales calls.",
    10: "Support managers want to identify the average time customers spend on support calls and detect any agents whose calls are significantly longer than average.",
    11: "The data team is tasked with identifying customers who have made the most calls in the past 3 months to target for special retention efforts.",
    12: "To improve notes quality, management wants to analyze how often call notes are recorded per call and identify agents who provide the most detailed notes.",
    13: "The customer retention team is reviewing the frequency and reasons for callbacks scheduled to reduce repeat calls and improve first-call resolution rates.",
    14: "Operations leadership wants a report on agent skill distributions and proficiency levels to plan upcoming training and hiring needs effectively.",
    15: "The analytics team is analyzing call volumes and outcomes by city to detect geographic patterns in call types, issues, and resolutions."
    },
    databases[10]:
    {
    1: "The branch manager noticed a sudden spike in withdrawals at the New York Main Branch. They want to identify which customers made the highest withdrawals over the past month to investigate unusual activity.",
    2: "Loan officers reported delays in payments for personal loans. The bank wants to review which loans are currently late and how much the outstanding amount is for each customer.",
    3: "The risk department is concerned about customers with multiple high-value transactions. They need to find the top 10 customers by total transaction amount in the last quarter.",
    4: "Customer service received complaints about accounts with negative balances. The team wants to analyze which accounts have gone below zero and the frequency of these events.",
    5: "The bank wants to see which loan types are most popular among customers in the last year, in order to tailor marketing campaigns for new products.",
    6: "Branch managers want to track staff performance. They need a report showing employees in each branch and how long they've been with the bank.",
    7: "The compliance team wants to identify any cards that have been blocked or expired recently, to ensure proper follow-up with customers.",
    8: "The bank marketing team is curious which branches have the highest number of new customers joining this year, to understand branch growth trends.",
    9: "The fraud detection team wants to spot unusually large card transactions over $2,000 in a single day, to investigate potential fraudulent activity.",
    10: "Management wants to understand which branches generate the most interest from loans, summing up the interest rates times loan amounts for active loans.",
    11: "Customer retention analysts want to see which customers have multiple accounts across different branches, indicating loyalty or high engagement.",
    12: "The operations team noticed delays in account openings. They want a list of accounts opened in the last 30 days along with their customer names and branch locations.",
    13: "The credit department wants to monitor loan payments. They need a report of the total payments made per loan over the last year.",
    14: "The bank is exploring which customers use multiple contact methods (email and phone). They want to identify these customers for cross-channel communication campaigns.",
    15: "Management wants insights into card usage patterns: which merchants see the most transactions and total spend across all customers in the last six months."
},
    databases[11]:
    {
    1: "The operations team wants to identify drivers with the highest cancellation rates in the last 3 months to improve service reliability.",
    2: "Marketing is interested in riders who have used promotions frequently, aiming to analyze their ride frequency and value.",
    3: "Customer support received complaints about long trip durations in certain cities; they want to investigate average trip times by city and time of day.",
    4: "The safety team wants to flag drivers with multiple low ratings (2 stars or below) in the past 6 months for further review.",
    5: "Finance wants to analyze payment methods distribution and failed payments over the last year to optimize transaction processes.",
    6: "The fleet management wants to check vehicles with upcoming registration expiry dates to ensure compliance.",
    7: "The app development team wants to analyze ride distances and fare amounts to detect any unusual pricing or errors.",
    8: "Customer loyalty program managers want to find riders who took at least 20 rides last year and never used promotions, targeting them for new offers.",
    9: "Operations want to track average wait times between trip end and next trip start for drivers to optimize efficiency.",
    10: "Marketing wants to identify cities with the highest number of active riders and drivers to focus regional campaigns.",
    11: "The fraud detection team suspects some riders use multiple accounts to exploit promotions and wants to find riders with overlapping payment methods.",
    12: "The HR team wants to analyze driver join dates and current status to forecast driver availability in the coming months.",
    13: "Customer satisfaction team wants to analyze correlation between driver ratings and trip cancellation status.",
    14: "Finance wants to summarize total revenue from trips with applied promotions vs without promotions.",
    15: "The analytics team wants to identify peak hours for trips across cities to improve surge pricing models."
    }
    }

def page():
    st.write("")
    st.write("")
    with st.container(border = True):
        
        c,c1,c,c0 = st.columns([.15,3,.1,1])
        with c1:
            st.markdown("<div style='text-align: center'><h4>Let's start with your field of interest:</h4>", unsafe_allow_html=True)
            #st.write("")
            c1,c2,c3 = st.columns(3)
            with c1:
                if st.button("E-Commerce", use_container_width=1):
                    ss.db = databases[0]
                if st.button("Flight Booking", use_container_width=1):
                    ss.db = databases[1]
                if st.button("University", use_container_width=1):
                    ss.db = databases[2]
                if st.button("Social Media", use_container_width=1):
                    ss.db = databases[3]
            with c2:
                if st.button("Retail POS", use_container_width=1):
                    ss.db = databases[4]
                if st.button("Supply Chain", use_container_width=1):
                    ss.db = databases[5]
                if st.button("Hospital", use_container_width=1):
                    ss.db = databases[6]
                if st.button("Human Resource", use_container_width=1):
                    ss.db = databases[7]
            with c3:
                if st.button("Event ROI", use_container_width=1):
                    ss.db = databases[8]
                if st.button("Call Center", use_container_width=1):
                    ss.db = databases[9]
                if st.button("Banking", use_container_width=1):
                    ss.db = databases[10]
                if st.button("Ride Sharing", use_container_width=1):
                    ss.db = databases[11]
            st.write("")
        with c0:
            for i in databases:
                if ss.db == i:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.image(i+".jpeg",width=120)
        c0,c,c0 = st.columns([.02,1,.02])
        with c:
            try:
                st.success(descriptions[ss.db])
            except:
                pass
        st.write("")
    st.write("")
    st.write("")
    c1,c2 = st.columns([1,1.5])
    with c1:
        with st.popover("Save / Load Data", use_container_width=1):
            action = st.radio("Choose your action:",["Load","Save"], key = "save_load")
            if action == "Load":
                uploaded_file = st.file_uploader("Upload your saved data:")
                if (uploaded_file is not None) and st.button("Load this save data"):
                    open_save_file(uploaded_file)

            elif action == "Save":
                create_save_file(password)
    with c2:
        if st.button("Check My Progress", use_container_width=1):
            check_my_progress()
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    for n,t in questions[ss.db].items():
        write_questions(ss.db,n,t)
        st.write("")


    
    