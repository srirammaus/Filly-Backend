import os
import psycopg2
import json

def seed_loki():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", "5432")),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "maus2003"),
            dbname="filly_main"
        )
        cur = conn.cursor()
        
        name = "loki-mcp"
        command = "python"
        args_str = json.dumps(["C:\\Users\\SriramMariappan\\Documents\\knowtifics\\filly_loki_mcp_server\\loki_mcp.py"])
        env_str = json.dumps({"LOKI_URL": "http://localhost:3100"})
        logo_url = "https://cdn-icons-png.flaticon.com/512/8226/8226065.png"  # A logging/monitoring icon
        created_at = datetime_now_iso()
        
        # Check if already exists
        cur.execute("SELECT id FROM mcp_servers WHERE name = %s;", (name,))
        row = cur.fetchone()
        
        if row:
            print(f"Server '{name}' already exists. Updating it...")
            cur.execute(
                "UPDATE mcp_servers SET command = %s, args = %s, env = %s, logo_url = %s WHERE name = %s;",
                (command, args_str, env_str, logo_url, name)
            )
        else:
            print(f"Creating new server record for '{name}'...")
            cur.execute(
                "INSERT INTO mcp_servers (name, command, args, env, logo_url, created_at) VALUES (%s, %s, %s, %s, %s, %s);",
                (name, command, args_str, env_str, logo_url, created_at)
            )
            
        conn.commit()
        print(f"Successfully seeded '{name}' in database.")
        
        # Verify
        cur.execute("SELECT * FROM mcp_servers WHERE name = %s;", (name,))
        result = cur.fetchone()
        print(f"Seeded Record: {result}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error seeding Loki MCP: {e}")

def datetime_now_iso() -> str:
    import datetime
    return datetime.datetime.utcnow().isoformat()

if __name__ == "__main__":
    seed_loki()
