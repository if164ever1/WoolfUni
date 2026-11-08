import { useState } from 'react'
import { toast } from 'react-toastify'
import styles from './BookingForm.module.css'

const INITIAL = { name: '', email: '', date: '', comment: '' }

export default function BookingForm() {
  const [form, setForm] = useState(INITIAL)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const errs = {}
    if (!form.name.trim()) errs.name = 'Name is required'
    if (!form.email.trim()) errs.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = 'Invalid email address'
    if (!form.date) errs.date = 'Booking date is required'
    return errs
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = validate()
    if (Object.keys(errs).length > 0) {
      setErrors(errs)
      return
    }
    // Simulate successful booking
    toast.success('🎉 Booking confirmed! We will contact you shortly.')
    setForm(INITIAL)
    setErrors({})
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }))
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.heading}>
        <h3 className={styles.title}>Book your camper van now</h3>
        <p className={styles.subtitle}>Stay connected! We are always ready to help you.</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        <div className={styles.field}>
          <input
            type="text"
            name="name"
            placeholder="Name*"
            value={form.name}
            onChange={handleChange}
            className={`${styles.input} ${errors.name ? styles.inputError : ''}`}
          />
          {errors.name && <span className={styles.error}>{errors.name}</span>}
        </div>

        <div className={styles.field}>
          <input
            type="email"
            name="email"
            placeholder="Email*"
            value={form.email}
            onChange={handleChange}
            className={`${styles.input} ${errors.email ? styles.inputError : ''}`}
          />
          {errors.email && <span className={styles.error}>{errors.email}</span>}
        </div>

        <div className={styles.field}>
          <input
            type="date"
            name="date"
            placeholder="Booking date*"
            value={form.date}
            onChange={handleChange}
            className={`${styles.input} ${errors.date ? styles.inputError : ''}`}
            min={new Date().toISOString().split('T')[0]}
          />
          {errors.date && <span className={styles.error}>{errors.date}</span>}
        </div>

        <div className={styles.field}>
          <textarea
            name="comment"
            placeholder="Comment"
            value={form.comment}
            onChange={handleChange}
            className={styles.textarea}
            rows={4}
          />
        </div>

        <button type="submit" className={`btn-primary ${styles.submitBtn}`}>
          Send
        </button>
      </form>
    </div>
  )
}
