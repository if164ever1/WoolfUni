import { NavLink } from 'react-router-dom'
import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        {/* Logo */}
        <NavLink to="/" className={styles.logo}>
          Travel<span>Trucks</span>
        </NavLink>

        {/* Navigation */}
        <nav className={styles.nav}>
          <NavLink to="/" className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link} end>
            Home
          </NavLink>
          <NavLink to="/catalog" className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}>
            Catalog
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
