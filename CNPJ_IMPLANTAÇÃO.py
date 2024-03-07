def implantacao():
    import get_session
    from html.parser import HTMLParser
    import http.client
    import json
    import os
    from dotenv import load_dotenv, dotenv_values

    ## Foi utilizado metodo de resgate de variaveis .ENV ##
    ## Os dados contidos no credentials.env.example são ficticios ##

    ## >>> Não tente replicar o codigo ou utiliza-lo para qualquer fim <<<

    """ OBTER VARIAVEIS NECESSARIAS """
    # Resgatando variaveis .ENV   
    load_dotenv()

    # Link para requisição portal Gluo
    linkGluo = os.getenv("link_crm")

    print("Iniciando busca...")

    # Iniciando sessao API para obter "session"
    # session é o pametro chave para todas as requisições no portal Gluo Crm

    import get_session
    get_session.get_session()

    with open("session.txt", "r", encoding="utf-8") as arquivo:
            cnpjs = arquivo.readlines()
            for i, linha in enumerate(cnpjs):
                if i == 0:
                    session = linha


    # contados de looping
    num = 0

    # contador de linha - resultado do parametro
    i = 0

    while num <= 20:
        # quety_campos
        # retorna: account_id e PDV_NO (parametro para requisição via API)

        conn = http.client.HTTPSConnection(linkGluo)
        payload = ''
        headers = {}
        conn.request("GET", f"/webservice.php?sessionName={session}&operation=query&query=SELECT%20sostatus,account_id,salesorder_no%20FROM%20SalesOrder%20WHERE%20produto_pdv%20LIKE%20'Sitef%20Nuvem%25'%20AND%20sostatus%20=%20'Implanta%C3%A7%C3%A3o';", payload, headers)
        res = conn.getresponse()
        data = res.read()

        #print(data.decode("utf-8"))

        # conta id -
        data_dict_1 = json.loads(data)
        conta_id = (data_dict_1["result"][i]["account_id"])
        # print(f"account_id: {conta_id}")

        # pdvno
        data_dict_2 = json.loads(data)
        pdvno = (data_dict_1["result"][i]["salesorder_no"])
        # print(f"salesorder_no: {pdvno}")
        # print()

        # utilizar dado obtido 'account_id' para retornar 'cnpj'
        conn = http.client.HTTPSConnection(linkGluo)
        payload = ''
        headers = {}
        conn.request("GET", f"/webservice.php?sessionName={session}&id={conta_id}&operation=retrieve",
                        payload, headers)
        res = conn.getresponse()
        data = res.read()

        data_dict_1 = json.loads(data)
        cnpj = (data_dict_1["result"]["cpfcnpj"])
        # print(f"account_id: {cnpj}")

        print(f"Pedido Implantação: {cnpj}")
        print()

        with open("Implantações.txt", "a", encoding="utf-8") as arquivo:
            frases = list()
            frases.append(f"{cnpj}\n")
            arquivo.writelines(frases)
        
        num += 1
        i += 1

    print("Finalizado...")