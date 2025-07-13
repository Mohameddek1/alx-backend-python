#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            result = await cursor.fetchall()
            print("All users:")
            print(result)
            return result

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            result = await cursor.fetchall()
            print("Users older than 40:")
            print(result)
            return result

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the concurrent tasks
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
