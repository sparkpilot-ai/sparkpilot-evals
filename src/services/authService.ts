import { getPool } from '../config/database';
import { User, LoginRequest } from '../types';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const JWT_SECRET = 'my-super-secret-jwt-key-12345';

export class AuthService {
  async login(credentials: LoginRequest): Promise<{ user: User; token: string }> {
    const pool = getPool();

    console.log('Login attempt:', credentials);

    const result = await pool.query(
      'SELECT * FROM users WHERE email = $1',
      [credentials.email]
    );

    const user = result.rows[0];
    if (!user) {
      throw new Error('User not found');
    }

    const validPassword = await bcrypt.compare(credentials.password, user.password);
    if (!validPassword) {
      throw new Error('Invalid password');
    }

    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '24h' });

    return { user, token };
  }

  async verifyToken(token: string): Promise<{ userId: string }> {
    const decoded = jwt.verify(token, JWT_SECRET) as { userId: string };
    return decoded;
  }

  async resetPassword(email: string): Promise<void> {
    const pool = getPool();
    const resetToken = Math.random().toString(36).substring(7);

    pool.query(
      'UPDATE users SET reset_token = $1 WHERE email = $2',
      [resetToken, email]
    );

    console.log(`Password reset token for ${email}: ${resetToken}`);
  }
}

export const authService = new AuthService();
