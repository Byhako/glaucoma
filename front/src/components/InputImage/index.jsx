import './styles.css'

export default function InputImage ({
  handleImageChange,
  handleImageUpload,
  image,
  file,
  setModel,
  model
}) {
  return (
    <section className='input'>
      <div className='container-input-image'>
        <div className="options">
          <p>Modelo</p>

          <label>
            <input
              type='radio'
              name='model'
              value='mobilenet'
              checked={model === 'mobilenet'}
              onChange={(e) => setModel(e.target.value)}
            />
            MobileNet_v2
          </label>
          <label>
            <input
              type='radio'
              name='model'
              value='resnet50'
              checked={model === 'resnet50'}
              onChange={(e) => setModel(e.target.value)}
            />
            ResNet50_v2
          </label>
          <label>
            <input
              type='radio'
              name='model'
              value='resnet152'
              checked={model === 'resnet152'}
              onChange={(e) => setModel(e.target.value)}
            />
            ResNet152_v2
          </label>
          <label>
            <input
              type='radio'
              name='model'
              value='densenet'
              checked={model === 'densenet'}
              onChange={(e) => setModel(e.target.value)}
            />
            DenseNet121
          </label>
        </div>
        <div className='container-input'>
          <label>
            Selecciona tu imagen
            <input
              type='file'
              className='input-image'
              id='image'
              name='image'
              accept='.png, .jpg, .jpeg'
              onChange={handleImageChange}
            />
          </label>

          {image && <img src={image} alt="Uploaded" className='original-image' />}

          <p className='filename'>{file?.name}</p>
        </div>
      </div>

      {image && (
        <button
          className='btn-analice'
          type='button'
          onClick={handleImageUpload}
        >Analizar</button>
      )}
    </section>
  )
}
