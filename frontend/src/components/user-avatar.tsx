import type { User } from '@/auth/api'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

const SIZES = {
  default: { avatar: 'size-7', initials: 'text-xs' },
  lg: { avatar: 'size-16', initials: 'text-lg' },
}

const initialsOf = (user: User) =>
  (user.full_name || user.email)
    .split(/[\s@.]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('')

export const UserAvatar = ({ user, size = 'default' }: { user: User; size?: keyof typeof SIZES }) => (
  <Avatar className={SIZES[size].avatar}>
    {user.avatar_url && <AvatarImage src={user.avatar_url} alt="" className="object-cover" />}
    <AvatarFallback className={SIZES[size].initials}>{initialsOf(user)}</AvatarFallback>
  </Avatar>
)
