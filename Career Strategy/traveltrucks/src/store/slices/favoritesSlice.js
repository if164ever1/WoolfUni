import { createSlice } from '@reduxjs/toolkit'

// Load favorites from localStorage
const loadFavorites = () => {
  try {
    const saved = localStorage.getItem('tt_favorites')
    return saved ? JSON.parse(saved) : []
  } catch {
    return []
  }
}

const saveFavorites = (ids) => {
  try {
    localStorage.setItem('tt_favorites', JSON.stringify(ids))
  } catch {}
}

const favoritesSlice = createSlice({
  name: 'favorites',
  initialState: {
    ids: loadFavorites(),
  },
  reducers: {
    toggleFavorite(state, action) {
      const id = action.payload
      const idx = state.ids.indexOf(id)
      if (idx === -1) {
        state.ids.push(id)
      } else {
        state.ids.splice(idx, 1)
      }
      saveFavorites(state.ids)
    },
  },
})

export const { toggleFavorite } = favoritesSlice.actions
export default favoritesSlice.reducer
