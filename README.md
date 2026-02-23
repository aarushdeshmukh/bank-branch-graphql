# Bank Branches GraphQL API

A Flask-based GraphQL API that allows users to query Indian bank and branch information efficiently. Built to demonstrate modern API development practices with clean code and comprehensive testing.

---

## ✨ Features

- **GraphQL API** at `/gql` endpoint with interactive GraphiQL interface
- Query bank branches with complete bank details and relationships
- Filter branches by IFSC code or bank name
- Efficient pagination using Relay-style connections
- Comprehensive test suite with 8+ test cases
- Clean, well-documented codebase
- Production-ready architecture

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Flask 3.0 |
| API Layer | GraphQL (Graphene) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy 2.0 |
| Testing | Python unittest |

---

## 📋 Prerequisites

- Python 3.11+
- pip (Python package manager)
- SQLite (included with Python)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aarushdeshmukh/bank-branch-graphql.git
cd bank-branch-graphql
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

**Note:** On first run, the application will automatically download and set up the database. This may take 1-2 minutes.

---

## 📖 API Usage

### GraphQL Endpoint

Access the interactive GraphiQL interface at: `http://localhost:5000/gql`

### Sample Queries

#### 1. Get All Branches (with pagination)

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

#### 2. Get All Banks

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

#### 3. Search Branch by IFSC Code

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

#### 4. Get Branches by Bank Name

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

---

## 🧪 Running Tests

Execute the test suite:

```bash
python test_api.py
```

The test suite includes:
- Endpoint availability tests
- GraphQL query validation
- Data integrity checks
- Error handling verification

All tests should pass with `OK` status.

---

## 🏗️ Project Structure

```
bank-branch-graphql/
├── app.py              # Main Flask application
├── schema.py           # GraphQL schema and queries
├── models.py           # Database models (Bank & Branch)
├── database.py         # Database configuration and setup
├── test_api.py         # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

---

## 💾 Database Schema

### Banks Table
- `id` (Primary Key) - Unique identifier
- `name` - Bank name

### Branches Table
- `ifsc` (Primary Key) - IFSC code
- `bank_id` (Foreign Key) - References Banks table
- `branch` - Branch name
- `address` - Branch address
- `city` - City name
- `district` - District name
- `state` - State name

### Relationship
- One bank has many branches (one-to-many)
- Each branch belongs to one bank (many-to-one)

---

## 🔧 Technical Implementation

### Architecture

The application follows a clean three-layer architecture:

1. **Data Layer** (`models.py`, `database.py`)
   - SQLAlchemy ORM models
   - Database connection management
   - Automatic data import from GitHub

2. **API Layer** (`schema.py`)
   - GraphQL schema definition
   - Query resolvers
   - Type definitions with Relay support

3. **Application Layer** (`app.py`)
   - Flask application setup
   - GraphQL endpoint configuration
   - Health check endpoints

### Database Setup

The application uses an automated database setup process:
- Downloads the SQL file from the source repository
- Creates necessary tables
- Imports all data automatically
- Handles both SQLite (development) and PostgreSQL (production)

**Note:** On Windows systems, the automated import requires SQLite CLI tools. The application is fully functional when deployed to a Linux/Unix environment or with PostgreSQL.

---

## 📊 API Performance

- Pagination support prevents memory overload
- Lazy loading optimizes database queries
- Connection pooling for production deployments
- Efficient relationship handling via SQLAlchemy

---

## 💡 Development Approach

### Method & Process

1. **Database Design** - Started with data modeling and relationships
2. **ORM Implementation** - Built SQLAlchemy models with proper constraints
3. **GraphQL Schema** - Designed intuitive query structure
4. **API Development** - Implemented Flask application with GraphQL endpoint
5. **Testing** - Wrote comprehensive test suite
6. **Documentation** - Created detailed README and code comments

### Key Learnings

- GraphQL query design and resolver implementation
- SQLAlchemy relationship management
- Automated database setup and import
- Test-driven development practices
- Production-ready application architecture

---

## ⏱️ Development Timeline

**Total Time:** Approximately 4 days 

I took time to properly understand each component and ensure high code quality:

- **Day 1-2:** Database models and configuration
- **Day 3:** GraphQL schema implementation
- **Day 4:** Flask application and API integration
- **Day 4:** Comprehensive testing
- **Day 4:** Documentation and code refinement

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Database not downloading
- **Solution:** Check internet connection and ensure curl is installed

**Issue:** GraphQL queries failing
- **Solution:** Verify database setup completed successfully
- **Solution:** Check that Flask server is running

**Issue:** Import errors
- **Solution:** Ensure virtual environment is activated
- **Solution:** Run `pip install -r requirements.txt`

---

## 🔮 Future Enhancements

Potential improvements for future iterations:
- Add authentication and authorization
- Implement caching layer (Redis)
- Add more filter options (by state, city, district)
- Create REST API endpoints alongside GraphQL
- Add rate limiting
- Implement GraphQL subscriptions for real-time updates

---

## 📝 License

This project was created as an assignment submission.

---

## 👤 Author

**[aarush deshmukh]**  
GitHub: [@yourusername](https://github.com/aarushdeshmukh)

---

## 🙏 Acknowledgments

- Database source: [Indian Banks Repository](https://github.com/Amanskywalker/indian_banks)
- Built with Flask, Graphene, and SQLAlchemy

---

⭐ If you found this project helpful, please give it a star on GitHub!
