import streamlit as st
from streamlit_extras.app_logo import add_logo
from custom_echarts.graph import load_data, render_graph, render_generic_graph, generate_generic_graph_data
import pandas as pd
import ast
import json


# Path to data & images
DATA_ES = {"Agroindustrial": ["graphs_es/Agroindustria.json", "AGROINDUSTRIA"],
        "Fabricación Automotores": ["graphs_es/automotive_fabricar.json", "AUTOMOTOR"],
        "Energia y Agua": ["graphs_es/energy_y_agua.json", "ENERGÍA Y AGUA"],
        "Moda" : ["graphs_es/moda.json", "MODA"],
        "Turismo" : ["graphs_es/turismo.json", "TURISMO"],
        "Ciencias de la vida" : ["graphs_es/salud.json", "SALUD"]}

IMGS = {"logoIDEA": "images/200-Anos-ideaGTO.png",
        "logoLASALLE": "images/ulsa-logo.png",
        "logoFUTUROS": "images/Logo Radar del Futuro_Color.png"}


@st.cache_data
def read_links(filename):
    df = pd.read_csv(filename, sep=',')
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


# main interface: sliderbar, graph & info container
def main():        
    st.title("Radar del Futuro", anchor=False)
    with st.sidebar:
        st.image(IMGS["logoIDEA"])
        st.markdown("---")
        st.image(IMGS["logoFUTUROS"])
        st.markdown("---")
        # Sector selector
        st.header("Sector", anchor=False)
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
        st.header("Eje", anchor=False)
        sub_options = ("---", "Tecnológico", "Profesional", "Científico")
        selected_option = st.selectbox(
            label="Selecciona una opción",
            options=sub_options,
        )
        
        st.markdown("---")
        st.image(IMGS["logoLASALLE"])

        st.markdown("---")
        st.markdown('<a href="mailto:cbravo@lasallebajio.edu.mx">Contactanos !</a>', unsafe_allow_html=True)
    
    # Create a list op api options
    api_list = list(api_options)
    api_list = api_list[1:]
        
    # Add Sector subheader 
    st.subheader(f"Sector: {selected_api if selected_api != '---' else ' Seleccione un sector'}", anchor=False)

    # Add the graph container
    plot_container = st.container(border=True)

    # Add Eje subheader
    st.subheader(f"Eje: {selected_option if selected_option != '---' else 'Seleccione un eje'}", anchor=False)

    # Add Information container
    info_container = st.expander("Ver más información")

    # Verify the sector selection and if their graph exist
    if selected_api in api_list and selected_api in DATA_ES:
        # get data folder name
        data_folder = DATA_ES[selected_api][1] 
        # load selected sector data
        data = load_data(DATA_ES[selected_api][0])

        # Plot graph
        with plot_container:
            selected_node = render_graph(data, width="100%", height="700px", label_font_size=12)
        
        # Verify selected node is a subnode
        if selected_node and selected_node['symbolSize']==20:
            with info_container:
                # show Patent Pulse information
                if selected_option == 'Tecnológico' or selected_option == 'Científico':
                    # check if selected option is Tecnologico or Cientifico to load the data
                    sel_op = 'ppulse' if selected_option == 'Tecnológico' else 'scopus'
                    st.markdown(f"Top categorias asociadas a: **{selected_node['name']}**")
                    
                    try:    
                        df_central_node = pd.read_csv(f"data_es/{data_folder}/{sel_op}/{sel_op}_{selected_node['name']}.csv")
                        #
                        df_central_node['Todos los años'] = df_central_node['Todos los años'].apply(lambda x: ast.literal_eval(x))

                        # Extract all lists from 'Todos los años' column
                        all_years_lists = df_central_node['Todos los años'].tolist()
                        
                        # Flatten the lists into a single list
                        flattened_list = [item for sublist in all_years_lists for item in sublist]
                        num_years = len(all_years_lists[0])

                        # Find the maximum value in the flattened list
                        max_value = max(flattened_list)

                        #st.dataframe(df_central_node) 
                        st.dataframe(
                            df_central_node,
                            column_config={
                                f"{'Categorias' if selected_option == 'Tecnológico' else 'Etiqueta de tema dominante'}": "Categorias",
                                "Todos los años": st.column_config.LineChartColumn( # BarChartColumn
                                    f"{'Patentes' if selected_option == 'Tecnológico' else 'Artículos'} ({2024-num_years}-2024)", y_min=0, y_max=max_value, 
                                    width="large",
                                ),
                                
                            },
                            hide_index=True,
                            use_container_width=True,
                        )

                        try:
                            content_filename = f"{sel_op}_link_{selected_node['name']}.csv"
                            contents = read_links(f"data_es/{data_folder}/{sel_op}/{content_filename}")
                            st.download_button(f"{'Descargar Patentes' if selected_option == 'Tecnológico' else 'Descarcar Artículos Top'}", contents, content_filename)
                        except:
                            st.write(f"Sin más detalles por descargar")

                    except: 
                        st.write(f"Sin información disponible de {selected_node['name']} en el eje {selected_option}")
                elif selected_option == "Profesional":
                    st.markdown(f"Topico asociado de Trend Hunter **{selected_node['name']}**")
                    try:
                        file_th = f"data_es/{data_folder}/trend/trend_subnodo-{selected_node['name']}.json"
                        with open(file_th, 'r', encoding='utf-8') as f:
                            d = json.load(f)
                        st.markdown(f"**Resumen:** {d['info']}", unsafe_allow_html=True)
                        st.page_link(d['url'], label="Trend Hunter", icon="🌎")
                    except: 
                        st.write(f"Sin información disponible en el eje {selected_option}")
                else:
                    st.write(f"Sin información disponible en el eje {selected_option}")
        elif selected_node and selected_node['symbolSize']==30:
            with info_container:
                st.write(f"Selecciona algun subnodo para mostrar su información")
        elif selected_node and selected_node['symbolSize']==50:
            with info_container:
                st.write(f"Selecciona algun subnodo para mostrar su información")
        



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
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: calc(100% - 10rem); /* Adjusts the width to avoid the sidebar */
        background-color: #1d285c;
        color: white;
        text-align: center;
        z-index: 100;
        margin-left: 10rem; /* Moves the footer to the right */
    }
    </style>
    <div class='footer'>
        <p>Universidad De La Salle Bajío - Dirección de Investigación y Doctorado &copy; Copyright 2024. <br /> Investigación de futuros: Prospectiva de tendencias científicas y tecnológicas en Guanajuato. Con clave IDEA GTO/SG/386/2023</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

        # Add custom CSS to hide the entire header section
    hide_header = """
        <style>
        header[data-testid="stHeader"] {
            display: none !important;
        }
        </style>
        """

    st.markdown(hide_header, unsafe_allow_html=True)

    # Add custom CSS to hide the "Manage app" button
    hide_manage_app_button = """
        <style>
        button[data-testid="manage-app-button"] {
            display: none !important;
        }
        </style>
        """

    st.markdown(hide_manage_app_button, unsafe_allow_html=True)

    # Add custom CSS to hide the Hosted with stremlit element
    hide_div_element = """
        <style>
        div.viewerBadge_link__qRIco {
            display: none !important;
        }
        </style>
        """

    st.markdown(hide_div_element, unsafe_allow_html=True)
