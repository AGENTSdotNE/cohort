import { useQuery } from '@tanstack/react-query'

import { fetchInboundItems } from './api'

export const INBOUND_ITEMS_KEY = ['inbound-items']

export const useInboundItems = () => useQuery({ queryKey: INBOUND_ITEMS_KEY, queryFn: fetchInboundItems })
