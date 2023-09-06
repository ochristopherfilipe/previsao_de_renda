import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import statsmodels.api as sm
import statsmodels.formula.api as smf

sns.set(context='talk', style='ticks')

st.set_page_config(
     page_title="Previsão de renda",
     page_icon="💰",
     layout="wide",
)

# tabs configuration

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home" 
                                        ,"Gráficos alteráveis" 
                                        ,"Univariadas" 
                                        ,"Bivariadas"
                                        ,"Dados brutos"]
                                        )

with tab1:
     # abrindo o arquivo
    df = pd.read_csv('previsao_de_renda.csv')
     # definindo uma mascara para outliers
    mascara = (df['renda'] <= 20000) & (df['renda'] >= 500)
    df = df[mascara]
     # rodando o modelo statsmodel
    reg = smf.ols('renda ~ sexo + posse_de_veiculo + posse_de_imovel + qtd_filhos + educacao + estado_civil + tipo_residencia + idade + tempo_emprego + qt_pessoas_residencia ''', data = df).fit()

    def predict_income(sexo, posse_de_veiculo, posse_de_imovel, qtd_filhos, educacao, estado_civil, tipo_residencia, idade, tempo_emprego, qt_pessoas_residencia):
        input_data = {
            'sexo': sexo,
            'posse_de_veiculo': posse_de_veiculo,
            'posse_de_imovel': posse_de_imovel,
            'qtd_filhos': qtd_filhos,
            'educacao': educacao,
            'estado_civil': estado_civil,
            'tipo_residencia': tipo_residencia,
            'idade': idade,
            'tempo_emprego': tempo_emprego,
            'qt_pessoas_residencia': qt_pessoas_residencia
        }

        # Crie um DataFrame a partir dos dados de entrada
        input_df = pd.DataFrame([input_data])

        # Faça a previsão usando seu modelo
        prediction = reg.predict(input_df)

        return prediction[0]

    # Interface do aplicativo usando Streamlit
        
    st.title('Análise exploratória da :green[Previsão de Renda]')
    st.markdown('#### Nas abas aqui dispostas, você encontrá informações referentes aos estudos de previsão de renda')
    st.markdown("##### O objetivo desta análise é prever a variação de renda dos clientes de uma instituição financeira. Os dados utilizados na análise e previsão foram coletados e distribuidos em variáveis com características diversas que auxiliam na previsão ou explicação da renda de um cliente.")
    st.markdown("---")

    st.markdown("\n" * 5)

    st.title(":red[Aplicativo] de Predição de Renda")

    # Widgets para inserção de valores
    sexo = st.radio("Sexo", ("M", "F"))
    posse_de_veiculo = st.checkbox("Possui Veículo?")
    posse_de_imovel = st.checkbox("Possui Imóvel?")
    qtd_filhos = st.slider("Quantidade de Filhos", min_value=0, max_value=14, value=0)
    educacao = st.selectbox("Educação", ("Secundário", "Superior completo", "Superior incompleto", "Primário", "Pós Graduação"))
    estado_civil = st.selectbox("Estado Civil", ("Solteiro", "Casado", "Separado", "União", "Viúvo"))
    tipo_residencia = st.selectbox("Tipo de Residência", ("Casa", "Com os pais", "Aluguel", "Estúdio", "Governamental", "Comunitário"))
    idade = st.slider("Idade", min_value=18, max_value=100, value=30)
    tempo_emprego = st.slider("Tempo de Emprego", min_value=0, max_value=42, value=10)
    qt_pessoas_residencia = st.slider("Quantidade de adultos na Residência", min_value=1, max_value=15, value=2)

    # Botão para fazer a predição
    if st.button("Prever"):
        # Transformar valores de entrada em formato apropriado
        posse_de_veiculo = True if posse_de_veiculo else False
        posse_de_imovel = True if posse_de_imovel else False
        
        # Fazer a previsão usando a função
        prediction = predict_income(sexo, posse_de_veiculo, posse_de_imovel, qtd_filhos, educacao, estado_civil, tipo_residencia, idade, tempo_emprego, qt_pessoas_residencia)

        # Formatando para resultado em português
        formatted_prediction = f"R$ {prediction:.2f}"

        # Mostrando resultado
        st.write(f"A previsão de renda é: {formatted_prediction}")
    

with tab2:
    

    #Gráfico customizável univariadas

    st.write('# Gráfico customizável para análises univariadas')
    option1 = st.selectbox(
        'Selecione a variável que deseja exibir',
        ('sexo', 'posse_de_veiculo', 'posse_de_imovel', 
         'qtd_filhos', 'tipo_renda', 'educacao', 
         'estado_civil', 'tipo_residencia', 'idade', 
         'tempo_emprego', 'qt_pessoas_residencia')
        )
    
    fig = plt.figure(figsize=(6, 4))
    sns.lineplot(x='data_ref',y='renda', hue= option1 ,data=df)
    plt.xlabel(option1)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    #Gráfico customizável bivariadas
    
    st.divider()

    options = st.multiselect(
        'Selecione até duas variáveis que deseja cruzar',
        ['renda','sexo', 'posse_de_veiculo', 'posse_de_imovel', 
        'qtd_filhos', 'tipo_renda', 'educacao', 
        'estado_civil', 'tipo_residencia', 'idade', 
        'tempo_emprego', 'qt_pessoas_residencia'],
        ['educacao', 'renda']
        )
    
    st.write('# Gráfico customizável para análises bivariadas')
    fig = plt.figure(figsize=(6, 4))
    sns.barplot(x=options[0],y=options[1],data=df)
    plt.xticks(rotation=30)
    st.pyplot(plt)

with tab3:

        #plots
        
    st.write('# Gráficos ao longo do tempo')
    st.divider()

    # Criar subplots
    fig, ax = plt.subplots(6, 1, figsize=(10, 40), sharex=True, gridspec_kw={'hspace': 0.5})

    # Gráfico 1
    sns.lineplot(x='data_ref', y='renda', hue='posse_de_imovel', data=df, ax=ax[0])
    ax[0].tick_params(axis='x', rotation=45)
    ax[0].set_title('Gráfico 1 - Renda vs. Posse de Imóvel')

    # Gráfico 2
    sns.lineplot(x='data_ref', y='renda', hue='posse_de_veiculo', data=df, ax=ax[1])
    ax[1].tick_params(axis='x', rotation=45)
    ax[1].set_title('Gráfico 2 - Renda vs. Posse de Veículo')

    # Gráfico 3
    sns.lineplot(x='data_ref', y='renda', hue='qtd_filhos', data=df, ax=ax[2])
    ax[2].tick_params(axis='x', rotation=45)
    ax[2].set_title('Gráfico 3 - Renda vs. Quantidade de Filhos')

    # Gráfico 4
    sns.lineplot(x='data_ref', y='renda', hue='tipo_renda', data=df, ax=ax[3])
    ax[3].tick_params(axis='x', rotation=45)
    ax[3].set_title('Gráfico 4 - Renda vs. Tipo de Renda')

    # Gráfico 5
    sns.lineplot(x='data_ref', y='renda', hue='educacao', data=df, ax=ax[4])
    ax[4].tick_params(axis='x', rotation=45)
    ax[4].set_title('Gráfico 5 - Renda vs. Educação')

    # Gráfico 6
    sns.lineplot(x='data_ref', y='renda', hue='estado_civil', data=df, ax=ax[5])
    ax[5].tick_params(axis='x', rotation=45)
    ax[5].set_title('Gráfico 6 - Renda vs. Estado Civil')

    # Remover margens desnecessárias
    sns.despine()

    # Exibir os gráficos no Streamlit
    st.pyplot(fig)
     
with tab4:   

    st.write('# Gráficos das análises bivariadas')
    st.divider()
    fig, ax = plt.subplots(7,1,figsize=(10,40))
    sns.barplot(x='posse_de_imovel',y='renda',data=df, ax=ax[0])
    sns.barplot(x='posse_de_veiculo',y='renda',data=df, ax=ax[1])
    sns.barplot(x='qtd_filhos',y='renda',data=df, ax=ax[2])
    sns.barplot(x='tipo_renda',y='renda',data=df, ax=ax[3])
    sns.barplot(x='educacao',y='renda',data=df, ax=ax[4])
    ax[4].tick_params(axis='x', rotation=20)
    sns.barplot(x='estado_civil',y='renda',data=df, ax=ax[5])
    sns.barplot(x='tipo_residencia',y='renda',data=df, ax=ax[6])
    ax[6].tick_params(axis='x', rotation=30)
    sns.despine()
    st.pyplot(plt)

with tab5:
    st.markdown("<h1 style='text-align: center; '>Dicionário de dados</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        | Variável                | Descrição                                           | Tipo         |
        | ----------------------- |:---------------------------------------------------:| ------------:|
        | data_ref                |  Data de referência da coleta do dado               | texto|
        | id_cliente              |  Número de identificação do cliente                 | inteiro|
        | sexo                    |  M = 'Masculino'; F = 'Feminino'                    | inteiro|
        | posse_de_veiculo        |  True = 'possui'; False = 'não possui'              | booleana|
        | posse_de_imovel         |  True = 'possui'; False = 'não possui'              | booleana|
        | qtd_filhos              |  Quantidade de filhos do cliente                    | inteiro|
        | tipo_renda              |  Tipo de renda (ex: assaliariado, autônomo etc)     | texto|
        | educacao                |  Nível educacional (ex: secundário, superior etc)   | texto|
        | estado_civil            |  Estado civil (ex: solteiro, casado etc)            | texto|
        | tipo_residencia         |  Tipo de residência (ex: casa/apartamento, com os pais etc)| texto|
        | idade                   |  Idade em anos                                      | inteiro|
        | tempo_emprego           |  Tempo de emprego em anos                           | float|
        | qt_pessoas_residencia   |  Quantidade de pessoas na residência                | float|
        | renda                   |  Valor da renda mensal                              | float|
    """
    )
    st.divider()
    st.markdown("<h1 style='text-align: center; '>Base de dados</h1>", unsafe_allow_html=True)
    st.write(df)

