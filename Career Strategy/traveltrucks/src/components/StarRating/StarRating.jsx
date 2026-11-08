import styles from './StarRating.module.css'

// Renders filled/empty stars for a given rating (0-5)
export default function StarRating({ rating, count, showCount = true }) {
  const stars = Array.from({ length: 5 }, (_, i) => i + 1)

  return (
    <div className={styles.wrapper}>
      <div className={styles.stars}>
        {stars.map((star) => (
          <span
            key={star}
            className={`${styles.star} ${star <= Math.round(rating) ? styles.filled : styles.empty}`}
          >
            ★
          </span>
        ))}
      </div>
      {showCount && count !== undefined && (
        <span className={styles.count}>
          {rating.toFixed(1)} ({count} {count === 1 ? 'review' : 'reviews'})
        </span>
      )}
    </div>
  )
}
