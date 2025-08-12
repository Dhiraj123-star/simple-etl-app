# Simple ETL Application

A containerized ETL (Extract, Transform, Load) application built with FastAPI, PostgreSQL, and Docker that processes CSV data and provides REST API endpoints for data management.

## Features

- **ETL Pipeline**: Extract data from CSV files, transform with Pandas, and load into PostgreSQL
- **REST API**: FastAPI-based endpoints for triggering ETL processes and querying data
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Containerized**: Docker and Docker Compose for easy deployment
- **Environment Configuration**: Secure configuration management with `.env` files
- **Multi-stage Docker Build**: Optimized production-ready container images

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (optional, for cloning)

### Setup and Run

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred database credentials
   ```

2. **Start the Application**
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   - API Documentation: http://localhost:8000/docs
   - Application Health: http://localhost:8000/health
   - Configuration: http://localhost:8000/config

## API Endpoints

### Core Endpoints
- `GET /` - Welcome message and application info
- `GET /health` - Health check status
- `GET /config` - Application configuration (safe)

### ETL Operations
- `POST /etl/run` - Execute ETL process on CSV files
- `GET /sales/` - Retrieve processed sales data (paginated)
- `GET /sales/count` - Get total record count
- `DELETE /sales/clear` - Clear all processed data

## Usage Example

1. **Run ETL Process**
   - Navigate to http://localhost:8000/docs
   - Use `/etl/run` endpoint with default `sample_data.csv`
   - Monitor processing status and record count

2. **View Processed Data**
   - Use `/sales/` endpoint to view transformed data
   - Use `/sales/count` to check total records

3. **Data Management**
   - Use `/sales/clear` to reset data for new processing

## Environment Variables

Configure these variables in your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | `etl_db` |
| `POSTGRES_USER` | Database username | `etl_user` |
| `POSTGRES_PASSWORD` | Database password | `secure_etl_password_123` |
| `APP_NAME` | Application name | `Simple ETL Application` |
| `DEBUG` | Debug mode | `True` |

## Data Processing

The ETL pipeline performs the following transformations:
- **Extract**: Reads CSV files from the data directory
- **Transform**: Cleans data, handles missing values, calculates totals
- **Load**: Stores processed data in PostgreSQL with timestamps

## Docker Services

- **app**: FastAPI application container
- **db**: PostgreSQL database container with health checks
- **volumes**: Persistent data storage for database

## Stopping the Application

```bash
docker-compose down
```

To remove all data and start fresh:
```bash
docker-compose down -v
```

## Troubleshooting

### Common Issues

**Container not starting:**
- Check logs: `docker-compose logs app`
- Verify `.env` file configuration
- Ensure ports 8000 and 5432 are available

**Database connection errors:**
- Wait for database health check to complete
- Verify database credentials in `.env`
- Check database logs: `docker-compose logs db`

**ETL process fails:**
- Ensure CSV file exists in `/data` directory
- Check file format and headers
- Review application logs for specific errors

### Health Monitoring

The application includes built-in health checks:
- Database connectivity verification
- Container health monitoring
- API endpoint health status

## Production Considerations

- Change default passwords in `.env`
- Review debug settings before deployment
- Configure proper backup strategies for PostgreSQL
- Monitor container resource usage
- Implement logging and monitoring solutions