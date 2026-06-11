# Use a lightweight, official Python image
FROM python:3.13-alpine

# Install uv directly from the official binaries
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy dependency tracking files first to leverage Docker caching layers
COPY pyproject.toml uv.lock ./

# Install dependencies using uv into a global system environment inside the container
# --system tells uv not to create a nested virtualenv inside the container
RUN uv sync --frozen

# Copy the rest of your application code into the container
COPY . .

# Expose Django's default port
EXPOSE 8000

# Run the development server binding to all network interfaces
CMD ["uv","run","python", "manage.py", "runserver", "0.0.0.0:8000"]
