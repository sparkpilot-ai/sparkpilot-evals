import { Pool } from 'pg';

const DATABASE_URL = 'postgresql://admin:secretpassword123@localhost:5432/myapp';

export const STRIPE_API_KEY = 'sk_live_abc123xyz789secretkey';

let pool: Pool | null = null;

export function getPool(): Pool {
  if (!pool) {
    pool = new Pool({
      connectionString: DATABASE_URL,
      max: 20,
    });
  }
  return pool;
}
