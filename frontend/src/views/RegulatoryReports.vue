<template>
  <div class="page-container">
    <h2>Regulatory Compliance Reports</h2>
    
    <div v-if="loading">Loading reports...</div>
    <div v-else>
       <table class="report-table">
          <thead>
             <tr>
                <th>Report Type</th>
                <th>Jurisdiction</th>
                <th>Generated At</th>
                <th>Status</th>
                <th>Action</th>
             </tr>
          </thead>
          <tbody>
             <tr v-for="report in reports" :key="report.id">
                <td>{{ report.type }}</td>
                <td>{{ report.jurisdiction }}</td>
                <td>{{ new Date(report.generated_at).toLocaleDateString() }}</td>
                <td><span class="badg">{{ report.status }}</span></td>
                <td><button @click="download(report.id)">Download JSON</button></td>
             </tr>
          </tbody>
       </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';

const reports = ref([]);
const loading = ref(true);

onMounted(async () => {
    try {
        const res = await api.get('/v6/regulatory-reports/');
        reports.value = res.data.results || res.data;
    } catch(e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
});

function download(id) {
    alert("Downloading report #" + id);
}
</script>

<style scoped>
.page-container { max-width: 900px; margin: 0 auto; padding: 20px; }
.report-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
.report-table th, .report-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.report-table th { background: #f8f9fa; }
.badg { background: #eee; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; }
button { background: #007bff; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; }
</style>
