import { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import InputImage from './components/InputImage'
import Results from './components/Results'
import './App.css'

function App () {
  const [image, setImage] = useState('')
  const [file, setFile] = useState()

  const [message, setMessage] = useState('')
  const [model, setModel] = useState('mobilenet')

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    setFile(file)
    setImage(URL.createObjectURL(file))
  }

  const handleImageUpload = async () => {
    const formData = new FormData()
    formData.append('file', file, file.name)
    formData.append('model', model)

    try {
      const response = await fetch('http://localhost:4000/upload-image/', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()

      setMessage(data.message)
    } catch (error) {
      console.error('Error uploading image:', error)
    }
  }

  return (
    <div className="app">
      <Header />

      <div className='main'>
        <h1>Detector de glaucoma</h1>

        <div className='container'>
          <InputImage
            handleImageChange={handleImageChange}
            handleImageUpload={handleImageUpload}
            setModel={setModel}
            model={model}
            image={image}
            file={file}
          />

          <Results message={message} />
        </div>

      </div>

      <Footer />
    </div>
  )
}

export default App
