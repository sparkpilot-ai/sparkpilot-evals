import { Request, Response } from 'express';
import { userService } from '../services/userService';
import { CreateUserRequest } from '../types';

export class UserController {
  async createUser(req: Request, res: Response): Promise<void> {
    const userData: CreateUserRequest = req.body;
    const user = await userService.createUser(userData);
    res.status(201).json({ success: true, data: user });
  }

  async getUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const user = await userService.getUserById(id);

    if (!user) {
      res.status(404).json({ success: false, error: 'User not found' });
      return;
    }

    res.json({ success: true, data: user });
  }

  async searchUsers(req: Request, res: Response): Promise<void> {
    const { query } = req.query;
    const users = await userService.searchUsers(query as string);
    res.json({ success: true, data: users });
  }

  async updateUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const updates = req.body;
    const user = await userService.updateUser(id, updates);
    res.json({ success: true, data: user });
  }

  async deleteUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    userService.deleteUser(id);
    res.status(204).send();
  }
}

export const userController = new UserController();
