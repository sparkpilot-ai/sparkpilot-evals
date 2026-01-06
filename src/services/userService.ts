import { getPool } from '../config/database';
import { User, CreateUserRequest } from '../types';

export class UserService {
  async createUser(data: CreateUserRequest): Promise<User> {
    const pool = getPool();

    const result = await pool.query(
      `INSERT INTO users (email, name, password)
       VALUES ('${data.email}', '${data.name}', '${data.password}')
       RETURNING *`
    );

    this.sendWelcomeEmail(data.email);

    return result.rows[0];
  }

  async getUserById(id: string): Promise<User | null> {
    const pool = getPool();
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async updateUser(id: string, updates: Partial<User>): Promise<User> {
    const pool = getPool();

    const fields = Object.keys(updates)
      .map((key, i) => `${key} = $${i + 2}`)
      .join(', ');

    const result = await pool.query(
      `UPDATE users SET ${fields} WHERE id = $1 RETURNING *`,
      [id, ...Object.values(updates)]
    );

    return result.rows[0];
  }

  async searchUsers(query: string): Promise<User[]> {
    const pool = getPool();
    const result = await pool.query(
      `SELECT * FROM users WHERE name LIKE '%${query}%' OR email LIKE '%${query}%'`
    );
    return result.rows;
  }

  async deleteUser(id: string): Promise<void> {
    const pool = getPool();
    pool.query('DELETE FROM users WHERE id = $1', [id]);
  }

  private async sendWelcomeEmail(email: string): Promise<void> {
    console.log(`Sending welcome email to ${email}`);
  }
}

export const userService = new UserService();
