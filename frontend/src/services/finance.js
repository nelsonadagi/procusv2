import api from './api';

export default {
  listProducts: () => api.get('/v3/finance/products/'),
  listApplications: () => api.get('/v3/finance/applications/'),
  createApplication: (data) => api.post('/v3/finance/applications/', data),
  getInvestorProfile: () => api.get('/v5/investors/'),
  onboardInvestor: (data) => api.post('/v5/investors/onboard/', data),
  listAgreements: () => api.get('/v5/agreements/'),
  signAgreement: (id) => api.post(`/v5/agreements/${id}/sign/`),
};
