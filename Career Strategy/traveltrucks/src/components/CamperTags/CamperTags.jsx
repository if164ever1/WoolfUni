import { Icon } from '../Icon'
import { EQUIPMENT_LABELS, TRANSMISSION_LABELS } from '../../utils/helpers'
import styles from './CamperTags.module.css'

// Map of equipment keys to icon names
const ICON_MAP = {
  AC: 'ac',
  bathroom: 'bathroom',
  kitchen: 'kitchen',
  TV: 'tv',
  radio: 'radio',
  refrigerator: 'refrigerator',
  microwave: 'microwave',
  gas: 'gas',
  water: 'water',
  transmission: 'transmission',
  engine: 'engine',
}

// Shows feature tags for a camper
export default function CamperTags({ camper, limit }) {
  const tags = []

  // Transmission & engine always shown first
  if (camper.transmission) {
    tags.push({
      key: 'transmission',
      label: TRANSMISSION_LABELS[camper.transmission] || camper.transmission,
      icon: 'transmission',
    })
  }
  if (camper.engine) {
    tags.push({
      key: 'engine',
      label: camper.engine.charAt(0).toUpperCase() + camper.engine.slice(1),
      icon: 'engine',
    })
  }

  // Equipment features (boolean true = shown)
  const equipmentKeys = ['AC', 'bathroom', 'kitchen', 'TV', 'radio', 'refrigerator', 'microwave', 'gas', 'water']
  equipmentKeys.forEach((key) => {
    if (camper[key] === true) {
      tags.push({ key, label: EQUIPMENT_LABELS[key], icon: ICON_MAP[key] })
    }
  })

  const displayed = limit ? tags.slice(0, limit) : tags

  return (
    <div className={styles.tags}>
      {displayed.map((tag) => (
        <span key={tag.key} className={styles.tag}>
          <Icon name={tag.icon} size={16} color="#101828" />
          {tag.label}
        </span>
      ))}
    </div>
  )
}
