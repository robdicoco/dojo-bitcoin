# Bitcoin SDK

# Avisos da Paróquia

- Aviso 1: Prof
- Aviso 2: Premios
- Aviso 3: Dojo

# O que é um SDK

- Python, Rust, JavaScript, Golang, Java

# O que são Wallets

1. Seed
2. Chave Privada
3. Chave Pública
4. Address

# O que são Transações

- Função de Transição de Estate (STF)
- Tipo de tx (UTXO vs Account-Based Model)
- Ciclo de vida de uma tx

1. Criar tx
2. Assinar tx
3. enviar tx
4. validar tx
5. mempol tx
6. minerada tx
7. assentar tx (6 tx) 10min * 6 = 1h

- Anatomia de uma tx

* EVM: from, to, value, sign
* UTXO: INPUT, OUTPUT



---

-> 10BTC UTXO1
-> 1BTC  UTXO2
-> 4BTC  UTXO3
== 15BTC

-> UTXO1 10BTC
-> UTXO3 4BTC
<- 13BTC UTX04 (to)
<- 0.5BTC UTX05 (from)
== 14BTC

-> 1BTC UTXO2
-> 1BTC UTXO5
== 2BTC