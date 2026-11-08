import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { fetchCamperById } from '../../store/slices/campersSlice'
import { toggleFavorite } from '../../store/slices/favoritesSlice'
import StarRating from '../../components/StarRating/StarRating'
import CamperTags from '../../components/CamperTags/CamperTags'
import BookingForm from '../../components/BookingForm/BookingForm'
import { Icon } from '../../components/Icon'
import { formatPrice, FORM_LABELS } from '../../utils/helpers'
import styles from './CamperPage.module.css'

const DETAILS_KEYS = [
  { key: 'form', label: 'Form', format: (v) => FORM_LABELS[v] || v },
  { key: 'length', label: 'Length' },
  { key: 'width', label: 'Width' },
  { key: 'height', label: 'Height' },
  { key: 'tank', label: 'Tank' },
  { key: 'consumption', label: 'Consumption' },
]

export default function CamperPage() {
  const { id } = useParams()
  const dispatch = useDispatch()
  const { currentCamper: camper, currentCamperLoading: loading, currentCamperError: error } = useSelector((s) => s.campers)
  const favoriteIds = useSelector((s) => s.favorites.ids)
  const isFav = camper ? favoriteIds.includes(camper.id) : false

  const [activeTab, setActiveTab] = useState('features') // features | reviews
  const [lightbox, setLightbox] = useState(null)

  useEffect(() => {
    dispatch(fetchCamperById(id))
  }, [id, dispatch])

  if (loading) return (
    <div className="loader-overlay" style={{ minHeight: 'calc(100vh - 72px)' }}>
      <div className="loader" />
    </div>
  )

  if (error || !camper) return (
    <div className={styles.errorPage}>
      <h2>Camper not found</h2>
      <p>The requested camper could not be loaded.</p>
    </div>
  )

  return (
    <div className={`container ${styles.page}`}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.headerTop}>
          <h1 className={styles.name}>{camper.name}</h1>
          <div className={styles.headerActions}>
            <span className={styles.price}>€{formatPrice(camper.price)}</span>
            <button
              className={`${styles.favBtn} ${isFav ? styles.favActive : ''}`}
              onClick={() => dispatch(toggleFavorite(camper.id))}
              aria-label={isFav ? 'Remove from favorites' : 'Add to favorites'}
            >
              <Icon name={isFav ? 'heartFilled' : 'heart'} size={26} color={isFav ? '#E44848' : '#101828'} />
            </button>
          </div>
        </div>

        <div className={styles.headerMeta}>
          <StarRating rating={camper.rating} count={camper.reviews?.length} />
          <span className={styles.location}>
            <Icon name="map" size={16} color="#101828" />
            {camper.location}
          </span>
        </div>
      </div>

      {/* Gallery */}
      <div className={styles.gallery}>
        {camper.gallery?.map((img, i) => (
          <button key={i} className={styles.galleryItem} onClick={() => setLightbox(img.original)}>
            <img src={img.thumb} alt={`${camper.name} ${i + 1}`} />
          </button>
        ))}
      </div>

      {/* Description */}
      <p className={styles.description}>{camper.description}</p>

      {/* Tabs */}
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'features' ? styles.tabActive : ''}`}
          onClick={() => setActiveTab('features')}
        >
          Features
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'reviews' ? styles.tabActive : ''}`}
          onClick={() => setActiveTab('reviews')}
        >
          Reviews
        </button>
      </div>
      <div className={styles.tabBorder} />

      {/* Tab content + Booking Form side by side */}
      <div className={styles.tabLayout}>
        <div className={styles.tabContent}>
          {activeTab === 'features' && (
            <div className={styles.featuresTab}>
              {/* Tags */}
              <CamperTags camper={camper} />

              {/* Vehicle Details */}
              <div className={styles.detailsSection}>
                <h3 className={styles.detailsTitle}>Vehicle details</h3>
                <div className={styles.detailsGrid}>
                  {DETAILS_KEYS.map(({ key, label, format }) => {
                    const val = camper[key]
                    if (!val) return null
                    return (
                      <div key={key} className={styles.detailRow}>
                        <span className={styles.detailLabel}>{label}</span>
                        <span className={styles.detailValue}>{format ? format(val) : val}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reviews' && (
            <div className={styles.reviewsTab}>
              {camper.reviews?.length > 0 ? camper.reviews.map((review, i) => (
                <div key={i} className={styles.review}>
                  <div className={styles.reviewHeader}>
                    <div className={styles.reviewerAvatar}>
                      {review.reviewer_name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <p className={styles.reviewerName}>{review.reviewer_name}</p>
                      <StarRating rating={review.reviewer_rating} showCount={false} />
                    </div>
                  </div>
                  <p className={styles.reviewComment}>{review.comment}</p>
                </div>
              )) : (
                <p className={styles.noReviews}>No reviews yet.</p>
              )}
            </div>
          )}
        </div>

        {/* Booking Form */}
        <div className={styles.bookingColumn}>
          <BookingForm />
        </div>
      </div>

      {/* Lightbox */}
      {lightbox && (
        <div className={styles.lightbox} onClick={() => setLightbox(null)}>
          <button className={styles.lightboxClose} onClick={() => setLightbox(null)}>
            <Icon name="close" size={24} color="#fff" />
          </button>
          <img src={lightbox} alt="Camper" className={styles.lightboxImg} onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </div>
  )
}
