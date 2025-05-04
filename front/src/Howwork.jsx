import Header from './components/Header'
import Footer from './components/Footer'

export default function Howwork () {
  return (
    <div className="app">
      <Header />

      <main className="main">
        <h1>Aplicación Web para la Detección de Glaucoma mediante Inteligencia Artificial</h1>

        <h2>Introducción</h2>
        <p>Esta aplicación web ha sido desarrollada con el objetivo de <strong>facilitar la detección temprana del glaucoma</strong>, una enfermedad ocular que puede provocar pérdida de visión irreversible si no es tratada a tiempo. A través de un sistema basado en <strong>inteligencia artificial</strong>, la aplicación permite analizar imágenes oftalmológicas y determinar la presencia o ausencia de glaucoma con alta precisión.</p>

        <h2>Arquitectura del Sistema</h2>
        <p>La aplicación está compuesta por dos módulos principales:</p>
        <ul>
          <li><strong>Frontend:</strong> Desarrollado en <strong>React</strong>, proporciona una interfaz intuitiva donde el usuario puede cargar imágenes para su análisis.</li>
          <li><strong>Backend:</strong> Implementado en <strong>Python</strong>, se encarga del procesamiento de las imágenes utilizando <strong>cuatro modelos de IA entrenados con Keras y TensorFlow</strong>. Estos modelos han sido optimizados mediante <strong>fine-tuning</strong> para maximizar su capacidad de detección.</li>
        </ul>

        <h2>Funcionamiento</h2>
        <p>El flujo de trabajo de la aplicación sigue los siguientes pasos:</p>
        <ol>
          <li><strong>Carga de imagen:</strong> El usuario selecciona y carga una imagen oftalmológica a través de la interfaz.</li>
          <li><strong>Envío al backend:</strong> La imagen se envía al servidor, donde se procesa utilizando uno de los modelos previamente entrenados.</li>
          <li><strong>Análisis con IA:</strong> El modelo analiza la imagen y determina si existen signos de glaucoma.</li>
          <li><strong>Respuesta al frontend:</strong> Una vez completado el análisis, el backend envía un mensaje con el resultado al frontend, informando si la imagen presenta o no evidencia de glaucoma.</li>
        </ol>

        <h2>Modelos de Detección</h2>
        <p>Los modelos utilizados en el backend han sido desarrollados y entrenados con un enfoque de <strong>transfer learning</strong>, lo que permite aprovechar redes neuronales avanzadas y adaptarlas específicamente para la detección de glaucoma. Cada modelo ofrece variaciones en precisión y rendimiento, permitiendo al sistema realizar análisis más robustos.</p>
        <p>Los modelos base empleados en este sistema son MobileNet_v2, ResNet50_v2, ResNet152_v2 y DenseNet121</p>

        <h2>Beneficios de la Aplicación</h2>
        <ul>
          <li><strong>Detección temprana</strong> para prevenir la progresión de la enfermedad.</li>
          <li><strong>Accesibilidad</strong> al permitir a profesionales y pacientes obtener análisis rápidos.</li>
          <li><strong>Automatización del proceso</strong> sin necesidad de equipos especializados.</li>
          <li><strong>Optimización con IA</strong> para mejorar la precisión del diagnóstico.</li>
        </ul>

        <p>Esta solución representa un avance significativo en el uso de la inteligencia artificial aplicada a la salud ocular, ofreciendo una herramienta eficiente y confiable para la detección de glaucoma. 🚀</p>

      </main>

      <Footer />
    </div>
  )
}
