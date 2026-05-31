import { useDispatch, useSelector } from 'react-redux'
import { toggleFavorite } from '../../store/slices/favoritesSlice'
import { Icon } from '../Icon'
import StarRating from '../StarRating/StarRating'
import CamperTags from '../CamperTags/CamperTags'
import { formatPrice } from '../../utils/helpers'
import styles from './CamperCard.module.css'

export default function CamperCard({ camper }) {
  const dispatch = useDispatch()
  const favoriteIds = useSelector((state) => state.favorites.ids)
  const isFav = favoriteIds.includes(camper.id)

  const handleToggleFav = (e) => {
    e.preventDefault()
    dispatch(toggleFavorite(camper.id))
  }

  const handleShowMore = () => {
    // Opens in a new browser tab as required
    window.open(`/catalog/${camper.id}`, '_blank')
  }

  const coverImage = camper.gallery?.[0]?.thumb || camper.gallery?.[0]?.original

  return (
    <article className={styles.card}>
      {/* Image */}
      <div className={styles.imageWrapper}>
        <img
          src={coverImage}
          alt={camper.name}
          className={styles.image}
          loading="lazy"
        />
      </div>

      {/* Content */}
      <div className={styles.content}>
        {/* Header row */}
        <div className={styles.cardHeader}>
          <h2 className={styles.name}>{camper.name}</h2>
          <div className={styles.priceRow}>
            <span className={styles.price}>€{formatPrice(camper.price)}</span>
            <button
              className={`${styles.favBtn} ${isFav ? styles.favActive : ''}`}
              onClick={handleToggleFav}
              aria-label={isFav ? 'Remove from favorites' : 'Add to favorites'}
              title={isFav ? 'Remove from favorites' : 'Add to favorites'}
            >
              <Icon name={isFav ? 'heartFilled' : 'heart'} size={24} color={isFav ? '#E44848' : '#101828'} />
            </button>
          </div>
        </div>

        {/* Rating + Location */}
        <div className={styles.meta}>
          <StarRating rating={camper.rating} count={camper.reviews?.length} />
          <span className={styles.location}>
            <Icon name="map" size={16} color="#101828" />
            {camper.location}
          </span>
        </div>

        {/* Description */}
        <p className={styles.description}>{camper.description}</p>

        {/* Tags */}
        <CamperTags camper={camper} limit={4} />

        {/* Action */}
        <button className={`btn-primary ${styles.showMore}`} onClick={handleShowMore}>
          Show more
        </button>
      </div>
    </article>
  )
}
