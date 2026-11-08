import { useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchCampers, incrementPage, resetCampers } from '../../store/slices/campersSlice'
import Filters from '../../components/Filters/Filters'
import CamperCard from '../../components/CamperCard/CamperCard'
import styles from './CatalogPage.module.css'

export default function CatalogPage() {
  const dispatch = useDispatch()
  const { items, total, page, loading, error } = useSelector((s) => s.campers)
  const filters = useSelector((s) => s.filters)

  // Initial load on mount
  useEffect(() => {
    dispatch(resetCampers())
    dispatch(fetchCampers({ page: 1, filters, reset: true }))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Filter client-side by equipment (API doesn't support boolean filters)
  const filteredItems = items.filter((camper) => {
    if (filters.equipment.length === 0) return true
    return filters.equipment.every((key) => camper[key] === true)
  })

  // Search / re-fetch with new filters
  const handleSearch = useCallback(() => {
    dispatch(resetCampers())
    dispatch(fetchCampers({ page: 1, filters, reset: true }))
  }, [dispatch, filters])

  // Load more
  const handleLoadMore = useCallback(() => {
    const nextPage = page + 1
    dispatch(incrementPage())
    dispatch(fetchCampers({ page: nextPage, filters }))
  }, [dispatch, page, filters])

  const hasMore = items.length < total

  return (
    <div className={`container ${styles.page}`}>
      {/* Sidebar */}
      <Filters onSearch={handleSearch} />

      {/* Results */}
      <section className={styles.results}>
        {error && (
          <div className={styles.errorMsg}>
            <p>Something went wrong. Please try again.</p>
            <button className="btn-primary" onClick={handleSearch}>Retry</button>
          </div>
        )}

        {filteredItems.length === 0 && !loading && !error && (
          <div className={styles.empty}>
            <p>No campers found matching your filters.</p>
          </div>
        )}

        <ul className={styles.list}>
          {filteredItems.map((camper) => (
            <li key={camper.id}>
              <CamperCard camper={camper} />
            </li>
          ))}
        </ul>

        {loading && (
          <div className="loader-overlay">
            <div className="loader" />
          </div>
        )}

        {hasMore && !loading && (
          <div className={styles.loadMore}>
            <button className="btn-outline" onClick={handleLoadMore}>
              Load more
            </button>
          </div>
        )}
      </section>
    </div>
  )
}
