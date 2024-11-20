
# DistribuLanchea 🍔🍟

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)
[![Visual Studio Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Canva](https://img.shields.io/badge/Canva-00C4CC?style=for-the-badge&logo=canva&logoColor=white)](https://www.canva.com/)

---

## 📋 **Descrição do Projeto**

O **DistribuLanche** é uma aplicação web desenvolvida como parte da disciplina de **Sistemas Distribuídos** na **UNIVASF**. O sistema oferece uma plataforma para compra e venda de lanches, permitindo:

- **Clientes**: Navegar pelo catálogo de lanches, adicionar itens ao carrinho e realizar pedidos.
- **Administradores**: Gerenciar produtos, monitorar pedidos e controlar o fluxo de vendas.

A aplicação utiliza contêineres para simplificar o desenvolvimento e a implantação.

---

## 🛠️ **Tecnologias Utilizadas**

Este projeto utiliza as seguintes tecnologias:

- **Backend**: Django
- **Frontend**: Django Templates
- **Banco de Dados**: PostgreSQL
- **Ambiente**: Docker e Docker Compose
- **Ferramentas de Desenvolvimento**: Git e Visual Studio Code
- **Design de Interface**: Canva

---

## 🚀 **Instruções de Instalação e Uso**

Siga os passos abaixo para configurar e executar o projeto:

### 1️⃣ **Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/distribulanche.git
cd distribulanche
```

### 2️⃣ **Inicie o Banco de Dados**
Configure o banco de dados inicial:
```bash
sh init_db.sh
```

### 3️⃣ **Suba os Contêineres**
Utilize o Docker Compose para iniciar os serviços:
```bash
docker compose up -d
```

### 4️⃣ **Configure o Django**
Realize as migrações e configure o superusuário:
```bash
docker exec -it web python manage.py makemigrations
docker exec -it web python manage.py migrate
docker exec -it web python manage.py createsuperuser
```

### 5️⃣ **Acesse a Aplicação**
Abra o navegador e acesse:
```
http://localhost:8000
```

---


## 👥 **Contribuidores**

Projeto desenvolvido por estudantes da **UNIVASF** como parte da disciplina de **Sistemas Distribuídos**:

- **[Antonio](https://github.com/seu-usuario)**
- **[Andréa](https://github.com/outro-usuario)**
- **[João Pedro](https://github.com/outro-usuario)**
---

## 🛡️ **Licença**

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT). Sinta-se à vontade para usar, modificar e distribuir!

---

## 🌟 **Agradecimentos**

Agradecemos à **UNIVASF** e ao professor Jairson Rodrigues, responsável pela disciplina de **Sistemas Distribuídos** por nos proporcionar a oportunidade de desenvolver este projeto.

---
```