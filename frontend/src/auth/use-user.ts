import { useSession } from './use-session'

export const useUser = () => {
  const { data: user } = useSession()

  if (!user) throw new Error('useUser must be used inside RequireAuth, where a user is signed in')

  return user
}
