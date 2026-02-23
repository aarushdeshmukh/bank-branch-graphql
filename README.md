# Bank Branches GraphQL API

A Flask-based GraphQL API that allows users to query Indian bank and branch information efficiently. Built with Flask and GraphQL, this service provides efficient querying of bank and branch data with support for relationships and filtering.

## 🚀 Features

- **GraphQL API** at `/gql` endpoint
- Query bank branches with complete bank details
- Filter branches by IFSC code or bank name
- Interactive GraphiQL interface for testing
- Comprehensive test suite
- Production-ready with Heroku deployment support
- Clean, well-documented code

## 📋 Prerequisites

- Python 3.11+
- pip (Python package manager)
- SQLite (comes with Python)

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

**Note:** On first run, the application will automatically:
- Download the database from GitHub
- Set up the SQLite database
- Import all bank and branch data

This may take a minute or two. Subsequent runs will be instant.

## 📖 API Usage

### GraphQL Endpoint

Access the GraphQL endpoint at: `http://localhost:5000/gql`

For interactive testing, open `http://localhost:5000/gql` in your browser to use GraphiQL.

### Sample Queries

#### 1. Query all branches with bank details

```graphql
query {
  branches(first: 10) {
    edges {
      node {
        ifsc
        branch
        city
        district
        state
        bank {
          name
        }
      }
    }
  }
}
```

#### 2. Query all banks

```graphql
query {
  banks(first: 5) {
    edges {
      node {
        id
        name
      }
    }
  }
}
```

#### 3. Query a specific branch by IFSC code

```graphql
query {
  branchByIfsc(ifsc: "ABHY0065001") {
    ifsc
    branch
    address
    city
    state
    bank {
      name
    }
  }
}
```

#### 4. Query branches by bank name

```graphql
query {
  branchesByBank(bankName: "STATE BANK OF INDIA") {
    ifsc
    branch
    city
    state
  }
}
```

## 🧪 Running Tests

Execute the test suite with:

```bash
python -m pytest test_api.py -v
```

Or using unittest:

```bash
python test_api.py
```

The test suite includes:
- Endpoint availability tests
- GraphQL query validation
- Data integrity checks
- Error handling verification

## 🏗️ Project Structure

```
.
├── app.py              # Main Flask application
├── schema.py           # GraphQL schema and queries
├── models.py           # SQLAlchemy database models
├── database.py         # Database configuration and setup
├── test_api.py         # Test suite
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment config
├── runtime.txt        # Python version for Heroku
└── README.md          # This file
```

## 🌐 Deployment to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon** (for production database)
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Deploy the application**
   ```bash
   git push heroku main
   ```

5. **Open your deployed app**
   ```bash
   heroku open
   ```

Your API will be live at `https://your-app-name.herokuapp.com/gql`

### Important Notes for Heroku

- The app automatically detects PostgreSQL when deployed
- For Heroku PostgreSQL, you'll need to import the SQL data separately:
  ```bash
  heroku pg:psql < indian_banks.sql
  ```
- Check logs with: `heroku logs --tail`

## 🔧 Technical Details

### Architecture

- **Framework**: Flask - lightweight Python web framework
- **GraphQL**: Graphene - Python GraphQL framework
- **ORM**: SQLAlchemy - SQL toolkit and ORM
- **Database**: SQLite (development) / PostgreSQL (production)

### Database Schema

**Banks Table:**
- `id` (Primary Key)
- `name` (Bank name)

**Branches Table:**
- `ifsc` (Primary Key - IFSC code)
- `bank_id` (Foreign Key to Banks)
- `branch` (Branch name)
- `address`
- `city`
- `district`
- `state`

### Method & Approach

1. **Database Setup**: Automated download and import of SQL data on first run
2. **ORM Models**: Clean SQLAlchemy models with proper relationships
3. **GraphQL Schema**: Well-structured schema with relay-style pagination
4. **API Design**: RESTful health endpoints + GraphQL for queries
5. **Testing**: Comprehensive test coverage for all endpoints
6. **Deployment**: Production-ready configuration for Heroku

## 📊 Performance Considerations

- Pagination support for large datasets using Relay connections
- Efficient database queries with SQLAlchemy ORM
- Lazy loading of relationships to optimize performance
- Connection pooling for production deployments

## 🐛 Troubleshooting

**Issue: Database not downloading**
- Check your internet connection
- Ensure `curl` is installed
- Manually download from: https://github.com/Amanskywalker/indian_banks

**Issue: GraphQL queries failing**
- Verify the database was set up correctly
- Check that the app is running
- Ensure you're sending POST requests to `/gql`

**Issue: Heroku deployment fails**
- Verify all files are committed to git
- Check Heroku logs: `heroku logs --tail`
- Ensure PostgreSQL addon is active

## ⏱️ Time Taken

**Total Development Time: Approximately 4 days**
**I took time to properly understand each component, write clean code, and ensure thorough testing before moving to the next feature.**

Breakdown:
- Project setup and structure: 30 minutes
- Database models and setup: 45 minutes
- GraphQL schema implementation: 1 hour
- Test suite development: 45 minutes
- Documentation and deployment config: 1 hour

## 📝 License

## 👤 Author

**Aarush Deshmukh**  
[aarushd98@gmail.com]  
GitHub: [@aarushdeshmukh](https://github.com/aarushdeshmukh)
