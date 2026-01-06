import { Request, Response, NextFunction } from 'express';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  res.status(500).json({
    error: error.message,
    stack: error.stack,
    path: req.path,
  });
}
