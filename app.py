import streamlit as st
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from meteostat import Stations, Daily, Point, Hourly
from datetime import datetime, timedelta



# Set page config

st.set_page_config(
    page_title="Malaria warning",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Cities info for automatic prediction
cities = ['Malanville','Natitingou', 'Kouandé','Parakou', 'Cotonou', 'Abomey-Calavi', 'Porto-Novo', 'Bohicon',
            'Savè', 'Abomey',  'Lokossa', 'Ouidah','Covè' , 'Athiémé','Kandi', 'Ségbana',  'Pobè',  'Savalou', 'Sakété',
            'Comè','Dogbo-Tota', 'Kétou', 'Dassa-Zoumè', 'Tchaourou', 'Allada','Bembéréké', 'Bassila',
          'Banikoara', 'Aplahoué', 'Tanguiéta', 'N\'Dali',  'Grand-Popo', 'Kérou','Nikki', 'Djougou']

coordinates = {
    'Cotonou': Point(6.3676953,2.4252507, 7),
    'Abomey-Calavi': Point(6.5109623,2.3303076, 31),
    'Porto-Novo': Point(6.4990718,2.6253361, 20),
    'Parakou': Point(9.3400159,2.6278258, 369),
    'Djougou': Point(9.7106683,1.6651614, 444),
    'Bohicon': Point(7.1816331,2.0695683, 166),
    'Natitingou': Point(10.2514083,1.383541, 450),
    'Savè': Point(7.985217,2.5417577, 189),
    'Abomey': Point(7.165446,1.9828804,  228),
    'Nikki': Point(9.899685,3.1780254, 295),
    'Lokossa': Point(6.6458524,1.7171404, 49),
    'Ouidah': Point(6.3666147,2.0853599, 17 ),
    'Dogbo-Tota': Point(6.801846,1.7815205, 69),
    'Kandi': Point(11.134233, 2.938215, 334),
    'Covè': Point(11.2849785,3.0464209, 206),
    'Malanville': Point(11.8618128,3.3862982, 223),
    'Pobè': Point(6.9820238,2.666791, 197),
    'Kérou': Point(10.972115,1.9983428, 197),
    'Savalou': Point(7.9297324,1.9780951, 181),
    'Sakété': Point(6.7440318,2.6765507, 50),
    'Comè': Point(6.4305976,1.9000602, 20),
    'Bembéréké': Point(10.2539589,2.7507427, 302),
    'Bassila': Point(8.9666644,1.8218397, 225),
    'Banikoara': Point(11.3262542,2.4730407, 355),
    'Kétou': Point(7.3604193,2.6024222, 212),
    'Dassa-Zoumè': Point(7.7815402,2.183606, 157),
    'Tchaourou': Point(8.8881676,2.596108, 206),
    'Allada': Point(6.6658411,2.1511876, 41),
    'Aplahoué': Point(6.9489244,1.7041012, 59),
    'Tanguiéta': Point(10.965512,1.4203383, 346),
    "N'Dali": Point(9.6883335,2.4633607, 329),
    'Ségbana': Point(10.9286988,3.6952064, 289),
    'Athiémé': Point(6.5322971,1.7414349, 7),
    'Grand-Popo': Point(6.2763745,1.8067199, 2),
    'Kouandé': Point(10.3321794,1.6919847, 362),
}

# Fit the SVR model for the manuel prediction
LoR = pd.read_csv("Average_Northern.csv")
LoR = LoR.dropna()
LoR1 = LoR.iloc[:, 0:11]
data= LoR1.iloc[0:90, :]
X= data[['Prec_Average', 'Average_Temperature_Max', 'Average_RH_Max']]
y= data['Malaria_incidence']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)
svr_model = SVR(kernel='rbf',epsilon=0.1)
svr_model.fit(X_train, y_train)
#For prediction status displayed
word_style = "font-weight: bold; font-size:32px ;font-family: Arial;"
#In side bar
language = st.sidebar.selectbox('Translate/Traduire', ['Français','English'])
#Interface


# Display text based on language selection
if language == 'Français':
    st.markdown("<span style='font-weight: bold; font-size:34px; color:blue;font-family: Arial;background-color: lightblue; padding: 10px;'>Application d'alerte en cas d'épidémie de paludisme</span>", unsafe_allow_html=True)
    st.sidebar.markdown("#### Comment ça marche?")
    st.sidebar.write("Choisir une ville pour une prédiction en temps réel")
    st.sidebar.write("OU")
    st.sidebar.write("Renseigner les données d'entrée manuellement en glissant les curseurs")

    col1, col2 = st.columns(2)
    # Interface in the left column

        # Interface in the right column
    with col1:
        def user_input():
            input_var1 = st.slider('Précipitation', 0, 500, 500)
            input_var2 = st.slider('Température ', 29, 11, 100)
            input_var3 = st.slider('Humidité relative ', 0, 100, 100)
            data = {'Prec_Average': input_var1,
                    'Average_Temperature_Max': input_var2,
                    'Average_RH_Max': input_var3}
            input_data = pd.DataFrame(data, index=[0])
            return input_data
        df = user_input()
        prediction = svr_model.predict(df)
        prediction=prediction*0.39318
        st.write("Incidence du Paludisme:", "{:.2f}".format(prediction[0]), "%")

        if (prediction[0] >= 0 and prediction[0] < 5):
            st.markdown('Statut: <span style="{}">Très faible</span>'.format("color:blue;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 5 and prediction[0] < 15):
            st.markdown('Statut: <span style="{}">Faible</span>'.format("color:green;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 15 and prediction[0] < 30):
            st.markdown('Statut: <span style="{}">Modéré</span>'.format("color:orange;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 30 and prediction[0] < 50):
            st.markdown('Statut: <span style="{}">Elevé</span>'.format("color:pink;", word_style),
                                unsafe_allow_html=True)
        else:
            st.markdown('Statut: <span style="{}"> Très élevé</span>'.format("color:red;", word_style),
                                unsafe_allow_html=True)
    with col2:
        #st.write("Voulez-vous une prédiction automatique sur les données météo actuelles?")
        city = st.selectbox('Choisir une ville', cities)
        start = datetime.now() - timedelta(days=30)
        end = datetime.now()
        data = Hourly(coordinates[city], start, end)
        data = data.fetch()
        prec = data['prcp'].mean() * 1000
        temp = data['temp'].max()
        hum = data['rhum'].max()

        auto_data = {'Prec_Average': prec,
                     'Average_Temperature_Max': temp,
                     'Average_RH_Max': hum}
        auto_df = pd.DataFrame(auto_data, index=[0])
        st.markdown(
            '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">',
            unsafe_allow_html=True)
        # Display icons
        st.markdown(f'<i class="fa fa-tint"></i> Précipitation : {prec:.2f} mm', unsafe_allow_html=True)
        st.markdown(f'<i class="fa fa-thermometer-empty"></i> Température : {temp:.2f} °C', unsafe_allow_html=True)
        st.markdown(f'<i class="fa fa-tachometer"></i> Humidité : {hum:.2f} %', unsafe_allow_html=True)
        if auto_df.isnull().values.any():
           # st.markdown('<span style="color:red;">Echec de Prédiction</span>', unsafe_allow_html=True)
            st.markdown('<span style="color:red;">Données indisponibles, essayez une ville proche</span>',
                        unsafe_allow_html=True)

        else:
            # st.dataframe()
            auto_prediction = svr_model.predict(auto_df)
            st.write("Incidence  actuelle du paludisme:", "{:.2f}".format(auto_prediction[0]), "%")
            if (auto_prediction[0] >= 0 and auto_prediction[0] < 5):
                st.markdown('Statut: <span style="{}">Très faible</span>'.format("color:blue;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction >= 5 and auto_prediction[0] < 15):
                st.markdown('Statut: <span style="{}">Faible</span>'.format("color:green;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction[0] >= 15 and auto_prediction[0] < 30):
                st.markdown('Statut: <span style="{}">Modéré</span>'.format("color:orange;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction[0] >= 30 and auto_prediction[0] < 50):
                st.markdown('Statut: <span style="{}">Elevé</span>'.format("color:pink;", word_style),
                            unsafe_allow_html=True)
            else:
                st.markdown('Statut: <span style="{}"> Très élevé</span>'.format("color:red;", word_style),
                            unsafe_allow_html=True)


else:
    title = "My Title"


    st.markdown(f"<span style='font-weight: bold; font-size:46px; color:blue;font-family: Arial;background-color: lightblue; padding: 10px;'>Malaria Outbreak Warning Application</span>", unsafe_allow_html=True)
    st.sidebar.markdown("#### How does it work?")
    st.sidebar.write("Choose a city for real-time prediction")
    st.sidebar.write("OR")
    st.sidebar.write("Enter input data by dragging cursors")
    col1, col2 = st.columns(2)
    # Interface in the left column
    with col1:
        def user_input():
            input_var1 = st.slider('Precipitation', 0, 1000, 1000)
            input_var2 = st.slider('Average maximum temperature', 29, 11, 40)
            input_var3 = st.slider('Maximum relative humidity', 0, 100, 100)
            data = {'Prec_Average': input_var1,
                    'Average_Temperature_Max': input_var2,
                    'Average_RH_Max': input_var3}
            input_data = pd.DataFrame(data, index=[0])
            return input_data
        df = user_input()
        prediction = svr_model.predict(df)
        st.write("Incidence of malaria:", "{:.2f}".format(prediction[0]), "%")

        if (prediction[0] >= 0 and prediction[0] < 5):
            st.markdown('Statut: <span style="{}">Very low</span>'.format("color:blue;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 5 and prediction[0] < 15):
            st.markdown('Statut: <span style="{}">Low</span>'.format("color:green;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 15 and prediction[0] < 30):
            st.markdown('Statut: <span style="{}">Medium</span>'.format("color:orange;", word_style),
                                unsafe_allow_html=True)
        elif (prediction[0] >= 30 and prediction[0] < 50):
            st.markdown('Statut: <span style="{}">High</span>'.format("color:pink;", word_style),
                                unsafe_allow_html=True)
        else:
            st.markdown('Statut: <span style="{}"> Very high</span>'.format("color:red;", word_style),
                                unsafe_allow_html=True)

    # Interface in the right column
    with col2:
        #st.write("Would you like an automatic prediction based on current weather data?")
        city = st.selectbox('Choose a city', cities)
        start = datetime.now() - timedelta(days=30)
        end = datetime.now()
        data = Hourly(coordinates[city], start, end)
        data = data.fetch()
        prec = data['prcp'].mean() * 1000
        temp = data['temp'].max()
        hum = data['rhum'].max()

        auto_data = {'Prec_Average': prec,
                     'Average_Temperature_Max': temp,
                     'Average_RH_Max': hum}
        auto_df = pd.DataFrame(auto_data, index=[0])
        st.markdown(
            '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">',
            unsafe_allow_html=True)
        # Display icons
        st.markdown(f'<i class="fa fa-tint"></i> Precipitation : {prec:.2f} mm', unsafe_allow_html=True)
        st.markdown(f'<i class="fa fa-thermometer-empty"></i> Temperature : {temp:.2f} °C', unsafe_allow_html=True)
        st.markdown(f'<i class="fa fa-tachometer"></i> Humidity : {hum:.2f} %', unsafe_allow_html=True)
        if auto_df.isnull().values.any():
            #st.markdown('<span style="color:red;">Prediction failure</span>', unsafe_allow_html=True)
            st.markdown('<span style="color:red;">Data unavailable, try a nearby city</span>',
                        unsafe_allow_html=True)
        else:
            # st.dataframe()
            auto_prediction = svr_model.predict(auto_df)
            st.write("Incidence of malaria today:", "{:.2f}".format(auto_prediction[0]), "%")
            if (auto_prediction[0] >= 0 and auto_prediction[0] < 5):
                st.markdown('Statut: <span style="{}">Very low</span>'.format("color:blue;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction >= 5 and auto_prediction[0] < 15):
                st.markdown('Statut: <span style="{}">Low</span>'.format("color:green;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction[0] >= 15 and auto_prediction[0] < 30):
                st.markdown('Statut: <span style="{}">Medium</span>'.format("color:orange;", word_style),
                            unsafe_allow_html=True)
            elif (auto_prediction[0] >= 30 and auto_prediction[0] < 50):
                st.markdown('Statut: <span style="{}">High</span>'.format("color:pink;", word_style),
                            unsafe_allow_html=True)
            else:
                st.markdown('Statut: <span style="{}"> Very high</span>'.format("color:red;", word_style),
                            unsafe_allow_html=True)






