import { useDispatch, useSelector } from 'react-redux'
import { setLocation, setForm, toggleEquipment } from '../../store/slices/filtersSlice'
import { Icon } from '../Icon'
import styles from './Filters.module.css'

const VEHICLE_TYPES = [
  { key: 'panelTruck', label: 'Van', icon: 'transmission' },
  { key: 'fullyIntegrated', label: 'Fully Integrated', icon: 'engine' },
  { key: 'alcove', label: 'Alcove', icon: 'transmission' },
]

const EQUIPMENT_OPTIONS = [
  { key: 'AC', label: 'AC', icon: 'ac' },
  { key: 'bathroom', label: 'Bathroom', icon: 'bathroom' },
  { key: 'kitchen', label: 'Kitchen', icon: 'kitchen' },
  { key: 'TV', label: 'TV', icon: 'tv' },
  { key: 'radio', label: 'Radio', icon: 'radio' },
  { key: 'refrigerator', label: 'Refrigerator', icon: 'refrigerator' },
  { key: 'microwave', label: 'Microwave', icon: 'microwave' },
  { key: 'gas', label: 'Gas', icon: 'gas' },
  { key: 'water', label: 'Water', icon: 'water' },
]

export default function Filters({ onSearch }) {
  const dispatch = useDispatch()
  const { location, form, equipment } = useSelector((state) => state.filters)

  return (
    <aside className={styles.sidebar}>
      {/* Location filter */}
      <div className={styles.section}>
        <label className={styles.label} htmlFor="location-input">Location</label>
        <div className={styles.inputWrapper}>
          <Icon name="map" size={18} color="#475467" />
          <input
            id="location-input"
            type="text"
            className={styles.input}
            placeholder="City"
            value={location}
            onChange={(e) => dispatch(setLocation(e.target.value))}
          />
        </div>
      </div>

      <p className={styles.filterHeading}>Filters</p>

      {/* Vehicle Equipment */}
      <div className={styles.section}>
        <p className={styles.sectionTitle}>Vehicle equipment</p>
        <div className={styles.optionGrid}>
          {EQUIPMENT_OPTIONS.map((opt) => {
            const isActive = equipment.includes(opt.key)
            return (
              <button
                key={opt.key}
                className={`${styles.optionBtn} ${isActive ? styles.optionActive : ''}`}
                onClick={() => dispatch(toggleEquipment(opt.key))}
                type="button"
              >
                <Icon name={opt.icon} size={32} color={isActive ? '#E44848' : '#475467'} />
                <span>{opt.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Vehicle Type */}
      <div className={styles.section}>
        <p className={styles.sectionTitle}>Vehicle type</p>
        <div className={styles.optionGrid}>
          {VEHICLE_TYPES.map((type) => {
            const isActive = form === type.key
            return (
              <button
                key={type.key}
                className={`${styles.optionBtn} ${isActive ? styles.optionActive : ''}`}
                onClick={() => dispatch(setForm(type.key))}
                type="button"
              >
                <Icon name={type.icon} size={32} color={isActive ? '#E44848' : '#475467'} />
                <span>{type.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Search Button */}
      <button className={`btn-primary ${styles.searchBtn}`} onClick={onSearch} type="button">
        Search
      </button>
    </aside>
  )
}
