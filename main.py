import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up the page title and introductory text
st.title('Simulação - Alunos com dívidas > 1440 dias')
st.write("Clique nos botões ao lado para ver a carteira de acordo com o filtro que você deseja.")

# Load the dataframes
tickets = pd.read_csv('C:\\Users\\kevin\\Desktop\\Projects\\Ticket.csv')
campanhas = pd.read_csv('C:\\Users\\kevin\\Desktop\\Projects\\Campanhas.csv')

# Rename columns in campanhas dataframe
campanhas = campanhas.rename(columns={'VALOR_CAMPANHA': 'VALOR CAMPANHA'})

# Rename columns in tickets dataframe
tickets = tickets.rename(columns={'COM JUROS, MULTAS E TAXAS': 'VALOR ATUALIZADO',
                                  ' COM DESCONTO CAMPANHA': 'VALOR CAMPANHA'})

# Create a sidebar with buttons
sidebar_choice = st.sidebar.radio("Escolha uma opção", ("Por tipo de inadimplência e campanhas","Por Ticket"))

# Show content based on sidebar choice
if sidebar_choice == "Por tipo de inadimplência e campanhas":
    # Create a multiselect widget to select specific campanhas vigentes or reset filters
    filter_options = ['Todas as Campanhas'] + list(campanhas['CAMPANHA VIGENTE'].unique())
    selected_campanhas = st.sidebar.multiselect('Selecione a(s) Campanha(s) Vigente(s)', filter_options)
    
    # Filter the campanhas dataframe based on the selected campanhas vigentes
    if 'Todas as Campanhas' in selected_campanhas:
        filtered_campanhas = campanhas
    else:
        filtered_campanhas = campanhas[campanhas['CAMPANHA VIGENTE'].isin(selected_campanhas)]
    
    # Create an input widget for discount percentage
    discount_percentage = st.sidebar.number_input('Desconto (%)', min_value=0, max_value=100, value=0)
    
    # Calculate the simulated values and create the "SIMULAÇÃO" column
    filtered_campanhas['SIMULAÇÃO'] = filtered_campanhas['VALOR ATUALIZADO'] * (1 -(discount_percentage / 100))

    # Create an input widget for forecast of results
    results_preview = st.sidebar.number_input('Previsão de Retorno', min_value=0, max_value=100, value=0)

    # Calculate the simulated values and create the "PREVISÃO" column
    filtered_campanhas['PREVISÃO'] = filtered_campanhas['SIMULAÇÃO'] * (results_preview / 100)
    
    # Create a new DataFrame for the bubble graph
    campanhas_grafico = filtered_campanhas.drop(columns=['TIPO_INADIMPLENCIA']).groupby('CAMPANHA VIGENTE').sum().reset_index()
    campanhas_grafico['% DO DESCONTO'] = (1 - (campanhas_grafico['VALOR CAMPANHA'] / campanhas_grafico['VALOR ATUALIZADO'])) * 100
    
    # Display the filtered campanhas dataframe
    st.write(filtered_campanhas)

    # # Calculate totals for VALOR ATUALIZADO, VALOR_CAMPANHA, and SIMULAÇÃO
    total_valor_atualizado = campanhas_grafico['VALOR ATUALIZADO'].sum()
    total_valor_campanha = campanhas_grafico['VALOR CAMPANHA'].sum()
    total_valor_simulacao = campanhas_grafico['SIMULAÇÃO'].sum()
    total_valor_previsao = campanhas_grafico['PREVISÃO'].sum()
    
    # Display the total values in a vertical layout
    st.write("Totais:")
    with st.container():
        st.metric("Total VALOR ATUALIZADO", f"R$ {total_valor_atualizado:,.2f}")
        st.metric("Total VALOR CAMPANHA", f"R$ {total_valor_campanha:,.2f}")
        st.metric("Total SIMULAÇÃO", f"R$ {total_valor_simulacao:,.2f}")
        st.metric("Total PREVISÃO", f"R$ {total_valor_previsao:,.2f}")


    # Create a bubble graph using Plotly
    fig = px.scatter(campanhas_grafico, x='VALOR CAMPANHA', y='% DO DESCONTO', size='Cont. CPFs', color='CAMPANHA VIGENTE', size_max=100,
                     title="Valor da Campanha por % do Desconto e Qtd de Alunos (tamanho da bolha)")
    st.plotly_chart(fig)

     # Create a grouped bar chart for VALOR ATUALIZADO, VALOR_CAMPANHA, and SIMULAÇÃO
    campanha_vigente = campanhas_grafico['CAMPANHA VIGENTE']
    valor_atualizado = campanhas_grafico['VALOR ATUALIZADO']
    valor_campanha = campanhas_grafico['VALOR CAMPANHA']
    valor_simulação = campanhas_grafico['SIMULAÇÃO']

    grouped_bar_fig = go.Figure(data=[
    		go.Bar(name='VALOR ATUALIZADO', x=campanha_vigente, y=valor_atualizado),
    		go.Bar(name='VALOR CAMPANHA', x=campanha_vigente, y=valor_campanha),
    		go.Bar(name='VALOR SIMULAÇÃO', x=campanha_vigente, y=valor_simulação)
    	])
    grouped_bar_fig.update_layout(barmode='group')
    st.plotly_chart(grouped_bar_fig)  

elif sidebar_choice == "Por Ticket":
      # Create a multiselect widget to select specific tickets or reset filters
    filter_options = ['Todos os Tickets'] + list(tickets['Ticket'].unique())
    selected_tickets = st.sidebar.multiselect('Selecione o(s) Ticket(s)', filter_options)
    
    # Filter the tickets dataframe based on the selected tickets
    if 'Todos os Tickets' in selected_tickets:
        filtered_tickets = tickets
    else:
        filtered_tickets = tickets[tickets['Ticket'].isin(selected_tickets)]
    
    # Create an input widget for discount percentage
    discount_percentage = st.sidebar.number_input('Desconto (%)', min_value=0, max_value=100, value=0)
    
    # Calculate the simulated values and create the "SIMULAÇÃO" column
    filtered_tickets['SIMULAÇÃO'] = filtered_tickets['VALOR ATUALIZADO'] * (1 - (discount_percentage / 100))

    # Create an input widget for forecast of results
    tickets_preview = st.sidebar.number_input('Previsão de Retorno', min_value=0, max_value=100, value=0)

    # Calculate the simulated values and create the "PREVISÃO" column
    filtered_tickets['PREVISÃO'] = filtered_tickets['SIMULAÇÃO'] * (tickets_preview / 100)
    
    # Display the filtered tickets dataframe
    st.write(filtered_tickets)

     # # Calculate totals for VALOR ATUALIZADO, VALOR_CAMPANHA, and SIMULAÇÃO
    tickets_atualizado = filtered_tickets['VALOR ATUALIZADO'].sum()
    tickets_campanha = filtered_tickets['VALOR CAMPANHA'].sum()
    tickets_simulacao = filtered_tickets['SIMULAÇÃO'].sum()
    tickets_previsao = filtered_tickets['PREVISÃO'].sum()
    
    # Display the total values in a vertical layout
    st.write("Totais:")
    with st.container():
        st.metric("Total VALOR ATUALIZADO", f"R$ {tickets_atualizado:,.2f}")
        st.metric("Total VALOR CAMPANHA", f"R$ {tickets_campanha:,.2f}")
        st.metric("Total SIMULAÇÃO", f"R$ {tickets_simulacao:,.2f}")
        st.metric("Total PREVISÃO", f"R$ {tickets_previsao:,.2f}")

    # Create a bubble graph using Plotly
    ticket_fig = px.scatter(filtered_tickets, x='VALOR ATUALIZADO', y='Ticket', size='Cont. CPFs', size_max=100,
                     title="Valor de dívida por Ticket")
    st.plotly_chart(ticket_fig)

     # Create a horizontal bar chart for VALOR ATUALIZADO, VALOR CAMPANHA, and SIMULAÇÃO
    ticket_medio = filtered_tickets['Ticket']
    ticket_atualizado = filtered_tickets['VALOR ATUALIZADO']
    ticket_campanha = filtered_tickets['VALOR CAMPANHA']
    ticket_simulação = filtered_tickets['SIMULAÇÃO']

    ticket_bar_fig = go.Figure(data=[
    		go.Bar(name='VALOR ATUALIZADO', y=ticket_medio, x=ticket_atualizado, orientation='h'),
    		go.Bar(name='VALOR CAMPANHA', y=ticket_medio, x=ticket_campanha, orientation='h'),
    		go.Bar(name='VALOR SIMULAÇÃO', y=ticket_medio, x=ticket_simulação, orientation='h')
    	])
    ticket_bar_fig.update_layout(barmode='group')
    st.plotly_chart(ticket_bar_fig)  



