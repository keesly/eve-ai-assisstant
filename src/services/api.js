import axios from 'axios';

class ApiService {
  constructor(baseURL) {
    this.api = axios.create({
      baseURL: baseURL,
    });
  }

  // Example method to get a list of items
  async getItems() {
    try {
      const response = await this.api.get('/items');
      return response.data;
    } catch (error) {
      console.error('Error fetching items:', error);
      throw error;
    }
  }

  // Example method to get a single item by ID
  async getItemById(itemId) {
    try {
      const response = await this.api.get(`/items/${itemId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching item with ID ${itemId}:`, error);
      throw error;
    }
  }

  // Example method to create a new item
  async createItem(itemData) {
    try {
      const response = await this.api.post('/items', itemData);
      return response.data;
    } catch (error) {
      console.error('Error creating item:', error);
      throw error;
    }
  }

  // Example method to update an existing item
  async updateItem(itemId, itemData) {
    try {
      const response = await this.api.put(`/items/${itemId}`, itemData);
      return response.data;
    } catch (error) {
      console.error(`Error updating item with ID ${itemId}:`, error);
      throw error;
    }
  }

  // Example method to delete an item by ID
  async deleteItem(itemId) {
    try {
      const response = await this.api.delete(`/items/${itemId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting item with ID ${itemId}:`, error);
      throw error;
    }
  }
}

// Export a single instance of ApiService
export default new ApiService('http://localhost:8000'); // Use your FastAPI backend URL