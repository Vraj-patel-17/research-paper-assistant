import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import PaperDetails from "./pages/PaperDetails";
import ProtectedRoute from "./auth/ProtectedRoute";
import Bookmarks from "./pages/Bookmarks";
import Navbar from "./components/Navbar";
function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/papers/:paperId"
          element={
            <ProtectedRoute>
              <PaperDetails />
            </ProtectedRoute>
          }
        />
        <Route
              path="/bookmarks"
              element={
                <ProtectedRoute>
                  <Bookmarks />
                </ProtectedRoute>
              }
            />
      </Routes>
    </BrowserRouter>
  );
}

export default App;