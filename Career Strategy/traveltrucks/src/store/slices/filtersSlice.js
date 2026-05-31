import { createSlice } from '@reduxjs/toolkit'

const filtersSlice = createSlice({
  name: 'filters',
  initialState: {
    location: '',
    form: '',        // alcove | fullyIntegrated | panelTruck
    equipment: [],   // AC, kitchen, TV, radio, refrigerator, microwave, gas, water, bathroom
  },
  reducers: {
    setLocation(state, action) {
      state.location = action.payload
    },
    setForm(state, action) {
      // Toggle: clicking the same form deselects it
      state.form = state.form === action.payload ? '' : action.payload
    },
    toggleEquipment(state, action) {
      const item = action.payload
      const idx = state.equipment.indexOf(item)
      if (idx === -1) {
        state.equipment.push(item)
      } else {
        state.equipment.splice(idx, 1)
      }
    },
    resetFilters(state) {
      state.location = ''
      state.form = ''
      state.equipment = []
    },
  },
})

export const { setLocation, setForm, toggleEquipment, resetFilters } = filtersSlice.actions
export default filtersSlice.reducer
