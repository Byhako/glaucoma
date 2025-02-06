import { NavLink } from 'react-router'
import './styles.css'

export default function Header () {
  return (
    <header className="app-header">
      <img src='/logo.png' alt='logo' />
      <nav>
        <ul>
          <li><NavLink to='/'>Inicio</NavLink></li>
          <li><NavLink to='/glaucoma'>¿Qué es glaucoma?</NavLink></li>
          <li><NavLink to='/howwork'>¿Cómo funciono?</NavLink></li>
        </ul>
      </nav>
    </header>
  )
}
