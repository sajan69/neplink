# Neplink Project Summary

## 1. Project Overview

Neplink is a social media platform where users can log in/register (including using Google OAuth), add/remove/block other users, chat and call (audio/video) with friends, and post content (text, video, audio) with feeling status (e.g., sad, happy). The project uses PostgreSQL for the database and is deployed through Vercel.

## 2. Features

- **Authentication**:
  - User registration and login using Django's built-in authentication.
  - Google OAuth for social login.
  - Password reset functionality using OTP for email verification.

- **User Management**:
  - Add, remove, block other users.
  - View user profiles.

- **Social Interaction**:
  - Post text, video, and audio content with captions and feeling statuses.
  - Like and comment on posts.
  - Reply to comments.
  - Edit and delete comments and replies.
  - Like comments and replies.

- **Communication**:
  - Real-time chat with friends.
  - Audio and video calls.

- **Admin Interface**:
  - Custom admin interface using Jazzmin.

- **API Documentation**:
  - API management and documentation using Swagger.

## 3. Deployment

- Deployed using Vercel for continuous deployment and scalability.
- Uses PostgreSQL for database management.

## 4. Model Definitions

### User Management

- **User**: Custom user model extending Django's AbstractUser.

### Social Interaction

- **Post**:
  - `user`: ForeignKey to User.
  - `caption`: TextField for post caption.
  - `media`: FileField for media (images, videos, audio).
  - `feeling_status`: CharField for feeling status.
  - `created_at`: DateTimeField for timestamp.

- **Like**:
  - `user`: ForeignKey to User.
  - `post`: ForeignKey to Post.
  - `created_at`: DateTimeField for timestamp.

- **Comment**:
  - `user`: ForeignKey to User.
  - `post`: ForeignKey to Post.
  - `text`: TextField for comment text.
  - `created_at`: DateTimeField for timestamp.

- **CommentLike**:
  - `user`: ForeignKey to User.
  - `comment`: ForeignKey to Comment.
  - `created_at`: DateTimeField for timestamp.

- **CommentReply**:
  - `user`: ForeignKey to User.
  - `comment`: ForeignKey to Comment.
  - `text`: TextField for reply text.
  - `created_at`: DateTimeField for timestamp.

- **ReplyLike**:
  - `user`: ForeignKey to User.
  - `reply`: ForeignKey to CommentReply.
  - `created_at`: DateTimeField for timestamp.

## 5. Views

### Authentication Views

- **Login**: Handles user login.
- **Register**: Handles user registration.
- **Google OAuth Callback**: Handles Google OAuth login.
- **Password Reset**: Handles OTP verification for password reset.

### Post Views

- **Post List**: Displays all posts.
- **Like Post**: Handles liking a post.
- **Comment on Post**: Handles adding a comment to a post.
- **Like Comment**: Handles liking a comment.
- **Reply to Comment**: Handles adding a reply to a comment.
- **Edit Comment**: Handles editing a comment.
- **Delete Comment**: Handles deleting a comment.
- **Edit Reply**: Handles editing a reply.
- **Delete Reply**: Handles deleting a reply.
- **Like Reply**: Handles liking a reply.

## 6. Templates

### Authentication Templates

- **login.html**: Login form with Google login option.
- **register.html**: Registration form.

### Post Templates

- **index.html**: Displays all posts with like, comment, and reply functionality.

## 7. URLs

### Authentication URLs

- `users/login/`
- `users/register/`
- `accounts/google/login/callback/`
- `accounts/password-reset/`
- `accounts/password-reset/`


### Post URLs

- `/posts/`
- `/like-post/<post_id>/`
- `/like-comment/<comment_id>/`
- `/reply-to-comment/<comment_id>/`
- `/edit-comment/<comment_id>/`
- `/delete-comment/<comment_id>/`
- `/edit-reply/<reply_id>/`
- `/delete-reply/<reply_id>/`
- `/like-reply/<reply_id>/`

## 8. Admin Interface

- Custom admin interface using Jazzmin for better UI/UX.

## 9. API and Swagger

- API endpoints for all features.
- Swagger for API documentation and testing.

