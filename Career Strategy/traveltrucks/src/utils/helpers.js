// Format price: 8000 -> "8,000.00"
export const formatPrice = (price) => {
  return Number(price).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

// Render star rating (filled + empty)
export const renderStars = (rating) => {
  const full = Math.floor(rating)
  const half = rating % 1 >= 0.5 ? 1 : 0
  const empty = 5 - full - half
  return (
    '★'.repeat(full) +
    (half ? '½' : '') +
    '☆'.repeat(empty)
  )
}

// Map equipment key to display label
export const EQUIPMENT_LABELS = {
  AC: 'AC',
  bathroom: 'Bathroom',
  kitchen: 'Kitchen',
  TV: 'TV',
  radio: 'Radio',
  refrigerator: 'Refrigerator',
  microwave: 'Microwave',
  gas: 'Gas',
  water: 'Water',
}

// Map form key to display label
export const FORM_LABELS = {
  alcove: 'Alcove',
  fullyIntegrated: 'Fully Integrated',
  panelTruck: 'Panel Truck',
}

// Map transmission key to display label
export const TRANSMISSION_LABELS = {
  automatic: 'Automatic',
  manual: 'Manual',
}
