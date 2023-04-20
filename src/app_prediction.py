import streamlit as st
import pandas as pd
import pickle

with st.spinner('Loading...'):
    ### ---- LOADING DATA ---- ###

    path = './data/'
    df_airlines = pd.read_csv(path + 'airlinesMap.csv')
    df_airports = pd.read_csv(path + 'originAirportMap.csv')
    df_dest_airports = pd.read_csv(path + 'destinAirportMap.csv')


    ### ---- VARIABLES ---- ###
    result = ''
    model_pkl = 'flight_delay.pkl'
    hours = [hr for hr in range(0, 24)]
    airlines_names = dict(zip(sorted(df_airlines.AIRLINE), df_airlines.AIRLINE_CODE))
    airports = dict(zip(sorted(df_airports.AIRPORT), df_airports.ORIGIN_AIRPORT_CODE))
    destAirports = dict(zip(sorted(df_dest_airports.AIRPORT), df_dest_airports.DESTINATION_AIRPORT_CODE))

    # Pressure
    min_pressure = 25.0
    max_pressure = 32.0

    # Relative Humidity
    min_rh = 1
    max_rh = 100

    # Dew Point
    min_dewpt = -0.37
    max_dewpt = 167.0


    ### ---- FUNCTIONS ---- ###
    def load_model():
        '''
        Function that open the file with pre-trained model
        Returns: The model object
        '''

        # Loading pre-trained model
        with open(model_pkl, 'rb') as rf:
            model = pickle.load(rf)
            return model


    def predict(deparHr_selected, arrivalHr_selected, airline_selected,
                airport_selected, dest_airport_selected, pressure,
                pressure_dest, rh, rh_dest, dewpt, dewpt_dest):
        '''
        Function that receives user inputs, send them to pre-trained model and receive predictions
        Args: User Inputs (model predictors)
        Returns: Prediction (0:on time, 1:delay)
        '''

        features = [deparHr_selected, arrivalHr_selected, airline_selected,
                        airport_selected, dest_airport_selected, pressure,
                        pressure_dest, rh, rh_dest, dewpt, dewpt_dest]
        df_features = pd.DataFrame(features).transpose()

        # Making predictions using the pre-trained model
        prediction = model.predict(df_features)
        prediction = int(prediction)

        return prediction



    ### ---- BUILDING THE PAGE (Streamlit) ---- ###

    # Page Title
    st.title("Flight Delays Predictions :airplane_departure:")
    st.markdown("#### Please select data to predict if the flight will be delayed or not.")

    # Web Form
    with st.form("web_form"):
        # Layout 2 columns
        col1, col2 = st.columns(2)

        with col1:
            airline = st.radio('Select Airline', sorted(airlines_names.keys()))

        with col2:
            departureHour = st.selectbox('Select departure hour:', (hours))
            arrivalHour = st.selectbox('Select schedule arrival hour:', (hours))
            airport = st.selectbox('Select the origin airport:', (airports.keys()))
            dest_airport = st.selectbox('Select the destination airport:', (destAirports.keys()))

        colA, colB = st.columns(2, gap="medium")

        with colA:
            pressure = st.slider('Pressure Origin (in):', min_pressure, max_pressure)
            rh = st.slider('Relative Humidity Origin (%):', min_rh, max_rh)
            dewpt = st.slider('Dew Point Origin °F:', min_dewpt, max_dewpt)

        with colB:
            pressure_dest = st.slider('Pressure Destination (in):', min_pressure, max_pressure)
            rh_dest = st.slider('Relative Humidity Destination (%):', min_rh, max_rh)
            dewpt_dest = st.slider('Dew Point Destination °F:', min_dewpt, max_dewpt)


        # Features for prediction model
        deparHr_selected = departureHour
        arrivalHr_selected = arrivalHour
        airline_selected = airlines_names[airline]
        airport_selected = airports[airport]
        dest_airport_selected = airports[dest_airport]

        st.write(" ")
        st.write(" ")

        colleft, colcenter, colright = st.columns(3, gap="large")
        with colcenter:
            button = st.form_submit_button("Predict")
            if button:
                with st.spinner('Predicting...'):
                    # calling pre-trained model
                    model = load_model()
                    # make prediction
                    category = predict(deparHr_selected, arrivalHr_selected, airline_selected,
                                     airport_selected, dest_airport_selected,
                                     pressure, pressure_dest, rh, rh_dest, dewpt, dewpt_dest)
                    if category == 0:
                        result = 'ON TIME'
                    else:
                        result = 'DELAYED'

        with colright:
            if result != '':
                if category == 0:
                    st.success(f'The flight will be {result}', icon="✅")
                else:
                    st.error(f'The flight will be {result}', icon="❌")
