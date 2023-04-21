import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit.components.v1 as components
import requests       
from streamlit_lottie import st_lottie  
from PIL import Image


### ---- READ BEFOR RUNNING: --- ### 
# You need to intsall the following in the terminal to run the app:
# pip install streamlit
# pip install requests
# pip install streamlit_lottie


### ---- LOADING DATA ---- ###

# Filename Variables
path = './data/'
flightsMonth = path + 'agg_flightsMonth.csv' 
flightsDay = path + 'agg_flightsDay.csv'     
airlinesTotal = path + 'agg_airlinesMonth.csv'

# Dataframe aggregate arrivals per month
aggMonth = pd.read_csv(flightsMonth)

# Dataframe aggregate arrivals per day per month
aggDay = pd.read_csv(flightsDay)

# Dataframe aggregate arrivals per airline per month
airlinesMonth = pd.read_csv(airlinesTotal)


### ---- FILTERS ---- ###
monthNames = aggMonth.MONTH_NAME.unique()


### ---- FUNCTIONS ---- ###

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_Fuugw4oaSM.json")


def setVariables(df):
    '''
    Receive a dataframe and make some calculations
        sum of total arrivals, delayed arrivals and on-time arrivals
        mean of delayed arrivals
        percentage of delayed and on-time arrivals
    return a dictionary
    '''

    results = {}

    results['total'] = "{:,}".format(df.COUNTS.sum())
    results['delayed'] = "{:,}".format(df[df['STATUS'] == 'DELAYED']['COUNTS'].sum())
    results['onTime'] = "{:,}".format(df[df['STATUS'] == 'ON_TIME']['COUNTS'].sum())
    results['avgDelayed'] = "{:,.2f}".format(df[df['STATUS'] == 'DELAYED']['COUNTS'].mean())
    results['pctDelayed']= "{:.2%}".format(df[df['STATUS'] == 'DELAYED']['COUNTS'].sum()/df.COUNTS.sum())
    results['pctonTime'] = "{:.2%}".format(df[df['STATUS'] == 'ON_TIME']['COUNTS'].sum()/df.COUNTS.sum())

    return results


### ---- BUILDING THE PAGE (Streamlit) ---- ###

# --- WEB SITE LAYOUT CONFIGURATION --- #
st.set_page_config(
    page_title="Georgia Tech - Flight Delay Prediction", 
    page_icon=":tada", 
    layout="centered")

# --- PAGE TITLE --- #
st.title("Analyzing the 2015 Flight Delays Dataset :airplane_departure:")


# --- INTRODUCTION ---
with st.container():
    st.write("---")
    st.header('Introduction and Motivation')
    st.write('##')
    left_column, right_column = st.columns(2)
    with left_column:
        st.write(
            '''
            Delayed flights can have significant negative economic impacts on airlines, airports, and passengers which motivates the analysis of the phenomenon.
            Our project consists of two parts: analyzing flight and weather datasets and predicting flight delays. 
            This website shows an analysis using a dataset worth of all US flight delays in 2015 and another a weather dataset gathered by performing web-scraping.  
            We have used data visualization techniques to display the data distribution and identified trends and seasonal patterns.         
            '''
        )
    with right_column:
        st_lottie(lottie_coding, height=300, key='coding')


# --- SUMMARY SECTION --- #
with st.container():
    st.write("---")
    st.subheader('Overview: 2015 Total Flight Arrivals in the US')
    st.write('##')

    general = setVariables(aggMonth)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Arrivals 2015", general['total'])
    col2.metric("Delayed Arrivals", general['delayed'])
    col3.metric("On-time Arrivals", general['onTime'])

    col1a, col2a, col3a = st.columns(3)
    col1a.metric("Average Delayed Arrivals (per month)", general['avgDelayed'])
    col2a.metric("% Delayed Arrivals", general['pctDelayed'])
    col3a.metric("% On-time Arrivals", general['pctonTime'])

    # CHART: Total Fligh Arrivals per Status
    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682111299602' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015TotalFlightArrivalsintheUS&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='2015TotalFlightArrivalsintheUS&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015TotalFlightArrivalsintheUS&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682111299602');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height =500, width = 800)
    if __name__ == "__main__":    
        main()

# --- KPIS PER MONTH PER DAY --- # 
with st.container():
    st.write("---")
    st.subheader('Key Performance Indicators per Month During 2015')
    st.write('##')
    with st.spinner(text="In progress..."):
        with st.expander("Click to expand/contract the visualization", expanded=False):
            cl1, empty_col1, empty_col2 = st.columns(3)
            with cl1:
                monthSelected = st.selectbox(
                    'Select the month:',
                    (monthNames)
                )

            monthTitle = datetime.datetime.strptime(monthSelected.upper(),'%b').strftime('%B')

            st.markdown("**Arrivals During " + monthTitle + " 2015**")

            dfMonth = setVariables(aggDay[(aggDay['MONTH_NAME'] == monthSelected)])
            col4, col5, col6 = st.columns(3)
            title_m = "Total Arrivals on " + monthTitle
            col4.metric("Total Arrivals 2015", dfMonth['total'])
            col5.metric("Delayed Arrivals", dfMonth['delayed'])
            col6.metric("On-time Arrivals", dfMonth['onTime'])

            col4a, col5a, col6a = st.columns(3)
            col4a.metric("Average Delayed Arrivals (per day)", dfMonth['avgDelayed'])
            col5a.metric("% Delayed Arrivals", dfMonth['pctDelayed'])
            col6a.metric("% On-time Arrivals", dfMonth['pctonTime'])


            data = aggDay[(aggDay['MONTH_NAME'] == monthSelected)]

            data_mean = aggDay[((aggDay['MONTH_NAME'] == monthSelected)) & (aggDay['STATUS']=='DELAYED')]['COUNTS'].mean()
            fig_2 = plt.figure(figsize=(10, 4))
            ax = sns.lineplot(data=data, x="DAY", y="COUNTS", hue="STATUS", markers=True, dashes=False, marker="o")
            ax.set(xlabel= "Days",
                ylabel='Total Arrivals',
                title=title_m,
                xticks=aggDay.DAY.values
                )

            st.pyplot(fig_2)


            st.markdown("**Arrivals by Airline During " + monthTitle + " 2015**")

            # Initialize the matplotlib figure
            fig_3, ax = plt.subplots(figsize=(10, 4))

            # Load dataset
            airlines = airlinesMonth[(airlinesMonth['MONTH_NAME'] == monthSelected)].sort_values("TOTAL_COUNT", ascending=False)

            # Plot - Total arrivals
            sns.set_color_codes("pastel")
            sns.barplot(x="TOTAL_COUNT", y="AIRLINE_y", data=airlines,
                        label="Total arrivals", color="b")

            sns.set_color_codes("muted")
            sns.barplot(x="DELAYS_COUNT", y="AIRLINE_y", data=airlines,
                        label="Delays", color="b")

            # Add a legend and informative axis label

            ax.legend(ncol=2, loc="lower right", frameon=True)
            ax.set(ylabel="",
                xlabel="ARRIVALS")
            sns.despine(left=True, bottom=True)

            st.pyplot(fig_3)

# --- CHOROPLETH --- #
with st.container():
    st.write("---")
    st.subheader('The majority of the delayed flights in 2015 were registered in California and Texas')
    st.write('##')
    st.write(
        '''
        The below map displays the number of flight delays per state registered in 2015. This interactive chart allows to visualizing the number of flight delays registered per month per state.
        Califonia and Texas consistently registered the greatest amount of flight delays.
        
        Use the drop-down list below and select a month to see the states with the highest amount of reported arrival delayed flights.
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682113978618' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelaysperState&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />  
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='2015FlightDelaysperState&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelaysperState&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682113978618');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='827px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='827px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 800, width = 850)
    if __name__ == "__main__":    
        main()

# --- TREEMAP --- #
with st.container():
    st.write("---")
    st.subheader('A total of 14 airlines were evaluated and their performance varies depending on the destination state')
    st.write('##')
    st.write(
        '''
        The airlines accumulating the most delays are Southwest Airlines, Delta Airlines, and American Airlines. 
        This is not very surprising, given their relatively low cost and volume with tighter margins.

        Use the drop-down list below and select a state(s) to see the airlines with the highest amount of reported arrival delayed flights.
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682114337467' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelaysperAirline&#47;Dashboard2&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='2015FlightDelaysperAirline&#47;Dashboard2' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelaysperAirline&#47;Dashboard2&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682114337467');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='677px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='677px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 650, width = 850)
    if __name__ == "__main__":    
        main()

# --- TOP 5 AIRPORTS --- #
with st.container():
    st.write("---")
    st.subheader('Valdez Airport was the airport with the shortest average arrival delay. Similarly, the Sawyer International Airport was registered as the worst airport based on the same metric.')
    st.write('##')
    st.write(
        '''
        The top 5 airports with the most delays are located in the Northeast/Midwest region. These airports are smaller and are most susceptible to flight disruptions because the carriers serving them have restricted capabilities in bad weather. Also these airports are located in regions more likely to experience bad weather conditions. 
        
        The airports averaging the least delays are mostly located in Alaska, New York, Idaho and Rhode Island. These airports have the lowest rates of arrival delay, and they are not very popular destination cities. When it comes to Alaska, most travlers visit by boat.
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682111544986' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 3 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelays-Top5Airports&#47;Dashboard3&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='2015FlightDelays-Top5Airports&#47;Dashboard3' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;20&#47;2015FlightDelays-Top5Airports&#47;Dashboard3&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682111544986');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='827px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='827px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='977px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 800, width = 850)
    if __name__ == "__main__":    
        main()

# --- TIME SERIES ANALYSIS: MONTHS --- #
with st.container():
    st.write("---")
    st.header('Time Series Analysis')
    st.subheader('Mean Flight Delays by Month')
    st.write('##')
    st.write(
        '''
        There is not much variation when it comes to the month or day of the week, but we can observe that February, July, June and December are the months with the highest amount of delays. This can probably be explained by the fact that December and February are busy travel months during the winter, due to cheaper costs, and lower temperatures can definitely affect flight departures. Not only is June a summer month, a time when there is heavy traffic volume, but it is also during peak tornado season (these are among the top causes of flight delays).
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682111579408' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightsDelaysbyMonth&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='MeanFlightsDelaysbyMonth&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightsDelaysbyMonth&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682111579408');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 500, width = 800)
    if __name__ == "__main__":    
        main()

# --- TIME SERIES ANALYSIS: WEEKS --- #
with st.container():
    st.subheader('Mean Flight Delays by Day of Week')
    st.write('##')
    st.write(
        '''
        Monday is the day of the week with the highest average arrival delay. The heaviest traffic volume occurs on Mondays which could lead to potentially more delays
        
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682113033059' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyDayofWeek&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='MeanFlightDelaysbyDayofWeek&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyDayofWeek&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682113033059');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 500, width = 800)
    if __name__ == "__main__":    
        main()

# --- TIME SERIES ANALYSIS: HOURS --- #
with st.container():
    st.subheader('Mean Flight Delays by Hour')
    st.write('##')
    st.write(
        '''
        Evening flights are also most likely to be delayed, this is correlated to heavy traffic volume because passengers prefer evening travels due to work schedule or school.
        
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682112840957' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyHour&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='MeanFlightDelaysbyHour&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyHour&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1682112840957');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='800px';vizElement.style.height='527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='800px';vizElement.style.height='527px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
        """
        components.html(html_temp,height = 500, width = 800)
    if __name__ == "__main__":    
        main()

# --- WEATHER ANALYSIS: TEMPERATURE --- #
with st.container():
    st.write("---")
    st.header('Weather Analysis')
    st.subheader('Mean Flight Delays by Origin Temperatures')
    st.write('##')
    st.write(
        '''
        On the histogram below, temperatures between -20 and 20 degrees account for the most flight delays. Lower temperatures may cause the oil in the turbine engine to become so thick that it would be difficult to start the engine, hence causing flight delays. Under extreme heat conditions, it may be harder for planes to fly, as warm air expands and is less dense, so the plane needs more fuel to transport the same amount of passengers and cargo.
        
        '''
    )

    def main():
        html_temp = """
        <div class='tableauPlaceholder' id='viz1682112914127' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyOriginTemperatures&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='MeanFlightDelaysbyOriginTemperatures&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyOriginTemperatures&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682112914127');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 500, width = 800)
    if __name__ == "__main__":    
        main()

# --- WEATHER ANALYSIS: WIND SPEED --- #
with st.container():
    st.subheader('Mean Flight Delays by Origin Wind Speed')
    st.write('##')
    st.write(
        '''
        High wind speeds are correlated with higher average delays. Although there is no single maximum wind limit for planes, a crosswind above 40 mph and a tailwind above 10 mph can cause flight delays and cancellations, which explains the distribution of mean flight delays grouped by wind speed ranges.
        
        '''
    )

    def main():
        html_temp = """
        
        <div class='tableauPlaceholder' id='viz1682112120034' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyOriginWindSpeed&#47;Dashboard1&#47;1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz'  style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
                <param name='embed_code_version' value='3' /> 
                <param name='site_root' value='' />
                <param name='name' value='MeanFlightDelaysbyOriginWindSpeed&#47;Dashboard1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Me&#47;MeanFlightDelaysbyOriginWindSpeed&#47;Dashboard1&#47;1.png' /> 
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>                
        
        <script type='text/javascript'>                    
            var divElement = document.getElementById('viz1682112120034');                    
            var vizElement = divElement.getElementsByTagName('object')[0];                    
            if ( divElement.offsetWidth > 800 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else if ( divElement.offsetWidth > 500 ) { 
                vizElement.style.width='800px';
                vizElement.style.height='527px';
            } else { 
                vizElement.style.width='100%';
                vizElement.style.height='727px';}                     
            var scriptElement = document.createElement('script');                    
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
            vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
        """
        components.html(html_temp,height = 500, width = 800)
    if __name__ == "__main__":    
        main()
