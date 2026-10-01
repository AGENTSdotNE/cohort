import { useSearchParams } from 'react-router-dom'

export const useEmailLink = () => {
  const [params] = useSearchParams()

  return { uid: params.get('uid') ?? '', token: params.get('token') ?? '' }
}
