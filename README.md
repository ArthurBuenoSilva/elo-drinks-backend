# 🥤 EloDrinks API

Esse projeto é uma API para gerenciamento de **drinks**, **pedidos** e **eventos**, construída com Django + Django REST Framework (DRF) e totalmente containerizada com Docker.  

Ela inclui endpoints RESTful, documentação automática via Swagger UI e comandos facilitados usando `invoke`.

---

## Tecnologias utilizadas

- **Django** e **Django REST Framework** para o backend
- **Docker** para ambiente isolado e consistente
- **drf-spectacular** para geração automática de documentação OpenAPI
- **invoke** para facilitar comandos do dia a dia
- **rest-framework-datatables** e **django-filters** para paginação e filtros avançados

---

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Acesse a pasta do projeto:

```bash
cd caminho/para/o/projeto
```

Crie um ambiente virtual(venv):

```bash
python -m venv venv
```

Acesse o ambiente virtual criado:

```bash
venv/Scripts/activate
```

Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

## Configuração

Instale o pre-commit:
```bash
pre-commit install
```

## Rodando o projeto

Faça a build do projeto:
```bash
invoke docker.build
```

Suba o ambiente com Docker:
```bash
invoke docker.run
```

Rode as migrações iniciais:
```bash
invoke django.migrate
```

---

## Documentação da API

Assim que o projeto estiver rodando, você pode explorar os endpoints em:

- 🔍 **Swagger UI**:  
  [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui)

- 📄 **OpenAPI Schema (JSON)**:  
  [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

Esses recursos são gerados automaticamente com base nos endpoints DRF utilizando `drf-spectacular`.

---

## Uso de filtros na API

Você pode enviar filtros diretamente como query params:

Exemplo:
```http
GET /api/drink/drinks/?name=Caipirinha
```

Response Body
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Caipirinha",
      "description": "Drink típico brasileiro",
      "ingredients": "Limão, Cachaça, Açucar e Gelo",
      "is_open_letter": true,
      "price": "15.00",
      "available": true,
      "category": 1,
      "created_at": "2025-04-21T14:32:34.677191Z"
    }
  ]
}
```

Ou usando formato DataTables, ideal para integração com frontend:

```http
GET /api/drink/drinks/?format=datatables&name=caipirinha
```

Response Body
```json
{
  "recordsTotal": 1,
  "recordsFiltered": 1,
  "data": [
    {
      "id": 1,
      "name": "Caipirinha",
      "description": "Drink típico brasileiro",
      "ingredients": "Limão, Cachaça, Açucar e Gelo",
      "is_open_letter": true,
      "price": "15.00",
      "available": true,
      "category": 1,
      "created_at": "2025-04-21T14:32:34.677191Z"
    }
  ],
  "draw": 1
}
```

A lógica de filtro está implementada no arquivo `filters.py` de cada app.

---

## Comandos úteis com Invoke

### 📦 Migrações do Django

```bash
invoke django.makemigrations
invoke django.migrate
```

### 🔁 Restart completo (com restore de backup)

```bash
invoke docker.fresh-restart --backup-file nome_do_backup.bkp
```

### 💾 Backup e Restore

```bash
invoke db.backup
invoke db.restore --file-name nome_do_backup.bkp
```

### ✅ Testes

```bash
invoke test.pytest
```

Com opções:
- `--file-path caminho/para/teste.py`
- `--keyword nome_do_teste`
- `--marker slow`
- `--debug` para rodar com pudb
- `--serial` para rodar sem paralelismo

### 🧼 Lint

```bash
invoke lint.flake8
invoke lint.black
invoke lint.isort
```

---

## Contribuições

Pull requests são bem-vindos! Para mudanças maiores, por favor abra uma issue antes para discutirmos o que você gostaria de alterar.

---