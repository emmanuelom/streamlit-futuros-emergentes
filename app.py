import streamlit as st
from streamlit_extras.app_logo import add_logo
from custom_echarts.graph import load_data, render_graph, render_generic_graph, generate_generic_graph_data
import pandas as pd
import ast
import json


# Path to data & images
DATA = {"Agroindustrial": ["graphs/agroindustry.json", "AGROINDUSTRY"],
        "Fabricación Automotores": ["graphs/automotive_manufacture.json", "AUTOMOTIVE"],
        "Energia y Agua": ["graphs/energy_and_water.json", "ENERGY_AND_WATER"],
        "Moda" : ["graphs/fashion.json", "FASHION"],
        "Turismo" : ["graphs/turism.json", "TURISM"],
        "Ciencias de la vida" : ["graphs/health.json", "HEALTH"]}

IMGS = {"logoIDEA": "images/200-Anos-ideaGTO.png",
        "logoLASALLE": "images/ulsa-logo.png"}


# main interface: sliderbar, graph & info container
def main():        
    st.title("Futuros Emergentes")
    with st.sidebar:
        st.image(IMGS["logoIDEA"])
        st.markdown("---")
        st.image(IMGS["logoLASALLE"])
        st.markdown("---")
        # Sector selector
        st.header("Sector")
        api_options = ("---", "Agroindustrial", "Moda", "Ciencias de la vida", "Movilidad",
                       "Turismo", "Fabricación Automotores", "Productos Químicos",
                       "Servicios basados en conocimientos", "Energia y Agua", "Gobierno"
                    )
        selected_api = st.selectbox(
            label="Selecciona una opción",
            options=api_options,
        )
        st.markdown("---")

        # Interest selector
        st.header("Eje")
        sub_options = ("---", "Tecnológico", "Profesional", "Científico")
        selected_option = st.selectbox(
            label="Selecciona una opción",
            options=sub_options,
        )
        st.markdown("---")

        # Caption
        st.caption(
                """Investigación de futuros: Prospectiva de tendencias científicas y tecnológicas en Guanajuato"""
            )
    
    # Create a list op api options
    api_list = list(api_options)
    api_list = api_list[1:]
        
    # Add Sector subheader 
    st.subheader(f"Sector: {selected_api if selected_api != '---' else ' Seleccione un sector'}")

    # Add the graph container
    plot_container = st.container(border=True)

    # Add Eje subheader
    st.subheader(f"Eje: {selected_option if selected_option != '---' else 'Seleccione un eje'}")

    # Add Information container
    info_container = st.expander("Ver más información")

    # Verify the sector selection
    if selected_api in api_list:
        # get data folder name
        data_folder = DATA[selected_api][1] 
        # load selected sector data
        data = load_data(DATA[selected_api][0])

        #print(f"Data from {DATA[selected_api][0]}: {data}")
        #data = generate_generic_graph_data()

        # Plot graph
        with plot_container:
            selected_node = render_graph(data, width="100%", height="700px", label_font_size=12)
            #selected_node = render_generic_graph(data, width="100%", height="700px", label_font_size=12)
        
        # Verify selected node is a subnode
        if selected_node and selected_node['symbolSize']==20:
            #print(f"Selected node size: {selected_node['symbolSize']==20}")
            with info_container:
                # show Patent Pulse information
                #print(f'Selected option: {selected_option}')
                if selected_option == 'Tecnológico' or selected_option == 'Científico':
                    # check if selected option is Tecnologico or Cientifico to load the data
                    sel_op = 'ppulse' if selected_option == 'Tecnológico' else 'scopus'
                    st.markdown(f"Associated top categories for **{selected_node['name']}**")
                    
                    try:    
                        df_central_node = pd.read_csv(f"data/{data_folder}/{sel_op}_{selected_node['name']}.csv")
                        #pd.read_csv(selected_node['info'])
                        
                        #
                        df_central_node['All Years'] = df_central_node['All Years'].apply(lambda x: ast.literal_eval(x))

                        # Extract all lists from 'All Years' column
                        all_years_lists = df_central_node['All Years'].tolist()
                        

                        # Flatten the lists into a single list
                        flattened_list = [item for sublist in all_years_lists for item in sublist]
                        num_years = len(all_years_lists[0])


                        # Find the maximum value in the flattened list
                        max_value = max(flattened_list)

                        #st.dataframe(df_central_node) 
                        st.dataframe(
                            df_central_node,
                            column_config={
                                f"{'Categories' if selected_option == 'Tecnológico' else 'Dominant_Topic_Label'}": "Categories",
                                "All Years": st.column_config.LineChartColumn( # BarChartColumn
                                    f"{'Patents' if selected_option == 'Tecnológico' else 'Papers'} ({2024-num_years}-2024)", y_min=0, y_max=max_value, 
                                    width="large",
                                ),
                                
                            },
                            hide_index=True,
                        )
                    except: 
                        st.write(f"Sin información disponible de {selected_node['name']} en el eje {selected_option}")
                elif selected_option == "Profesional":
                    st.markdown(f"Associated trend hunter topic for **{selected_node['name']}**")
                    try:
                        file_th = f"data/{data_folder}/trend_{selected_node['name']}.json"
                        with open(file_th) as f:
                            d = json.load(f)
                        st.markdown(f"**Summary:** {d['info']}")
                        st.page_link(d['url'], label="Trend Hunter", icon="🌎")
                        #st.markdown("[![Foo](https://cdn.trendhunterstatic.com/phpthumbnails/485/485683/485683_1_468d.jpeg)](https://www.trendhunter.com/report?ak=cr_3764e3c6095a42fb08e3a9c6d0ca1#idea=485683)")
                    except: 
                        st.write(f"Sin información disponible en el eje {selected_option}")
                else:
                    st.write(f"Sin información disponible en el eje {selected_option}")
        elif selected_node['symbolSize']==30:
            with info_container:
                st.write(f"Info about parents nodes")
        else:
            with info_container:
                st.write(f"Info about main node (Sector)")



    elif selected_api != "---":
        with plot_container:
            st.write(f"Grafo {selected_api} no disponible.")


if __name__ == "__main__":
    # Set page configuration: MUST be call here
    st.set_page_config(
        page_title="Futuros Emergentes", layout="wide" , page_icon=":robot_face:"
    )
    # Call main API
    main()

    # Add a custom footer.
    footer = """<style>.footer {position: fixed;left: 0;bottom: 0;width: 100%;background-color: #1d285c;color: white;text-align: center;}
    </style><div class='footer'><p>Universidad De La Salle Bajío - Dirección de Investigación y Doctorado &copy; Copyright 2024. <br /> Investigación de futuros: Prospectiva de tendencias científicas y tecnológicas en Guanajuato. Con clave IDEA GTO/SG/386/2023</p></div>"""
    st.markdown(footer, unsafe_allow_html=True)
