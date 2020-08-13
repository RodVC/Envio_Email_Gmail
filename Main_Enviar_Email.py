# pip install pysimplegui
#import PySimpleGUI
#PySimpleGUI.main()
import PySimpleGUI as sg
import os
import time
import sys
from class_email import Emailer

class aplicacao_email:

    def email_sem_anexo(self,email_remetente,senha,assunto,lista_destinatarios,conteudo_email):
        mail = Emailer(email_remetente,senha)
        mail.definir_conteudo_email(assunto,lista_destinatarios,conteudo_email)
        # mail.anexar_imagens(lista_imagens)
        # mail.anexar_arquivos_variados(lista_arquivos)
        mail.enviar_email_gmail(2)
    
    def email_anexo_imagem(self,email_remetente,senha,assunto,lista_destinatarios,conteudo_email,lista_imagens,caminho_imagem):
        mail = Emailer(email_remetente,senha)
        mail.definir_conteudo_email(assunto,lista_destinatarios,conteudo_email)
        mail.anexar_imagens(lista_imagens,caminho_imagem)
        # mail.anexar_arquivos_variados(lista_arquivos)
        mail.enviar_email_gmail(2)

    def email_anexo_variados(self,email_remetente,senha,assunto,lista_destinatarios,conteudo_email,lista_arquivos,caminho_arquivo):
        mail = Emailer(email_remetente,senha)
        mail.definir_conteudo_email(assunto,lista_destinatarios,conteudo_email)
        # mail.anexar_imagens(lista_imagens,caminho_imagem)
        mail.anexar_arquivos_variados(lista_arquivos,caminho_arquivo)
        mail.enviar_email_gmail(2)

    def criar_interface(self):
        # TEMA
        sg.theme('BlueMono')

        # LAYOUT DADOS DE EMAIL
        layout_dados_email = [
            
            [sg.Text('De:        '),sg.Input(key='input_de'),sg.Text('Senha do E-mail'),sg.Input(key='input_senha',password_char='*',size=(15,1))],
            [sg.Text('Para:     '),sg.Input(key='input_para',size=(78,1))],
            [sg.Text('Assunto:'),sg.Input(key='input_assunto',size=(78,1))],
            [sg.Text('Anexo:   '),sg.Input(key='input_anexo',size=(35,1)),sg.FilesBrowse('Selecionar Anexo'),sg.Radio('Imagem',key='rd_imagem',group_id='rd_anexos'),sg.Radio('Outros Docs',key='rd_outros_docs',default=True ,group_id='rd_anexos')]
            # [sg.Button('Iniciar'),sg.Button('Parar')]
        ]

        # LAYOUT MENSAGEM
        layout_mensagem = [

            [sg.Multiline(autoscroll=True,size=(86,10),key='mtl_email')]

        ]

        # LAYOUT PRINCIPAL
        layout = [

            [sg.Frame('Dados do E-mail # GMAIL #',layout_dados_email)],
            [sg.Frame('Mensagem',layout_mensagem)],
            [sg.Button('Enviar Mensagem',key='btn_enviar')]

        ]
        return sg.Window('Envio de E-mail',layout)

    def inciar_programa(self):
        # JANELA
        janela = self.criar_interface()
        
        # LEITURA DOS VALORES
        while True:
            evento, valores = janela.read() 

            #com esse código dá pra extrair o caminho em formato python e o nome do arquivo
            if evento == 'btn_enviar':
                caminho = valores['input_anexo']
                caminho_formato_python = caminho.translate({ord(c): "//" for c in "//"})
                posicao = caminho_formato_python.rfind('//')    
                nome_arquivo = caminho_formato_python[posicao+2:]  
                # janela['input_anexo'].update(nome_arquivo)    
                caminho_pasta = caminho_formato_python[0:posicao]
                
                #enviar email sem anexo
                if valores['input_anexo'] == '':
                    # o argumento de destinatário tem que ser passado no formato de lista
                    self.email_sem_anexo(valores['input_de'],valores['input_senha'],valores['input_assunto'],[valores['input_para']],valores['mtl_email'])
                    sg.Popup('Mensagem Enviada')

                #enviar email com anexo de imagem
                if valores['input_anexo'] != '' and valores['rd_imagem'] == True:
                    if  nome_arquivo[nome_arquivo.rindex('.') + 1:] not in('jpg','png','gif','bmp','jpeg'):
                        sg.Popup('Tipo de Anexo incorreto. Selecione o tipo de anexo ao lado.')
                    else:
                        # o argumento de destinatário tem que ser passado no formato de lista
                        self.email_anexo_imagem(valores['input_de'],valores['input_senha'],valores['input_assunto'],[valores['input_para']],valores['mtl_email'],nome_arquivo,caminho_pasta)
                        sg.Popup('Mensagem Enviada')
                
                #enviar email com anexo variado
                if valores['input_anexo'] != '' and valores['rd_outros_docs'] == True:
                    if  nome_arquivo[nome_arquivo.rindex('.') + 1:] in('jpg','png','gif','bmp','jpeg'):
                        sg.Popup('Tipo de Anexo incorreto. Selecione o tipo de anexo ao lado.')
                    else:
                        # o argumento de destinatário tem que ser passado no formato de lista
                        self.email_anexo_variados(valores['input_de'],valores['input_senha'],valores['input_assunto'],[valores['input_para']],valores['mtl_email'],nome_arquivo,caminho_pasta)
                        sg.Popup('Mensagem Enviada')


        
            if evento in (sg.WIN_CLOSED,'Exit'):
                break

        janela.close()
        sys.exit()

start = aplicacao_email()
start.inciar_programa()
