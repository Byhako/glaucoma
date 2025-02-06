import './styles.css'

export default function Results ({ message }) {
  return (
    <section className='container-results'>
      <h2>{message}</h2>

      {message.includes('No')
        ? (
          <img src='happy.png' alt='Hay glaucoma' />
          )
        : (
          <img src='sad.png' alt='No hay glaucoma' />
          )}
    </section>
  )
}
