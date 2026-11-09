# 🧪 Nexus ERP - Sistema de Gestão Industrial & Logística Química

![Python](https://shields.io)
![Flask](https://shields.io)
![MySQL](https://shields.io)
![Bootstrap](https://shields.io)

Um **ERP (Enterprise Resource Planning) Industrial e Logístico** completo e autoral, desenvolvido para simular as operações complexas de uma multinacional de produtos químicos em larga escala. O projeto combina a estrutura robusta de pipeline inspirada em gigantes de mercado como **Salesforce e TOTVS**, envelopada em uma interface exclusiva **Dark Mode com detalhes em Azul Neon (Glow)**.

---

## 🎯 Funcionalidades Principais (Regras de Negócio)

*   **Hierarquia de Permissões Corporativas (RBAC):** Sistema inteligente de restrição de acessos. Funcionários menores (como operadores de vendas) são bloqueados de acessar ou alterar dados sensíveis de outras divisões via barreiras de segurança (Acesso Negado - Erro 403).
*   **Módulo Fiscal Integrado:** Tela com inputs dinâmicos em neon que permitem ao Auditor Fiscal ou Gerente alterar e atualizar manualmente as alíquotas de impostos (ICMS/IPI) em tempo de execução para cada emissão de nota fiscal.
*   **Triagem Logística e Frota:** Vinculação completa da carga do pedido com dados críticos de transporte: nome da transportadora, placa do caminhão, rota de destino, peso bruto da carga, classe de risco químico do composto e status de seguro de carga ativo.
*   **Estoque Real-Time (Baixa Automatizada):** Monitor de silos químicos atualizado instantaneamente. No momento exato em que a logística despacha o caminhão, o sistema deduz automaticamente o volume em toneladas do estoque de insumos no banco de dados.
*   **Painel do Gerente Geral:** Painel macro de indicadores que unifica e exibe a quantidade exata de pendências em tempo real de cada setor (Administrativo, Fiscal e Logística), projetado com atualização automática por hora para monitoramento de casa.

---

## 🏗️ Modelagem Relacional do Banco de Dados (MySQL)

A arquitetura do banco de dados foi modelada localmente seguindo as regras rígidas de integridade referencial através das tabelas:
1.  `produtos`: Gerenciamento e controle de volumetria de silos químicos em toneladas.
2.  `clientes`: Carteira ativa de clientes e representantes comerciais (Estilo CRM).
3.  `pedidos`: Histórico e tracking da fase cadastral de cada ordem de venda.
4.  `notas_fiscais`: Registro fiscal com cálculo dinâmico de impostos manuais.
5.  `logistica_cargas`: Auditoria completa de frota, pesagem e segurança de rota.

---

## 💻 Tecnologias Utilizadas

*   **Backend:** Python 3 + Flask framework (Arquitetura leve de alta performance).
*   **Conector:** `mysql-connector-python` para transações SQL nativas diretas.
*   **Database:** MySQL Workbench (Local) / Estrutura ANSI SQL pronta para deploy na nuvem.
*   **Frontend:** HTML5 estruturado manualmente + CSS3 Custom Dark Neon (Glow Effects) + Bootstrap 5 Icons.

---

## 🚀 Como Executar o Projeto Localmente

1. Certifique-se de ter rodado o script de criação das tabelas no seu **MySQL Workbench**.
2. Altere a linha de conexão (`password`) no arquivo `app.py` com as credenciais do seu banco local.
3. Instale as dependências do projeto no terminal:
   ```bash
   pip install Flask mysql-connector-python
   ```
4. Inicie o servidor do ERP:
   ```bash
   python app.py
   ```
5. Acesse no seu navegador: `http://127.0.0`

---
Projeto desenvolvido como portfólio acadêmico - Segundo Semestre de ADS na **Faculdade Impacta Tecnologia**.
