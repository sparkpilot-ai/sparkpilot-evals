import { fetchUser, fetchPosts } from './api';

export function handleUserRequest(userId: string) {
  // BUG: This Promise.all is not awaited!
  // The function returns before the data is loaded
  Promise.all([
    fetchUser(userId),
    fetchPosts(userId)
  ]);

  return { status: 'processing' };
}

export async function handleUserRequestCorrect(userId: string) {
  // GOOD: Properly awaited
  const [user, posts] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId)
  ]);

  return { user, posts };
}
