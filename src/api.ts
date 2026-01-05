export async function fetchUser(id: string): Promise<{ id: string; name: string }> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

export async function fetchPosts(userId: string): Promise<{ id: string; title: string }[]> {
  const response = await fetch(`/api/users/${userId}/posts`);
  return response.json();
}
