import api from './api';

export default {
  listAccounts: () => api.get('/v6/bank-accounts/'),
  createAccount: (data) => api.post('/v6/bank-accounts/', data),
  deleteAccount: (id) => api.delete(`/v6/bank-accounts/${id}/`),
  listSettlements: () => api.get('/v6/settlements/'),
};
