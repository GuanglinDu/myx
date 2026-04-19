export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  friends_count: number;
  posts_count: number;
  is_active: boolean;
  is_superuser: boolean;
  is_staff: boolean;
};

export interface Post {
  id: string;
  body: string;
  attachments: string[];
  likes_count: number;
  liked: boolean;
  created_at: string;
  created_by: User;
};

export interface FriendshipRequest {
  id: string;
  status: 'sent' | 'accepted' | 'rejected';
  created_by: User;
};
