Alembic migration folder.

Usage:

1. Install backend requirements (including `alembic`).

2. Create initial revision (autogenerate):

   alembic -c alembic.ini revision --autogenerate -m "init"

3. Apply migrations:

   alembic -c alembic.ini upgrade head

Ensure `DATABASE_URL` environment variable is set when running migrations.
