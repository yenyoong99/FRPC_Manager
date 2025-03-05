<template>
  <div class="container">
    <h2 class="header">FRP Manager</h2>

    <!-- Create FRP Form -->
    <div class="form-container">
      <h3>Create FRP</h3>
      <form @submit.prevent="createFrp">
        <div class="form-group">
          <label for="clientName">Client Name</label>
          <input type="text" v-model="frp.client_name" id="clientName" required>
        </div>
        <div class="form-group">
          <label for="serverIp">Server IP</label>
          <input type="text" v-model="frp.server_ip" id="serverIp" required>
        </div>
        <div class="form-group">
          <label for="serverPort">Server Port</label>
          <input type="number" v-model="frp.server_port" id="serverPort" required>
        </div>
        <div class="form-group">
          <label for="remotePort">Remote Port</label>
          <input type="number" v-model="frp.remote_port" id="remotePort" required>
        </div>
        <div class="form-group">
          <label for="accessToken">Access Token</label>
          <input type="text" v-model="frp.access_token" id="accessToken">
        </div>
        <div class="form-group">
          <label for="status">Status</label>
          <input type="checkbox" v-model="frp.status" id="status">
        </div>
        <button type="submit" class="btn">Create FRP</button>
      </form>
      <div v-if="createdFrp" class="result">
        <h4>Created FRP</h4>
        <pre>{{ createdFrp }}</pre>
      </div>
    </div>

    <!-- FRP List -->
    <div class="list-container">
      <h3>FRP List</h3>
      <table>
        <thead>
        <tr>
          <th>Client Name</th>
          <th>Server IP</th>
          <th>Server Port</th>
          <th>Remote Port</th>
          <th>Access Token</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="frp in frps" :key="frp.id">
          <td>{{ frp.client_name }}</td>
          <td>{{ frp.server_ip }}</td>
          <td>{{ frp.server_port }}</td>
          <td>{{ frp.remote_port }}</td>
          <td>{{ frp.access_token }}</td>
          <td>{{ frp.status ? 'Active' : 'Inactive' }}</td>
          <td>
            <button @click="selectFrp(frp)" class="btn btn-edit">Edit</button>
            <button @click="deleteFrp(frp.id)" class="btn btn-delete">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit FRP -->
    <div v-if="selectedFrp" class="form-container">
      <h3>Edit FRP</h3>
      <form @submit.prevent="updateFrp">
        <div class="form-group">
          <label for="editClientName">Client Name</label>
          <input type="text" v-model="selectedFrp.client_name" id="editClientName" required>
        </div>
        <div class="form-group">
          <label for="editServerIp">Server IP</label>
          <input type="text" v-model="selectedFrp.server_ip" id="editServerIp" required>
        </div>
        <div class="form-group">
          <label for="editServerPort">Server Port</label>
          <input type="number" v-model="selectedFrp.server_port" id="editServerPort" required>
        </div>
        <div class="form-group">
          <label for="editRemotePort">Remote Port</label>
          <input type="number" v-model="selectedFrp.remote_port" id="editRemotePort" required>
        </div>
        <div class="form-group">
          <label for="editAccessToken">Access Token</label>
          <input type="text" v-model="selectedFrp.access_token" id="editAccessToken">
        </div>
        <div class="form-group">
          <label for="editStatus">Status</label>
          <input type="checkbox" v-model="selectedFrp.status" id="editStatus">
        </div>
        <button type="submit" class="btn btn-update">Update FRP</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      frp: {
        client_name: '',
        server_ip: '',
        server_port: '',
        remote_port: '',
        access_token: '',
        status: true
      },
      createdFrp: null,
      frps: [],
      selectedFrp: null,
    };
  },
  methods: {
    async createFrp() {
      try {
        const response = await api.createFrp(this.frp);
        this.createdFrp = response.data;
        this.fetchFrps();
      } catch (error) {
        console.error('Error creating FRP:', error.response.data);
      }
    },
    async fetchFrps() {
      try {
        const response = await api.listFrps();
        this.frps = response.data;
      } catch (error) {
        console.error('Error fetching FRPs:', error.response.data);
      }
    },
    async deleteFrp(frpId) {
      try {
        await api.deleteFrp(frpId);
        this.fetchFrps();
      } catch (error) {
        console.error('Error deleting FRP:', error.response.data);
      }
    },
    selectFrp(frp) {
      this.selectedFrp = { ...frp };
    },
    async updateFrp() {
      try {
        const response = await api.updateFrp(this.selectedFrp.id, this.selectedFrp);
        this.selectedFrp = response.data;
        this.fetchFrps();
      } catch (error) {
        console.error('Error updating FRP:', error.response.data);
      }
    }
  },
  mounted() {
    this.fetchFrps(); // Fetch FRPs on component mount
  }
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
}

.form-container {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  color: #333333;
  cursor: pointer;
  font-size: 16px;
}

.btn-edit {
  background-color: #4CAF50;
  margin-right: 3px;
}

.btn-delete {
  background-color: #f44336;
}

.btn-update {
  background-color: #2196F3;
}

.table-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
