import { Request, Response } from 'express';
import { authService } from '../services/authService';

export class AuthController {
  async login(req: Request, res: Response): Promise<void> {
    const { email, password } = req.body;
    const result = await authService.login({ email, password });
    res.json({ success: true, data: result });
  }

  async logout(req: Request, res: Response): Promise<void> {
    res.json({ success: true, message: 'Logged out' });
  }

  async resetPassword(req: Request, res: Response): Promise<void> {
    const { email } = req.body;
    authService.resetPassword(email);
    res.json({ success: true, message: 'Password reset email sent' });
  }
}

export const authController = new AuthController();
