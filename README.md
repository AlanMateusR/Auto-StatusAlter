# Auto-StatusAlter
## Projeto composto por software de teste automatizado que tem por objetivo automatizar verificações, cruzar dados e atualizar registros de pedidos de vendas em um CRM.

 * **Projeto:** Automatização de tarefas - alteração de Status de pedidos de cliente em CRM 
 * **Arquivos:** AutoStatus.py | CNPJ_IMPLANTAÇÃO.py | get_session.py | credentials.env
 * **Status do projeto:** Entregue

 
 * **Escopo:** Empresa disponibiliza serviços de suporte para integração no escopo de TEF (Transferencia eletronica de fundos) e vende a propria VPN e TLS para este fim. 
 * **Problematica:** Colaboradores do suporte técnico da empresa necessitam diariamente verificar uma lista de clientes no CRM com status do pedido de venda em implantação, feito isso é necessario acessar um portal de relatorios de vendas e cruzar informações afim de saber se os determinados clientes que foram implantados estão ou não vendendo com o produto disponibilizado, se estão vendendo é necessario alterar o status do pedido de venda para FINALIZADO no CRM, se não estiver vendendo deve-se manter o pedido em IMPLANTAÇÃO e seguir com a proxima verificação manual.
 * **Solução:** Script foi elaborado para automatizar todo o procedimento de verificação e alteração de status no CRM com base no resultado do cruzamento de dados, o RPA permanece rodando continuamente em um ambiente reservado da empresa para que inicializa diarimente e remova a necessidade de intervenção manual da equipe de suporte da empresa. Para o projeto foram concedidos acesso ao ambiente Fiserv (Sitef - integração TEF) para verificar relatorio de vendas e ainda as chaves de acesso para integração via API ao portal de CRM Gluo (baseado em Vtiger CRM).

  
 * **Autor:** [Alan Mateus Rodrigues]
 * **Data de Criação:** [10/08/2023]
 * **Empresa:** Tefway Tecnologia LTDA

<br>

 ## !!! Adendo !!!
 * **Este código é disponibilizado no GitHub exclusivamente como parte do portfólio de programação do autor.**
* **O objetivo é demonstrar experiência e habilidades na área de programação.** 
* **Não é recomendada a reprodução, distribuição ou utilização deste código para qualquer finalidade.**

 >* Links, Senhas, Nomes e dados confidenciais foram censurados e a explicação tecnica do funcionamento do codigo foi resumida.
 >* Para mais informações, entre em contato com o autor em: [alanjrelias@hotmail.com]

<br>

# || Resumo do Fluxo de funcionamento do script ||

* **1.** Primeiramente script efetua login no portal Fiserv e exporta uma planilha contendo dados de diversos clientes e seus respectivos dados de venda (quantidade de venda, valores etc) a informação essencial é o valor total de venda efetuados.
* **2.** Da planilha gerada é efetuada uma separação pra obter somente os clientes que venderam um valor diferente de R$ 0,00 para então resultar clientes que já venderam em algum momento (se já tiverem vendido qualquer valor então o produto de integração TEF já foi implantado).
* **3.** Script integra via API com CRM (Gluo) para efetuar requisições GET e registrar pelo menos 20 clientes que estão com pedido de vendas com status igual a "IMPLANTAÇÃO" (serão armazenados em .txt)
* **4.** Será efetuado merge para cruzamento de dados entre clientes que venderam um valor diferente de R$ 0,00 X Cliente com status em implantação, o resultado do cruzamento será a lista de clientes que não devem mais estar em implantação pois ja efetivaram pelo menos uma venda (será gerado outra lista em txt).
* **5.** Uma vez que for obtido a lista de clientes (Identificados com CNPJ) será enviado requisição novamente via API para alterar o status do pedido de venda de todos os cliente da lista para FINALIZADO.

<br>
<br>

- Efetua login ao portal de relatorios e se direciona para area de exportação de relatorios de venda.
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXg3MWJ3dGZiZHUxYmE5NG0zMXR6eXM1MHNoMXRod3NjdDM1dHU0eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Mf0I4DZ9hTIsuGLi1S/giphy.gif" alt="GIF de exemplo" width="700" height="400">

<br>

- Retorna todos os dados de vendas de um range de aproximadamente 7 mill clientes 
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHk2emp5ZXZnem4xZzgwN29oZXR6dHZhbHRlOWp3aTYyM3dsbTIzMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/whM9GIsflmOl5N5LYJ/giphy.gif" alt="GIF de exemplo" width="700" height="400">

<br>

- É selecionado as colunas que estarão presentes na planilha exportada 
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3ppdnB3enc5eWtraWYwM3Z6M3Y1MGZ1OGI2MnNpNmJ6NThhb2F6eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5f0vuxKZvW5DpUHWZz/giphy.gif" alt="GIF de exemplo" width="700" height="400">

<br>
<br>

- Script encerra webdriver, descarta os clientes que não estão vendendo da planilha e logo em seguida faz as requisições para o CRM procurando por clientes com status em IMPLANTAÇÃO
  
![download1](https://imgur.com/ytcrqEy.png)

<br>
<br>

- Codigo procura pela planilha no diretorio Downloads com um prefixo pré-determinado, é utilizado metodo datetime.now para obter ano, mes, dia, hora minuto e segundo atuais e encontrar a planilha, após isso o arquivo é movido para o diretorio onde se encontra o codigo e renomeado para RELATORIO_ESTATISTICA.xlsx

> Será aplicado as devidas condições para retornar outra planilha contendo somente clientes que tenham vendas totais maiores que zero, o resultado será a geração de outro arquivo nomeado RELATORIO_ESTATISTICA_SAIDA.txt

![terminal1](https://imgur.com/ExiOU5L.png)

<br>

- Efetua-se inicialização do codigo CNPJ_IMPLANTAÇÃO.py que efetua integração via API com CRM e busca um range de 20 clientes com pedido de venda em implantação, o resultado é armazenado em Implantações.txt. 
![terminal2](https://imgur.com/94nji3W.png)

<br>

* Codigo cruza os clientes em implantação com clientes que venderam qualquer valor acima de 0,00 
> Foi utilizado separação de dados com dataframe e merge.
> 
> É efetuado cruzamento de datos entre os arquivos Implantaçãos.txt e RELATORIO_ESTATISTICA_SAIDA.txt
> 
> O resultado do cruzamento é armazenado em cnpjs_finalizados.txt cujo status de todos da lista serão alterados.

![mergedf](https://imgur.com/fkcmqK8.png)

<br>

- Por fim, será enviado requisição de alteração de status do pedido para o CRM fazendo com que todos os clientes que já estão vendendo tenham o status alterado para FINALIZADO.
![terminal2](https://imgur.com/yNZr0O5.png)

<br>

> Antes da requisição via API 
![implantação1](https://imgur.com/2lBnsxI.png)

> Depois da requisição via API 
![finalizado](https://imgur.com/czpvFRt.png)
>
![interface](https://imgur.com/5joVT0F.png)



