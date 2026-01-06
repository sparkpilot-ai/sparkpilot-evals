import { Router } from 'express';
import { userController } from '../controllers/userController';
import { authController } from '../controllers/authController';
import { requireAuth } from '../middleware/auth';

const router = Router();

router.post('/auth/login', authController.login.bind(authController));
router.post('/auth/logout', authController.logout.bind(authController));
router.post('/auth/reset-password', authController.resetPassword.bind(authController));

router.post('/users', userController.createUser.bind(userController));
router.get('/users/search', userController.searchUsers.bind(userController));
router.get('/users/:id', requireAuth, userController.getUser.bind(userController));
router.patch('/users/:id', requireAuth, userController.updateUser.bind(userController));
router.delete('/users/:id', requireAuth, userController.deleteUser.bind(userController));

export default router;
