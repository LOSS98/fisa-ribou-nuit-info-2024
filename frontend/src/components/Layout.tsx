import React from "react";
import {Link} from "react-router-dom";
import {AsciiLogo} from "@/components/AsciiLogo.tsx";


const Navbar: React.FC = () => {
    return (
        <nav className="bg-white border-b">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between h-14">
                    <div className="flex space-x-8">
                        <Link to="/" className=" px-3 py-4">Home</Link>
                        <Link to="/quiz" className=" px-3 py-4">Play</Link>
                        <Link to="/leaderboard" className=" px-3 py-4">Leaderboard</Link>
                    </div>
                    <div className="flex content-center justify-center">
                        <Link to="/admin/login" className="px-3 py-4">Login</Link>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar />
            <AsciiLogo/>
            <main className="flex flex-grow">
                {children}
            </main>
            <Footer />
        </div>
    );
};

const Footer: React.FC = () => {
    return (
        <footer className="bg-white border-t">
            <div className="max-w-7xl mx-auto px-4 py-4">
                <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                        © {new Date().getFullYear()} Burger Quiz. All rights reserved.
                    </p>
                    <div className="flex space-x-6">
                        <Link to="/about" className="text-gray-500 hover:text-gray-700">About</Link>
                        <Link to="/contact" className="text-gray-500 hover:text-gray-700">Contact</Link>
                        <Link to="/privacy" className="text-gray-500 hover:text-gray-700">Privacy</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};