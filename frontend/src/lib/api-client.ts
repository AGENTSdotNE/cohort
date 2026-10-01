import { clearSession } from './query-client'

const CSRF_COOKIE = 'csrftoken'

const readCookie = (name: string) =>
  document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith(`${name}=`))
    ?.split('=')[1]

const firstMessage = (data: unknown): string | undefined => {
  if (typeof data === 'string') return data
  if (Array.isArray(data)) return firstMessage(data[0])

  if (data && typeof data === 'object') {
    const values = Object.values(data as Record<string, unknown>)

    return firstMessage(values[0])
  }

  return undefined
}

const fallbackMessage = (status: number) =>
  status >= 500
    ? 'The server had a problem. Check that make backend is running, and look in its terminal for the error.'
    : `Request failed with status ${status}`

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly data: unknown,
  ) {
    super(firstMessage(data) ?? fallbackMessage(status))
    this.name = 'ApiError'
  }

  /** Django REST Framework reports per-field problems as { field: [message] }. */
  fieldErrors(): Record<string, string> {
    if (!this.data || typeof this.data !== 'object') return {}

    return Object.fromEntries(
      Object.entries(this.data as Record<string, unknown>)
        .filter(([field]) => field !== 'detail' && field !== 'non_field_errors')
        .map(([field, value]) => [field, Array.isArray(value) ? String(value[0]) : String(value)]),
    )
  }
}

type RequestOptions = { method?: string; body?: unknown }

const encode = (body: unknown): BodyInit | undefined =>
  body === undefined || body instanceof FormData ? body : JSON.stringify(body)

export const apiRequest = async <T>(path: string, { method, body }: RequestOptions = {}): Promise<T> => {
  const verb = method ?? (body === undefined ? 'GET' : 'POST')

  // Django rejects unsafe requests without the CSRF cookie, so fetch it on first use.
  if (verb !== 'GET' && !readCookie(CSRF_COOKIE)) await apiRequest('/auth/csrf/')

  const response = await fetch(`/api${path}`, {
    method: verb,
    credentials: 'same-origin',
    headers: {
      // For a file upload the browser writes the Content-Type itself, including the multipart boundary.
      ...(body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...(verb === 'GET' ? {} : { 'X-CSRFToken': readCookie(CSRF_COOKIE) ?? '' }),
    },
    body: encode(body),
  }).catch(() => {
    throw new ApiError(0, 'Could not reach the server. Check your connection and that make frontend is running.')
  })

  // The session has ended (it expired, or the password was changed on another device), so sign out here too.
  if (response.status === 401) clearSession()

  if (response.status === 204) return undefined as T

  const data = await response.json().catch(() => null)

  if (!response.ok) throw new ApiError(response.status, data)

  return data as T
}
