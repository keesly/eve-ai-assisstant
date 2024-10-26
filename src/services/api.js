import axios from "axios";
const api = "http://localhost:5000/";

class APIService {
	constructor(baseURL) {
		this.api = axios.create({
			baseURL: baseURL,
		});
	}

	async processMessage(data) {
		try {
			const response = await axios.post(api + "process_message", data);
			return response.data;
		} catch (error) {
			console.error("Error in APIService:", error);
			return null;
		}
	}

	async getSessionToken(data) {
		try {
			const response = await axios.post(api + "session_token", data);
			return response.data;
		} catch (error) {
			console.error("Error in APIService:", error);
			return null;
		}
	}
}

export default new APIService("http://localhost:5000"); // Use your FastAPI backend URL
