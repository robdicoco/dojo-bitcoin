# Dojo Bitcoin

## ✅ Semana 1

**✍️ Aula**

- Subir nó Bitcoin (testnet) local.
- Interagir com o nó Bitcoin usando RPC e CLI.
- Estrutura de blocos e transações no Bitcoin.

**🤺 Desafio**

- Subir nó Bitcoin (testnet) em um serviço de cloud (ex.: AWS, DigitalOcean).
- Criar um Explorer que conecte ao nó Bitcoin, com as seguintes funcionalidades:
  - Buscar um bloco pelo número.
  - Buscar uma transação pelo hash.
  - Exibir o saldo de uma carteira com base no endereço.
- Documentar e compartilhar a trajetória no LinkedIn ou Twitter.

**🛟 Ajuda**

- o saldo de uma carteira pode ser calculado somando os UTXOs.

**⭐️ Engajamento**

| Link do Post                                                                                                                                                                                                        | Equipe             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Dojo Bitcoin Challenge: Progress on the Block Explorer](https://www.linkedin.com/posts/zackson-pessoa_bitcoin-blockchain-development-activity-7284287815385833473-Je5f?utm_source=share&utm_medium=member_desktop) | Anarcriptos        |
| [Dojo Bitcoin Challenge: Block Explorer](https://www.linkedin.com/posts/zackson-pessoa_introdução-ao-dojo-bitcoin-activity-7283916576972546048-SEJ1/?utm_source=share&utm_medium=member_desktop)                    | Anarcriptos        |
| [🚀 FOI DADA A LARGADA! ](https://www.linkedin.com/posts/oguilhermecss_softwaredevelopment-bitcoin-blockexplorer-activity-7283987796556476416-fWJF/?utm_source=share&utm_medium=member_desktop)                     | Os Quebra Blocos   |
| [Começando NX DOJO Bitcoin 101](https://www.linkedin.com/posts/vanessabarros-tech_come%C3%A7ando-nx-dojo-bitcoin-101-metas-do-dojo-activity-7282157167636287488-9U6H?utm_source=share&utm_medium=member_desktop)    | Lendas da Razão    |
| [Learning about Bitcoin on Nearx DOJO](https://www.linkedin.com/posts/mauriciodoerr_bitcoin-regtest-node-with-always-free-oracle-activity-7283312672475860993--1iH?utm_source=share&utm_medium=member_desktop)      | Campeões do Cripto |

## ✅ Semana 2

**Aula**

- Introdução à criptografia (hashes, chaves públicas/privadas, assinaturas digitais).
- Usando SDK Bitcoin com Python para criar e manipular transações.
- Conceitos de UTXO e taxas de transação.

**Desafio**

- Criar uma Wallet CLI/DESKTOP com Python/lang que:
  - Gere múltiplos endereços Bitcoin.
  - Consulte o saldo de uma carteira usando API do seu nó.
  - Envie transações de uma carteira para outras usando seu nó.
- Documentar e compartilhar a trajetória no LinkedIn ou Twitter.

---

## ⏰ Semana 3

**Aula**

- Introdução ao Bitcoin Script: como criar scripts personalizados.
- Gerando transações customizadas com SDK Bitcoin.

**Desafio**

- Criar uma plataforma de registro de direitos autorais que:
  - Qualquer user pode subir um documento.
  - Usuário precisa pagar para registrar documento.
  - Validar pagamento.
  - Consulte e valide o registro no blockchain.
  - Interface simples para upload e consulta.
- Documentar e compartilhar a trajetória no LinkedIn ou Twitter.

**Ajuda**

- Diagrama de Sequencia para usar em https://sequencediagram.org

```
title Registro de Direitos Autorais com Bitcoin

participant "Backend" as Backend
participant "Bitcoin (Testnet)" as Blockchain
participant "User" as User
participant "Frontend" as Frontend

User->>Frontend: Upload do Documento
Frontend->>Frontend: Geração do Hash (SHA-256)

# PARALLEL
Frontend->>Backend: Novo docs adicionado na Plataforma [enviar hash e docs]
Backend->>Backend: Cria nova carteira para receber pagamento
Backend->Backend: Aguarda Confirmação de Pagamento
Frontend->>User: Exibe Status do docs [Pagamento Pendente]
# PARALLEL

User->>Blockchain: Realiza Pagamento
Blockchain->>Backend: Evento de pagamento
Backend->Backend: Validar valor e carteira de pagamento

# PARALLEL
Backend->>Frontend: Confirmação do Pagamento
Frontend->>Frontend: Atualiza Status: "Mineração Pendente"
Backend->>Blockchain: Transmite Transação com OP_RETURN
Blockchain->>Backend: Confirmação de Mineração
Backend->>Frontend: Atualiza Status: "Minerado Confimada"
# PARALLEL

Frontend->>Frontend: Atualiza Status: "Mineração Confimada"
Frontend->>User: Link para Documento na Blockchain
```

---

## ⏰ Semana 4

**Aula**

- Conceitos da Lightning Network: canais de pagamento, BREEZ
- Configuração de um nó Lightning local.
- Interação com APIs Lightning (LND REST/gRPC).

**Desafio**

- Criar um chat de texto que:
  - Usuário envia mensagens para outros usuários.
  - É possivel enviar pagamentos dentro do chat.
  - Mensagens são exibidas no frontend.
  - Backend gerencia pagamentos e confirmações.
- Documentar e compartilhar a trajetória no LinkedIn ou Twitter.

---

## ⏰ Semana 5

**Aula**

- Fundamentos do Taproot
- Criando e assinando transações Taproot.

**Desafio**

- Airdrop de NFTs:
  - Criar NFTs e subir para IPFS (image + json metadata)
  - Implementar um contrato taproot para os NFTs
  - Criar uma plataforma para os usuários visualizarem seus Assets.
- Documentar e compartilhar a trajetória no LinkedIn ou Twitter.
