import { BrowserRouter, Route, Routes } from 'react-router'
import App from './App'
import Glaucoma from './Glaucoma'
import Howwork from './Howwork'

export default function Router () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/glaucoma" element={<Glaucoma />} />
        <Route path="/howwork" element={<Howwork />} />
      </Routes>
    </BrowserRouter>
  )
}
