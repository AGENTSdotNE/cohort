import type { Meta, StoryObj } from '@storybook/react-vite'

import { UserAvatar } from './user-avatar'

const meta = {
  title: 'Components/UserAvatar',
  component: UserAvatar,
  args: {
    user: { id: 1, email: 'ada@example.com', full_name: 'Ada Lovelace', email_verified: true, avatar_url: null },
  },
} satisfies Meta<typeof UserAvatar>

export default meta

type Story = StoryObj<typeof meta>

export const Initials: Story = {}

export const Large: Story = { args: { size: 'lg' } }
