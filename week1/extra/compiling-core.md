# Compilando o Bitcoin Core do código-fonte e iniciando uma rede regtest

Leitura Recomendada: Mastering Bitcoin 3, Capítulos 1, 2 e 3

Dica geral: Usem Linux!
Dica importante: Usem tmux/vim! 

https://github.com/bitcoinbook/bitcoinbook 

## Observação

Você pode optar pela instalação do sistema Polar. A instalação de Docker/Docker Compose é pré-requisito, mas ele facilita
muito esse setup inicial e permite a simulação de redes com topologia complexa. 

https://lightningpolar.com/

#### Bitcoin Core: A Implementação de Referência

Bitcoin Core é a implementação de referência do protocolo Bitcoin. Ele é derivado da implementação original escrita por Satoshi Nakamoto e é mantido por uma comunidade aberta de desenvolvedores. O Bitcoin Core inclui várias funcionalidades essenciais para a rede Bitcoin, tais como:

- Valida todas as transações e blocos na blockchain, garantindo que estejam em conformidade com as regras de consenso do Bitcoin.

- Ao rodar o Bitcoin Core, você está operando um nó completo, que ajuda a fortalecer a rede ao transmitir, verificar e armazenar transações e blocos.

- Inclui uma carteira que permite aos usuários armazenar, enviar e receber bitcoins. A carteira oferece um alto nível de segurança e privacidade.

- Segue estritamente o protocolo Bitcoin, o que ajuda a garantir a compatibilidade e a segurança da rede.
Inclui suporte a Segregated Witness (SegWit), uma atualização que aumenta a capacidade de transações e reduz taxas.

#### Funcionalidades Avançadas

O Bitcoin Core oferece várias funcionalidades avançadas para desenvolvedores e usuários experientes, como a capacidade de criar e assinar transações, monitorar a rede, e acessar dados detalhados de blocos e transações.

É amplamente considerado como a implementação de padrão do Bitcoin, e é usado por muitos usuários, empresas e desenvolvedores para interagir com a rede Bitcoin de forma segura e confiável.

https://github.com/bitcoin/bitcoin

Arquitetura do Bitcoin Core 

![Bitcoin Core Architecture](assets/1.png)

### Usuários Windows

Utilizando Linux Ubuntu no Computador Windows

No Terminal

```bash
wsl --install
```

Instalar Ubuntu no wsl:

```bash
wsl --install -d Ubuntu
```

Executar o Ubuntu a partir do Prompt de Comando ou PowerShell:

```bash
wsl
```

### Preparando a máquina com as dependências

Pesquise para que servem essas dependências no contexto do core

Linux:

```bash
sudo apt update
sudo apt install cmake build-essential pkg-config git python3 libssl-dev libboost-all-dev libevent-dev libdb++-dev libminiupnpc-dev libnatpmp-dev libzmq3-dev libqt6-dev
```

MacOS:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
xcode-select --install
brew update
brew install cmake git python@3 openssl boost libevent berkeley-db@4 miniupnpc libnatpmp zeromq qt@6
```

Clone o Bitcoin Core

```bash
git clone https://github.com/bitcoin/bitcoin.git # ou SSH: git clone git@github.com:bitcoin/bitcoin.git
```
Acesse a pasta onde está o código. 

```bash
cd bitcoin
```

Escolhendo uma release (versão lançada)
Por padrão, a cópia local será sincronizada com o código mais recente, que pode ser uma versão instável ou beta do Bitcoin. Antes de compilar o código, selecione uma versão específica verificando uma tag de lançamento. Isso sincronizará a cópia local com um snapshot específico do repositório de código identificado por uma tag de palavra-chave. Tags são usadas pelos desenvolvedores para marcar lançamentos específicos do código por número de versão. Primeiro, para encontrar as tags disponíveis, usamos o comando git tag. Você pode voltar para a linha de comando pressionando a tecla q.

```bash
git tag
```

Para sair do modo de visualização de tags

```bash
q
```
A lista de tags mostra todas as versões lançadas do Bitcoin. Por convenção, os candidatos a lançamento, que são destinados a testes, têm o sufixo "rc" (release candidate). Lançamentos estáveis que podem ser executados em sistemas de produção não têm sufixo. 

```bash
git checkout v28.0
```
Com o comando git status você confirma que tem a versão desejada. 

```bash
git status
```
Hora de configurar e compilar o core

```bash
./autogen.sh
```

```bash
./configure --without-gui --without-miniupnpc --disable-wallet
```

```bash
make
```

(Observação: existe uma nova opção de fazer o build com CMAKE que será lançado na v29, utilizando os comandos `cmake -B build` e `cmake --build build`)

### Iniciando uma rede local regtest, ou rede de teste de regressão

A regtest (regression test mode) é um modo que permite você rodar o Bitcoin Core em uma rede de teste completamente local, sem precisar sincronizar com a blockchain principal e sem se conectar a outros peers na Internet. Isso é muito útil para desenvolvimento e testes, pois você pode criar e minerar blocos rapidamente, sem taxas, sem precisar de terceiros.

O que é um teste de regressão?
Um teste de regressão é uma prática utilizada em desenvolvimento de software para verificar se alterações ou melhorias no código não reintroduziram erros que haviam sido corrigidos anteriormente ou não quebraram funcionalidades existentes.

A configuração abaixo: 
Habilita o modo regtest (regtest=1)
Habilita o servidor RPC (server=1)
Define as credenciais básicas do RPC
Habilita o índice de transações para consultas completas da blockchain (txindex=1)
Define uma taxa padrão para testes (fallbackfee=0.0001)
Permite conexões RPC locais
Executa como um daemon em segundo plano

```bash
mkdir -p ~/Library/Application\ Support/Bitcoin/
cat > ~/Library/Application\ Support/Bitcoin/bitcoin.conf << EOL
regtest=1
server=1
rpcuser=test
rpcpassword=test123
txindex=1
fallbackfee=0.0001
rpcallowip=127.0.0.1
daemon=1
```

Verifique que o arquivo foi criado corretamente:

```bash
cat ~/Library/Application\ Support/Bitcoin/bitcoin.conf
```

Inicie o Bitcoin no modo regtest

```bash
./src/bitcoind -regtest
```

Pronto! Agora você pode começar a chamar comandos RPC na sua blockchain local! 

Dica: para evitar digitar o prefixo `./src/bitcoind -regtest` com cada chamada de comando bitcoin-cli, você pode
adicionar o bitcoind ao seu PATH. Primeiro descubra o caminho da sua maquina para a pasta src, digitando pwd dentro do repositório `bitcoin`

```bash
export PATH=$PATH:/Users/cypherhead/nearx/bitcoin/src # use o caminho da sua máquina. descubra qual é entrando em bitcoin/src e digitando `pwd`

```
Em seguida abra o vim

```bash
vim ~/.bashrc # para ubuntu ou
vim ~/.zshrc   # Para macOS (zsh)

```
Aperte I de INSERT, adicione essa linha

```bash
export PATH=$PATH:/Users/cypherhead/nearx/bitcoin/src # use o caminho personalizado para sua máquina
```

Aperte Esc, em sequida

```bash
:wq! # escreve (w de write, grava) e sai do arquivo (q de quit)
```

Rode a configuração

```bash
source ~/.bashrc # para ubuntu
source ~/.zshrc  # para macos
```

Agora você deve conseguir chamar comandos RPC sem adicionar `./src/bitcoind -regtest` antes do comando principal!
Você pode encontrar uma lista de comandos aqui: https://developer.bitcoin.org/reference/rpc/

Inicializando o nó em regtest

```bash
bitcoind -regtest -daemon
```

Criando uma carteira
```bash
bitcoin-cli -regtest createwallet "testwallet"
```

Minerando blocos
```bash
bitcoin-cli -regtest generatetoaddress 101 $(bitcoin-cli -regtest getnewaddress)
```

Visualizando informações do bloco
```bash
bitcoin-cli -regtest getblockchaininfo
```

# Em 2025—Docker

Editor de código moderno: https://www.cursor.com/

Rodar instância do core no docker. Sandbox environment: https://labs.play-with-docker.com/

```bash
docker pull bitcoin/bitcoin
```
Inicie o container com as configurações de regtest

```bash
docker run -d \
  --name bitcoin-regtest \
  -v $(pwd)/bitcoin-data:/root/.bitcoin \
  -p 18443:18443 \
  -p 18444:18444 \
  bitcoin/bitcoin \
  bitcoind \
  -regtest \
  -server=1 \
  -rpcallowip=0.0.0.0/0 \
  -rpcbind=0.0.0.0 \
  -rpcuser=user \
  -rpcpassword=pass \
  -txindex=1 \
  -printtoconsole
```
Teste de comando rpc

```bash
curl --user user:pass --data-binary '{"jsonrpc":"1.0","id":"curltest","method":"getblockchaininfo","params":[]}' -H 'content-type:text/plain;' http://127.0.0.1:18443/ 
```

# Desafio Dojo Bitcoin

Agora vem o desafio para a próxima semana: a criação de um explorador de blocos!

Agora que você consegue se comunicar com o seu nó regtest, implemente os seguintes endpoints no backend:

- blocos por numero
- transacao por hash
- saldo de carteira por endereço
- (podem colocar mais funcionalidades-opcional)

Grave um vídeo tutorial de uma pessoa do grupo mostrando o software em funcionamento, e escrevam um blog post
para postar no medium junto com o vídeo e o código-fonte.
















