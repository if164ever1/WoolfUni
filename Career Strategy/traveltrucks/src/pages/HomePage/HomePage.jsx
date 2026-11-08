import { useNavigate } from 'react-router-dom'
import styles from './HomePage.module.css'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <section className={styles.hero}>
      <div className={styles.overlay} />
      <div className={`container ${styles.content}`}>
        <div className={styles.textBlock}>
          <h1 className={styles.title}>
            Campers for every<br />
            <span className={styles.accent}>adventure</span>
          </h1>
          <p className={styles.subtitle}>
            You can go anywhere you want with our campers. Discover the most
            beautiful corners of Ukraine with our comfortable vehicles.
          </p>
          <button className={`btn-primary ${styles.cta}`} onClick={() => navigate('/catalog')}>
            View Now
          </button>
        </div>
      </div>
    </section>
  )
}
