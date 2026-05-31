// Centralized SVG icon component
export const Icon = ({ name, size = 20, color = 'currentColor' }) => {
  const icons = {
    location: (
      <svg width={size} height={size} viewBox="0 0 20 20" fill="none">
        <path d="M10 1.667A5.833 5.833 0 0 0 4.167 7.5c0 4.375 5.833 10.833 5.833 10.833s5.833-6.458 5.833-10.833A5.833 5.833 0 0 0 10 1.667Zm0 7.916a2.083 2.083 0 1 1 0-4.166 2.083 2.083 0 0 1 0 4.166Z" fill={color}/>
      </svg>
    ),
    star: (
      <svg width={size} height={size} viewBox="0 0 20 20" fill="none">
        <path d="M10 1.667l2.575 5.217 5.758.838-4.166 4.062.983 5.733L10 14.583l-5.15 2.934.983-5.733L1.667 7.722l5.758-.838L10 1.667Z" fill="#FFC531"/>
      </svg>
    ),
    heart: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.5">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78Z"/>
      </svg>
    ),
    heartFilled: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78Z"/>
      </svg>
    ),
    ac: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M17 3v1.27l2.79-1.61.5.87L17 5.12v2l2.79-1.61.5.87L17 8l2.79 1.61-.5.87L16.5 8.88V11h-1V8.88L12.71 10.5l-.5-.87L15 8l-2.79-1.61.5-.87L15 7.12v-2L12.21 3.54l.5-.87L15 4.27V3h2zm6 9h-1v2h-2v1h2v5h-2v1h2v2h1v-2h2v-1h-2v-5h2v-1h-2v-2zM3 12h1v2h2v1H4v5h2v1H4v2H3v-2H1v-1h2v-5H1v-1h2v-2zM9.34 20.59l-.71.71-1.42-1.41.71-.71 1.42 1.41zm12.63 1.41.71-.71-1.41-1.41-.71.71 1.41 1.41zM10 24h12v2H10z" fill={color}/>
      </svg>
    ),
    kitchen: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M9 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm0-2a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm0-2a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm8-4H22v2h-5v-2zm0 6H22v2h-5v-2zM4 4h24v24H4V4zm2 2v20h20V6H6z" fill={color}/>
      </svg>
    ),
    tv: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M28 8H18.83l3.58-3.59L21 3l-5 5-5-5-1.41 1.41L13.17 8H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10v2H8v2h16v-2h-6v-2h10a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2zm0 16H4V10h24v14z" fill={color}/>
      </svg>
    ),
    bathroom: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M26 16h-2V10a4 4 0 0 0-4-4h-4a4 4 0 0 0-4 4v2H4v2h2l1 10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2l1-10h2v-2zm-12-6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2h-8v-2zm9 18H9l-1-10h16l-1 10z" fill={color}/>
      </svg>
    ),
    radio: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M24 10h-7.17l5.58-5.59L21 3l-8 8H8a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V12a2 2 0 0 0-2-2zm0 14H8V12h16v12zm-11-6a3 3 0 1 0 6 0 3 3 0 0 0-6 0zm3 1a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm5-2h2v2h-2z" fill={color}/>
      </svg>
    ),
    refrigerator: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M12 14h2v5h-2zm0-6h2v3h-2zM8 4h16v24H8V4zm2 2v8h12V6H10zm0 10v10h12V16H10z" fill={color}/>
      </svg>
    ),
    microwave: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M4 6h24v20H4V6zm2 2v16h20V8H6zm2 2h12v12H8V10zm2 2v8h8v-8h-8zm10 0h4v2h-4zm0 4h4v2h-4z" fill={color}/>
      </svg>
    ),
    gas: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M24.4 9l-2.8-2.8-1.4 1.4 2.1 2.1L24 11h-4V9a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4h4a2 2 0 0 0 2-2v-6a2 2 0 0 0-1.6-1.96zM18 25H6V9h12v16zm6-6h-4v-6h4v6z" fill={color}/>
      </svg>
    ),
    water: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M16 4s-8 8.5-8 14a8 8 0 0 0 16 0c0-5.5-8-14-8-14zm0 20a6 6 0 0 1-6-6c0-3.37 3.15-8.31 6-12.07C18.85 9.69 22 14.63 22 18a6 6 0 0 1-6 6z" fill={color}/>
      </svg>
    ),
    transmission: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M12 4H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2v6H6a2 2 0 0 0-2 2v6h2v-6h8v6h2v-6a2 2 0 0 0-2-2h-2v-6h2a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 8H6V6h6v6zm14-8h-6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 8h-6V6h6v6z" fill={color}/>
      </svg>
    ),
    engine: (
      <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
        <path d="M28 12h-2V8h-8v4h-4V4h-2v8H8a2 2 0 0 0-2 2v4H4v8h6v-4h12v4h6v-8h-2v-4a2 2 0 0 0-2-2zm0 12h-2v-4H6v4H4v-4h2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4h2v4zM20 8h4v4h-4z" fill={color}/>
      </svg>
    ),
    map: (
      <svg width={size} height={size} viewBox="0 0 20 20" fill="none">
        <path d="M10 1.667A5.833 5.833 0 0 0 4.167 7.5c0 4.375 5.833 10.833 5.833 10.833s5.833-6.458 5.833-10.833A5.833 5.833 0 0 0 10 1.667Zm0 7.916a2.083 2.083 0 1 1 0-4.166 2.083 2.083 0 0 1 0 4.166Z" fill={color}/>
      </svg>
    ),
    close: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2">
        <path d="M18 6L6 18M6 6l12 12"/>
      </svg>
    ),
    search: (
      <svg width={size} height={size} viewBox="0 0 20 20" fill="none">
        <circle cx="8.5" cy="8.5" r="5.75" stroke={color} strokeWidth="1.5"/>
        <path d="M13 13l4 4" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
    ),
  }

  return icons[name] || null
}
