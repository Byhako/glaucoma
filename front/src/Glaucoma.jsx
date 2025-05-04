import Header from './components/Header'
import Footer from './components/Footer'
import './index.css'

export default function Glaucoma () {
  return (
    <div className="app">
      <Header />

      <main className='main'>
        <h1 className='title'>Glaucoma</h1>

        <p className='description'>
          El glaucoma es una enfermedad degenerativa del nervio óptico que causa pérdida progresiva de la visión y del campo visual. Esta condición está asociada principalmente con un aumento en la presión intraocular (PIO) lo que lleva a la pérdida de células ganglionares de la retina y cambios en la cabeza del nervio óptico.
        </p>

        <p className='description'>
          Existen dos tipos principales de glaucoma, el glaucoma primario (GP) y el glaucoma secundario, que a su vez se dividen en glaucoma de ángulo abierto (GAA) y glaucoma de ángulo cerrado (GAC).
        </p>

        <ul>
          <li>El <b>glaucoma primario</b> ocurre sin una causa identificable, es decir, no está asociado a otra enfermedad o condición médica. Se desarrolla debido a problemas en el sistema de drenaje del ojo, lo que provoca acumulación de líquido y aumento de la presión intraocular.</li>
          <li>El <b>glaucoma secundario</b> es causado por factores externos como traumatismos, inflamaciones, diabetes o el uso prolongado de ciertos medicamentos. En este caso, la presión intraocular aumenta debido a una condición subyacente que afecta el sistema de drenaje del ojo.</li>
          <li>El <b>glaucoma de ángulo</b> abierto es el tipo más común y representa aproximadamente el 90% de los casos. Se caracteriza por una obstrucción progresiva de los canales de drenaje del ojo, aunque el ángulo entre el iris y la córnea permanece abierto. Es una enfermedad silenciosa, ya que los síntomas aparecen cuando el daño al nervio óptico ya es significativo</li>
          <li>El <b>glaucoma de ángulo</b> cerrado ocurre cuando el ángulo entre el iris y la córnea se estrecha o se bloquea completamente, impidiendo el drenaje del líquido ocular. Esto provoca un aumento repentino de la presión intraocular y puede causar síntomas graves como dolor intenso, visión borrosa y ojos rojos. Es una emergencia médica que requiere tratamiento inmediato.</li>
        </ul>
      </main>

      <Footer />
    </div>
  )
}
