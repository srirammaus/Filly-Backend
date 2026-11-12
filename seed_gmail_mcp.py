import os
import psycopg2
import json
import datetime

def seed_gmail():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", "5432")),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "maus2003"),
            dbname="filly_main"
        )
        cur = conn.cursor()
        
        # 1. Seed gmail in mcp_servers to point to our custom Python FastMCP server
        name = "gmail"
        command = "python"
        args_str = json.dumps(["C:\\Users\\SriramMariappan\\Documents\\knowtifics\\filly_gmail_mcp\\gmail_mcp.py"])
        env_str = json.dumps({})
        logo_url = "https://cdn-icons-png.flaticon.com/512/5968/5968534.png"
        created_at = datetime.datetime.utcnow().isoformat()
        
        cur.execute("SELECT id FROM mcp_servers WHERE name = %s;", (name,))
        mcp_row = cur.fetchone()
        
        if mcp_row:
            print("Gmail MCP server already exists. Updating...")
            cur.execute(
                "UPDATE mcp_servers SET command = %s, args = %s, env = %s, logo_url = %s WHERE name = %s;",
                (command, args_str, env_str, logo_url, name)
            )
        else:
            print("Inserting Gmail MCP server configuration...")
            cur.execute(
                "INSERT INTO mcp_servers (name, command, args, env, logo_url, created_at) VALUES (%s, %s, %s, %s, %s, %s);",
                (name, command, args_str, env_str, logo_url, created_at)
            )
            
        # 2. Seed gmail in integration_providers (with placeholder client credentials)
        provider_key = "gmail"
        display_name = "Gmail"
        scopes = "https://mail.google.com/ https://www.googleapis.com/auth/userinfo.profile"
        client_id = "placeholder_client_id"
        client_secret = "placeholder_client_secret"
        redirect_uri = "http://localhost:5173/oauth/callback"
        
        cur.execute("SELECT id FROM integration_providers WHERE provider_key = %s;", (provider_key,))
        prov_row = cur.fetchone()
        
        if prov_row:
            print("Gmail Integration Provider already exists. Updating...")
            cur.execute(
                "UPDATE integration_providers SET display_name = %s, icon_url = %s, oauth_enabled = %s, mcp_enabled = %s, client_id = %s, client_secret_encrypted = %s, redirect_uri = %s, scopes = %s, updated_at = %s WHERE provider_key = %s;",
                (display_name, logo_url, True, True, client_id, client_secret, redirect_uri, scopes, created_at, provider_key)
            )
        else:
            print("Inserting Gmail Integration Provider configuration...")
            cur.execute(
                "INSERT INTO integration_providers (provider_key, display_name, icon_url, oauth_enabled, mcp_enabled, client_id, client_secret_encrypted, redirect_uri, scopes, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (provider_key, display_name, logo_url, True, True, client_id, client_secret, redirect_uri, scopes, created_at, created_at)
            )
            
        conn.commit()
        print("Successfully updated Gmail MCP and Integration Provider in Postgres.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error seeding Gmail: {e}")

if __name__ == "__main__":
    seed_gmail()
