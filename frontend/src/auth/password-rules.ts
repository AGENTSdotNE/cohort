import { z } from 'zod'

export const passwordSchema = z.string().min(8, 'Use at least 8 characters')

export const PASSWORD_HINT = 'At least 8 characters, and not something obvious.'
