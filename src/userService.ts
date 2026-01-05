import { User, connectToDatabase } from './db';

// BAD: No error handling for database operations
export async function createUser(email: string): Promise<User> {
  await connectToDatabase();

  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });

  // What if the response is not ok?
  // What if JSON parsing fails?
  const user = await response.json();
  return user;
}

// GOOD: Proper error handling
export async function createUserSafe(email: string): Promise<User> {
  try {
    await connectToDatabase();

    const response = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create user: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to create user:', error);
    throw error;
  }
}
