import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

const BASE_URL = 'https://66b1f8e71ca8ad33d4f5f63e.mockapi.io'
const PAGE_SIZE = 4

// Fetch paginated & filtered campers list
export const fetchCampers = createAsyncThunk(
  'campers/fetchCampers',
  async ({ page = 1, filters = {}, reset = false }, { rejectWithValue }) => {
    try {
      const params = { page, limit: PAGE_SIZE }

      if (filters.location) params.location = filters.location
      if (filters.form) params.form = filters.form

      const { data } = await axios.get(`${BASE_URL}/campers`, { params })
      return { items: data.items || [], total: data.total || 0, reset }
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)

// Fetch single camper by ID
export const fetchCamperById = createAsyncThunk(
  'campers/fetchCamperById',
  async (id, { rejectWithValue }) => {
    try {
      const { data } = await axios.get(`${BASE_URL}/campers/${id}`)
      return data
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)

const campersSlice = createSlice({
  name: 'campers',
  initialState: {
    items: [],
    total: 0,
    page: 1,
    loading: false,
    error: null,
    currentCamper: null,
    currentCamperLoading: false,
    currentCamperError: null,
  },
  reducers: {
    resetCampers(state) {
      state.items = []
      state.total = 0
      state.page = 1
    },
    incrementPage(state) {
      state.page += 1
    },
  },
  extraReducers: (builder) => {
    builder
      // List
      .addCase(fetchCampers.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchCampers.fulfilled, (state, action) => {
        state.loading = false
        const { items, total, reset } = action.payload
        if (reset) {
          state.items = items
        } else {
          // Append for Load More
          state.items = [...state.items, ...items]
        }
        state.total = total
      })
      .addCase(fetchCampers.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      // Single
      .addCase(fetchCamperById.pending, (state) => {
        state.currentCamperLoading = true
        state.currentCamperError = null
        state.currentCamper = null
      })
      .addCase(fetchCamperById.fulfilled, (state, action) => {
        state.currentCamperLoading = false
        state.currentCamper = action.payload
      })
      .addCase(fetchCamperById.rejected, (state, action) => {
        state.currentCamperLoading = false
        state.currentCamperError = action.payload
      })
  },
})

export const { resetCampers, incrementPage } = campersSlice.actions
export default campersSlice.reducer
