import { BrowserRouter, Routes, Route } from 'react-router-dom';
import {Home} from './pages/Home.tsx';
import Quiz from './pages/Quiz.tsx';
import {Layout} from './components/Layout.tsx';


const App = () => {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/quiz" element={<Quiz />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
};

export default App;