
# Wasmer GraphQL Challenge

A Django-based GraphQL backend with modern features:

- **Custom Relay Node interface** with IDs in the format `u_<uuid>` and `app_<uuid>`
- **Async resolvers** enabled via ASGI
- Mutations for user/app creation and plan management (upgrade/downgrade)
- Sample fixtures for user and app data
- Deployed on: **https://wasmer.jgca.dev/**

## 🚀 Tech Stack

- Python 3.13  
- Django  
- uv (package & environment manager)
- Graphene-Django for GraphQL  
- ASGI server via **Uvicorn**  
- Database: PostgreSQL  
- Linting & formatting: **Ruff**  
- Containerized with **Docker**  
- Development commands via **Makefile**

## 🛠 Prerequisites

Make sure you have the following tools installed on your system:

- [uv](https://github.com/astral-sh/uv): a fast Python package and environment manager  
  → Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

- `make`: for running development commands via the included Makefile  
  → On Debian/Ubuntu: `sudo apt install make`

## 📦 Useful Make Commands

| Command              | Description                                                         |
|----------------------|---------------------------------------------------------------------|
| `make run`           | Start Django dev server (ASGI via uvicorn)                          |
| `make migrate`       | Apply pending database migrations                                   |
| `make collectstatic` | Collect static files                                                |
| `make loaddata`      | Load default sample fixtures (users + apps)                         |
| `make graphql-schema`| Export GraphQL SDL to `schema.graphql`                              |
| `make lint`          | Run Ruff to check code quality and import formatting                |
| `make format`        | Automatically format code with Ruff                                 |
| `make docker-build`  | Build Docker image                                                  |
| `make docker-run`    | Run Docker container                                                |

## 🐳 Setup Instructions (with Docker)

```bash
# Build the Docker image
make docker-build

# Copy and configure environment variables
cp .env.example .env

# Run the container
make docker-run
```

## ⚙️ Setup Instructions (with uv)

Follow these steps to run the project locally:

```bash
# Create virtual environment and install dependencies using uv
uv sync

# Copy and configure environment variables
cp .env.example .env

# Prepare database and load sample data
make migrate
make loaddata

# Run the development server
make run
```

## 🔍 GraphQL Examples

### 1️⃣ Query all users

```graphql
query {
  allUsers {
    id
    username
    plan
  }
}
```

### 2️⃣ Relay-style node lookup

```graphql
query {
  node(id: "u_<uuid>") {
    ... on User {
      id
      username
      plan
    }
  }
}
```

### 3️⃣ Upgrade User Plan

```graphql
mutation {
  upgradeAccount(userId: "u_<uuid>") {
    ok
    error
    user {
      id
      username
      plan
    }
  }
}
```

### 4️⃣ Query all apps including owner data

```graphql
query {
  allApps {
    id
    active
    owner {
      id
      username
      plan
    }
  }
}
```
