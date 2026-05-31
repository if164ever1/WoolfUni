# TravelTrucks 🚐

Frontend web application for **TravelTrucks** — a camper van rental platform built with React + Redux.

## Live Demo

> Deploy to Vercel/Netlify and paste your URL here.

## Tech Stack

- **React 18** + **Vite**
- **Redux Toolkit** — global state management
- **React Router v6** — client-side routing
- **Axios** — HTTP requests
- **CSS Modules** — component-scoped styles
- **React Toastify** — toast notifications

## Features

- 🏠 **Home page** with hero banner and "View Now" CTA
- 📋 **Catalog page** with:
  - Sidebar filters (location, vehicle type, equipment)
  - Paginated results with "Load more"
  - Add/remove favorites (persisted in localStorage)
- 🚐 **Camper detail page** with:
  - Photo gallery with lightbox
  - Features + Reviews tabs
  - Booking form with validation & success notification

## Getting Started

### Prerequisites

- Node.js 18+
- npm 9+

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header/
│   ├── CamperCard/
│   ├── CamperTags/
│   ├── Filters/
│   ├── StarRating/
│   ├── BookingForm/
│   └── Icon.jsx
├── pages/               # Route-level pages
│   ├── HomePage/
│   ├── CatalogPage/
│   ├── CamperPage/
│   └── NotFoundPage.jsx
├── store/               # Redux store
│   ├── store.js
│   └── slices/
│       ├── campersSlice.js
│       ├── favoritesSlice.js
│       └── filtersSlice.js
├── utils/
│   └── helpers.js
├── App.jsx
├── main.jsx
└── index.css
```

## API

Data source: `https://66b1f8e71ca8ad33d4f5f63e.mockapi.io/campers`

- `GET /campers?page=1&limit=4` — paginated camper list
- `GET /campers/:id` — single camper details

## Deployment

### Vercel

1. Push to GitHub
2. Import repo on [vercel.com](https://vercel.com)
3. Set **Framework Preset** to `Vite`
4. Add `vercel.json` for SPA routing:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```

### Netlify

1. Push to GitHub
2. Import on [netlify.com](https://netlify.com)
3. Build command: `npm run build`, publish dir: `dist`
4. Add `public/_redirects`: `/* /index.html 200`
