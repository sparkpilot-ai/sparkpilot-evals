export function log(message: string, data?: unknown): void {
  console.log(`[${new Date().toISOString()}] ${message}`, data ?? '');
}

export function logError(message: string, error: unknown): void {
  console.error(`[${new Date().toISOString()}] ERROR: ${message}`, error);
}
