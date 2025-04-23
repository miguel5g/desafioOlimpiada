![Logo](OLIMP%20PROGRAMAÇÃO.png)

# 🏛️ Olimpíada de Programação Nova Roma

Bem-vindo à **Olimpíada de Programação Nova Roma** — um desafio criado para testar suas habilidades de desenvolvimento, depuração e pensamento crítico!

## 📜 Contexto

Você acaba de ser contratado como desenvolvedor júnior na empresa fictícia **Nova Roma Systems**. Seu primeiro trabalho não é criar um sistema do zero, mas sim **corrigir e aprimorar o sistema que estava sendo desenvolvido pelo antigo estagiário**, que deixou o código incompleto, com várias falhas de lógica, estrutura e segurança.

Seu desafio é identificar os erros, propor soluções e deixar o sistema pronto para produção. Boa sorte!

## ⚙️ Sobre o projeto

Este projeto é uma API REST desenvolvida com **FastAPI** e persistência em **SQLite**, contendo funcionalidades relacionadas a:

- Cadastro e listagem de **clientes**.
- Consulta de **pagamentos**.
- Simulação de lucro com criptomoedas (utiliza dados da API do Mercado Bitcoin).

## Requisitos

- Docker (recomendado)
- Python 3.10+ (alternativa sem Docker)

## Como rodar com Docker

```bash
docker build -t desafio-api .
docker run --rm -v .:/app -d -p 8000:8000 --name desafio-api desafio-api
```

A API estará disponível em `http://localhost:8000`

A arquitetura segue o padrão de separação por domínio, com os seguintes diretórios:

  

```

app/

├── controllers/ # Rotas e endpoints

├── models.py # ORM com SQLAlchemy

├── database.py # Conexão com banco SQLite

└── main.py # Ponto de entrada da aplicação

tests/

└── test_main.py # Casos de teste (pytest)

```

  

---

## 🧪 Rodar testes

```bash
docker run --rm -v .:/app desafio-api pytest
```
ou após rodar o container

```bash
docker run --rm -v .:/app -d -p 8000:8000 --name desafio-api desafio-api (somente uma vez)
docker exec -it desafio-api pytest
```
## 🎯 Critérios de Avaliação
  

| Critério | Peso |
|------------------------------------|------|
| Correção dos erros principais | 🟩🟩🟩🟩 |
| Qualidade dos testes | 🟩🟩🟩 |
| Clareza e organização do código | 🟩🟩🟩 |
| Uso correto do Git | 🟩🟩 |
| Criatividade (melhorias extras) | 🟩 |

## Problemas e soluções

1. Status code incorreto

Trocamos o status code no customer_controller.py, de 200 para o esperado (201)

2. Nome nulo

Mapeamos os dados, returando espaços desnecessários, e analisamos o conteúdo dos mesmos,
caso encontrado nulo, retornamos o erro correspondente

3. Não considerar resto da revisão

O problema em questão era a não consideração do resto da divisão ao calcular o valor final.
Foi resolvido criando uma nova variável para armazenar o resto, e somando a mesma na hora de retornar o resultado

4. Intervalo negativo

Foi detectado um erro no preenchimento das datas, onde a venda era realizada antes da compra, dando resultado negativo.
Para resolver, retiramos o absoluto do cálculo de intervalo, e a partir disso criamos a exceção com base nele, caso fosse
menor que 0(caso do problema), retorna o erro

5. String onde era pra ser Float

Para corrigir, foi colocado uma verificação onde se o valor fosse de algum tipo que não seja float,
retornasse o erro esperado.

6. Data futura

Adicionamos uma nova API, onde possibilitamos uma previsão dos valores futuros baseado na inflação
