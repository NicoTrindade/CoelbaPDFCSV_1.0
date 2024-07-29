# import streamlit as st

# st.set_page_config(page_title="COELBA - PDF >> CSV")

# st.subheader("Conversão automática. Possível exportar o CSV para Excel.")
from PyPDF2 import PdfReader
import streamlit as st
import base64
import csv
# import os.path
# from pathlib import Path
from funcoes import DadosRetornoCSV

# PASTA_RAIZ = os.getcwd() 

def gerarCSV2022(NomeArquivoPDF):         

      RELATORIO_COELBA = NomeArquivoPDF               

      arquivoCSV = RELATORIO_COELBA.replace(".pdf","") + '.csv'

      CAMINHO_CSV = arquivoCSV 

      reader = PdfReader(NomeArquivoPDF) 
      page = reader.pages
      
      lista_cabecalho = ['Dados do cliente', 
                     'Endereço da Unidade Consumidora', 
                     'Número da Nota Fiscal', 
                     'N da Instalação', 
                     'Classificação', 
                     'Descrição da Nota Fiscal', 
                     'Tarifas Aplicadas', 
                     'ICMS Base de Cálculo', 
                     'ICMS Base 2', 
                     'ICMS Base 3', 
                     'ICMS Base 4', 
                     'ICMS Base 5', 
                     'ICMS Base 6', 
                     'ICMS Base 7', 
                     'ICMS Base 8', 
                     'ICMS Base 9', 
                     'Número do medidor', 
                     'Conta Contrato', 
                     'Mês Ano', 
                     'Total a pagar']

      with open(CAMINHO_CSV, 'w', newline='') as csvfile:   
         csv.DictWriter(csvfile, fieldnames=lista_cabecalho, quoting=csv.QUOTE_ALL, delimiter=',').writeheader()
         
         for page in reader.pages:                
                     
            if page.extract_text().find('DOCUMENTO PARA PAGAMENTO DA CONTA COLETIVA') == -1:
      
               TEXTO_COMPLETO = page.extract_text()            
               
               # Dados do cliente
               lista_dados_cliente = DadosRetornoCSV(len('DADOS DO CLIENTE'), page.extract_text().find('DADOS DO CLIENTE'), page.extract_text().find('DATA DE VENCIMENTO'), TEXTO_COMPLETO)            

               # Endereço Unidade Consumidora
               lista_end_unid_consum = DadosRetornoCSV(len('ENDEREÇO DA UNIDADE CONSUMIDORA'), page.extract_text().find('ENDEREÇO DA UNIDADE CONSUMIDORA'), page.extract_text().find('RESERVADO AO FISCO'), TEXTO_COMPLETO)                      

               # Número da Nota Fiscal
               lista_num_nota_fiscal = DadosRetornoCSV(len('NÚMERO DA NOTA FISCAL'), page.extract_text().find('NÚMERO DA NOTA FISCAL'), page.extract_text().find('CONTA CONTRATO'), TEXTO_COMPLETO)          
            
               # Nº da Instlação
               lista_num_Instalacao = DadosRetornoCSV(len('Nº DA INSTALAÇÃO'), page.extract_text().find('Nº DA INSTALAÇÃO'), page.extract_text().find('CLASSIFICAÇÃO'), TEXTO_COMPLETO)                      
               
               # Classificação
               lista_classificacao = DadosRetornoCSV(len('CLASSIFICAÇÃO'), page.extract_text().find('CLASSIFICAÇÃO'), page.extract_text().find('ENDEREÇO DA UNIDADE CONSUMIDORA'), TEXTO_COMPLETO)          

               # Descrição da Nota Fiscal
               lista_desc_nota_fiscal = DadosRetornoCSV(0, 0, page.extract_text().find('DESCRIÇÃO DA NOTA FISCAL'), TEXTO_COMPLETO)
               lista_desc_nota_fiscal_tratado = " ".join(lista_desc_nota_fiscal.split())

               # Tarifas Aplicadas
               if page.extract_text().find('DATA PREVISTA DA PRÓXIMA LEITURA:') > 0:
                  lista_tarifas_aplicadas_tratada = DadosRetornoCSV(len('DATA PREVISTA DA PRÓXIMA LEITURA:')+11, page.extract_text().find('DATA PREVISTA DA PRÓXIMA LEITURA:'), page.extract_text().find('Tarifas Aplicadas'), TEXTO_COMPLETO)          
               else:
                  lista_tarifas_aplicadas = DadosRetornoCSV(len('AJUSTECONSUMO'), page.extract_text().find('AJUSTECONSUMO'), page.extract_text().find('Tarifas Aplicadas'), TEXTO_COMPLETO)          
                  lista_tarifas_aplicadas_tratada = lista_tarifas_aplicadas.replace('(kWh)','').strip()

               # Informações de Tributos
               lista_inform_tributos = DadosRetornoCSV(len('INFORMAÇÕES DE TRIBUTOS'), page.extract_text().find('INFORMAÇÕES DE TRIBUTOS'), page.extract_text().find('AUTENTICAÇÃO MECÂNICA'), TEXTO_COMPLETO)          
               lista_inform_tributos_tratado = " ".join(lista_inform_tributos.split()) # Retrar os espaços entre as palavras      
               lista_inform_tributos_list = lista_inform_tributos_tratado.split(" ") # Converter em lista
               if len(lista_inform_tributos_list) > 8: # Definir se existe o ICMS Base de Cálculo 
                  lista_inform_tributos_list.insert(0,lista_inform_tributos_list[0]) 
               else:
                  lista_inform_tributos_list.insert(0,' ')     

               # Número do Medidor
               if page.extract_text().find('CAT') > 0 and page.extract_text().find('AJUSTECONSUMO') > 0:
                  lista_num_medidor = DadosRetornoCSV(len('AJUSTECONSUMO'), page.extract_text().find('AJUSTECONSUMO'), page.extract_text().find('CAT'), TEXTO_COMPLETO)
                  lista_num_medidor_tratado = lista_num_medidor.replace('(kWh)','').strip()
               else:
                  lista_num_medidor_tratado = ""

               # Conta Contrato
               lista_conta_contato = DadosRetornoCSV(len('CONTA CONTRATO'), page.extract_text().find('CONTA CONTRATO'), page.extract_text().find('Nº DO CLIENTE'), TEXTO_COMPLETO)
         
               # Mês Ano
               lista_mes_ano = DadosRetornoCSV(len('MÊS/ANO'), page.extract_text().find('MÊS/ANO'), page.extract_text().find('TOTAL A PAGAR(R$)')+1, TEXTO_COMPLETO) 
               
               # Total a pagar
               lista_total_pagar = DadosRetornoCSV(len('TOTAL A PAGAR (R$)'), page.extract_text().find('TOTAL A PAGAR (R$)'), page.extract_text().find('DATA DA EMISSÃO DA NOTA FISCAL'), TEXTO_COMPLETO)                      
               
               csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',').writerow([lista_dados_cliente, 
                                                                                 lista_end_unid_consum, 
                                                                                 lista_num_nota_fiscal, 
                                                                                 lista_num_Instalacao, 
                                                                                 lista_classificacao, 
                                                                                 lista_desc_nota_fiscal_tratado, 
                                                                                 lista_tarifas_aplicadas_tratada, 
                                                                                 lista_inform_tributos_list[0], 
                                                                                 lista_inform_tributos_list[1],
                                                                                 lista_inform_tributos_list[2],
                                                                                 lista_inform_tributos_list[3],
                                                                                 lista_inform_tributos_list[4],
                                                                                 lista_inform_tributos_list[5],
                                                                                 lista_inform_tributos_list[6],
                                                                                 lista_inform_tributos_list[7],
                                                                                 lista_inform_tributos_list[8],
                                                                                 lista_num_medidor_tratado,
                                                                                 lista_conta_contato,
                                                                                 lista_mes_ano,
                                                                                 lista_total_pagar])                   
                 
      with open(CAMINHO_CSV) as f:
        st.download_button('Download CSV Ano 2022', f, file_name=CAMINHO_CSV)
    
col1, col2, col3, col4, col5, col6, col7, col7, col9, col10, col11, col12, col13, col14, col15 = st.columns(15)

with col1:    
    with st.sidebar:    
        uploaded_file = st.file_uploader("Escolha um PDF Ano 2022")      
        if uploaded_file is not None:
            with col2:            
                pdf_data = open(uploaded_file.name, "rb").read()

                b64 = base64.b64encode(pdf_data).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" align="left" width="800" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            gerarCSV2022(uploaded_file.name)        

# with col3:
#    st.markdown("              ", unsafe_allow_html=True)
    # with st.sidebar:  
    #     uploaded_file = st.file_uploader("Escolha um PDF Ano 2024")
    #     if uploaded_file is not None:
            
    #         pdf_data = open(uploaded_file.name, "rb").read()

    #         b64 = base64.b64encode(pdf_data).decode("utf-8")
    #         pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="1000" type="application/pdf"></iframe>'
    #         st.markdown(pdf_display, unsafe_allow_html=True)

    #         gerarCSV2022(uploaded_file.name)        
