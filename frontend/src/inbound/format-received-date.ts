// Date only, because some items arrive without a time. Shown in council time whatever the browser's zone.
const RECEIVED_DATE_FORMAT = new Intl.DateTimeFormat('en-GB', {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  timeZone: 'Europe/London',
})

export const formatReceivedDate = (isoDate: string) => RECEIVED_DATE_FORMAT.format(new Date(isoDate))
