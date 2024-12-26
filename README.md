# BrickTracker

A web application for organizing and tracking LEGO sets, parts, and minifigures. Uses the Rebrickable API to fetch LEGO data and allows users to track missing pieces and collection status.

## Features

- Track multiple LEGO sets with their parts and minifigures
- Mark sets as checked/collected
- Track missing pieces
- View parts inventory across sets
- View minifigures across sets
- Automatic updates for LEGO data (themes, colors, sets)

## Prerequisites

- Docker
- Docker Compose
- Rebrickable API key (from [Rebrickable](https://rebrickable.com/api/))

## Setup

1. Clone the repository:
```bash
git clone https://gitea.baerentsen.space/FrederikBaerentsen/BrickTracker.git
cd BrickTracker
mkdir static/{sets,instructions,parts}
```

2. Create a `.env` file with your configuration:
```
REBRICKABLE_API_KEY=your_api_key_here
DOMAIN_NAME=https://your.domain.com
```

If using locally, set `DOMAIN_NAME` to `http://localhost:3333`.

3. Deploy with Docker Compose:
```bash
docker compose up -d
```

4. Access the web interface at `http://localhost:3333`

5. The database is created, csv files are downloaded and you will be redirected to the `/create` page for inputting a set number.

## Usage

### Adding Sets
1. Go to the Create page
2. Enter a LEGO set number (e.g., "42115")
3. Wait for the set to be downloaded and processed

### Managing Sets
- Mark sets as checked/collected using the checkboxes
- Track missing pieces by entering quantities in the parts table
    - Note, the checkbox for missing pieces is updated automatically, if the set has missing pieces. It cannot be manually checked off.
- View all missing pieces across sets in the Missing page
- View complete parts inventory in the Parts page
- View all minifigures in the Minifigures page

## Docker Configuration

The application uses two main configuration files:

### docker-compose.yml
```yaml
services:
  bricktracker:
    container_name: BrickTracker
    restart: unless-stopped
    build: .
    ports:
      - "3333:3333"
    volumes:
      - .:/app
    env_file:
      - .env
```

### Dockerfile
```dockerfile
FROM python:slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN bash lego.sh
CMD ["gunicorn","--bind","0.0.0.0:3333","app:app","--worker-class","eventlet"]
```

## Development

The application is built with:
- Flask (Python web framework)
- SQLite (Database)
- Socket.IO (Real-time updates)
- Rebrickable API (LEGO data)

Key files:
- `app.py`: Main application code
- `db.py`: Database operations
- `downloadRB.py`: Rebrickable data download utilities

## Notes

- The application stores images locally in the `static` directory
- Database is stored in `app.db` (SQLite)
- LEGO data is cached in CSV files from Rebrickable
- Images are downloaded from Rebrickable when entering a set and then stored locally.
