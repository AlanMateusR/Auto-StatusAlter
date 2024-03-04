# Auto-StatusAlter
Projeto composto por software de teste automatizado que tem por objetivo automatizar verificações, cruzar dados e atualizar registros de pedidos de vendas em um CRM.


 * Projeto: Automatização de tarefas - alteração de Status de pedidos de cliente em CRM 
 * Arquivos: AutoStatus.py | CNPJ_IMPLANTAÇÃO.py | get_session.py | credentials.env
 * Status do projeto: Entregue
 
 * Escopo: Empresa disponibiliza serviços de suporte para integração no escopo de TEF (Transferencia eletronica de fundos) e vende a propria VPN e TLS para este fim. 
 * Problematica: Colaboradores do suporte técnico da empresa necessitam diariamente verificar uma lista de clientes no CRM com status do pedido de venda em implantação, feito isso é necessario acessar um portal de relatorios de vendas e cruzar informações afim de saber se os determinados clientes que foram implantados estão ou não vendendo com o produto disponibilizado, se estão vendendo é necessario alterar o status do pedido de venda para FINALIZADO no CRM, se não estiver vendendo deve-se manter o pedido em IMPLANTAÇÃO e seguir com a proxima verificação manual.
 * Descrição: Script foi elaborado para automatizar todo o procedimento de verificação e alteração de status no CRM com base no resultado do cruzamento de dados, o RPA permanece rodando continuamente em um ambiente reservado da empresa para que inicialize diarimente e remova a necessidade de intervenção manual da equipe de suporte da empresa. Para o projeto foram concedidos acesso ao ambiente Fiserv para verificar relatorio de vendas e ainda as chaves de acesso para integração via API ao   portal GLUO.
  
 * Autor: [Alan Mateus Rodrigues]
 * Data de Criação: [10/08/2023]
 * Empresa: Tefway Tecnologia LTDA
 
 * Este código é disponibilizado no GitHub exclusivamente como parte do portfólio de programação do autor. 
 * O objetivo é demonstrar experiência e habilidades na área de programação. 
 * Não é recomendada a reprodução, distribuição ou utilização 
 * deste código para qualquer finalidade.
  
 * Para mais informações, entre em contato com o autor em:
 * [alanjrelias@hotmail.com]
 *************************************************************/

|| Resumo do Fluxo de funcionamento do script ||

1. Primeiramente script efetua login no portal Fiserv e exporta uma planilha contendo dados de diversos clientes e seus respectivos dados de venda (quantidade de venda, valores etc) a informação essencial é o valor total de venda efetuados.
2. Da planilha gerada é efetuada uma separação pra obter somente os clientes que venderam um valor diferente de R$ 0,00 para então resultar clientes que já venderam em algum momento (se já tiverem vendido qualquer valor então o produto de integração TEF já foi implantado).
3. Script integra via API com CRM (Gluo) para efetuar requisições GET e registrar pelo menos 20 clientes que estão com pedido de vendas com status igual a "IMPLANTAÇÃO" (serão armazenados em .txt)
4. Será efetuado merge para cruzamento de dados entre clientes que venderam um valor diferente de R$ 0,00 X Cliente com status em implantação, o resultado do cruzamento será a lista de clientes que não devem mais estar em implantação pois ja efetivaram pelo menos uma venda (será gerado outra lista em txt).
5. Uma vez que for obtido a lista de clientes (Identificados com CNPJ) será enviado requisição novamente via API para alterar o status do pedido de venda de todos os cliente da lista para FINALIZADO. 
