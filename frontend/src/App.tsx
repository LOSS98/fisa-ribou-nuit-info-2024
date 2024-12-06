import { BrowserRouter, Routes, Route } from 'react-router-dom';
import {Home} from './pages/Home.tsx';
import Quiz from './pages/Quiz.tsx';
import {Layout} from './components/Layout.tsx';
import {AdminLogin} from "@/pages/AdminLogin.tsx";
import {ProtectedRoute} from "@/components/ProtectedRoute.tsx";
import AdminDashboard from "@/pages/AdminDashboard.tsx";


const App = () => {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/quiz" element={<Quiz />} />

                    {/* Admin routes */}
                    <Route path="/admin/login" element={<AdminLogin />} />
                    <Route
                        path="/admin/dashboard"
                        element={
                            <ProtectedRoute>
                                <AdminDashboard />
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
};

export default App;