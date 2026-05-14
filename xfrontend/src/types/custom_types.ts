export interface User {
  id: string; // Python uuid.UUID as string
  name: string;
  email: string;
  avatar: string;
  friend_count: number;
  post_count: number;
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
  comments: string[];
  comments_count: number;
  created_at: string;
  created_by: User;
};

export interface Comment {
  id: string;
  body: string;
  comments: string[];
  comments_count: number;
  created_at_formatted: string;
  created_by: User;
};

export interface FriendshipRequest {
  id: string;
  status: 'sent' | 'accepted' | 'rejected';
  created_by: User;
};

export interface Conversation {
  id: string;
  participants: User[];
  last_message: string;
  last_message_time: string;
  modified_at_formatted: string;
  messages: {
    id: string;
    body: string;
    sent_to: User;
    created_at_formatted: string;
    created_by: User }[];
};
