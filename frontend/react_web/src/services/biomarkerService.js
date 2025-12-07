import axios from 'axios';

// Create a specific axios instance for AI service if needed, 
// or just use relative paths which will be handled by Vite proxy.

const analyzeBiomarkers = async (data) => {
    try {
        // Django ML Proxy endpoint: /ml/v1/predict/
        // Requires doctor_name/id and patient_name/id for logging
        // These should be passed in the 'data' object
        const payload = {
            ...data
        };

        const response = await axios.post('/ml/v1/predict/', payload);
        return response.data;
    } catch (error) {
        console.error('Biomarker analysis error:', error);
        throw error;
    }
};

const getExampleData = async () => {
    try {
        // Django ML Proxy endpoint: /ml/v1/example-data/
        const response = await axios.get('/ml/v1/example-data/');
        return response.data;
    } catch (error) {
        console.error('Error fetching example data:', error);
        throw error;
    }
};

export default {
    analyzeBiomarkers,
    getExampleData
};
