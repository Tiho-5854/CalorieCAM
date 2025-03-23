import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, Upload, Send, Utensils } from 'lucide-react';

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [foodText, setFoodText] = useState('');

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Image:', selectedImage);
    console.log('Food Text:', foodText);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-400 via-green-500 to-teal-600">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <Utensils className="w-12 h-12 text-white mr-2" />
            <h1 className="text-6xl font-bold text-white">
              <span className="opacity-90">Calorie</span>
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-yellow-300 to-yellow-500 font-black">CAM</span>
            </h1>
          </div>
          <p className="text-xl text-white mt-4">
            Snap, Track, and Master Your Nutrition Journey
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="max-w-md mx-auto bg-white rounded-2xl shadow-xl p-8"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <label className="block">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-green-400 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <Camera className="w-12 h-12 text-green-500 mb-2" />
                  <span className="text-sm text-gray-600">Upload Food Image</span>
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleImageChange}
                  />
                </motion.div>
              </label>

              {selectedImage && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-sm text-green-600 flex items-center gap-2"
                >
                  <Upload className="w-4 h-4" />
                  <span>{selectedImage.name}</span>
                </motion.div>
              )}

              <motion.div whileHover={{ scale: 1.01 }}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Or describe your food
                </label>
                <textarea
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  rows={3}
                  value={foodText}
                  onChange={(e) => setFoodText(e.target.value)}
                  placeholder="E.g., Grilled chicken breast with steamed broccoli"
                />
              </motion.div>
            </div>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 px-6 rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all"
            >
              <Send className="w-5 h-5" />
              Proceed
            </motion.button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}

export default App;