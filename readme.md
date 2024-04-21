# Migrations
- Shell into bot container first
- Create: `alembic revision --autogenerate -m "added tag to league user"`
- Run: `alembic upgrade head`