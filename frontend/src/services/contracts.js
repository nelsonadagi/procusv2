import api from './api';

const ContractsService = {
  list(params = {}) {
    return api.get('/v2/contracts/', { params });
  },
  get(id) {
    return api.get(`/contracts/${id}/`);
  },
  create(data) {
    return api.post('/v2/contracts/', data);
  },
  publish(id) {
    return api.post(`/contracts/${id}/publish/`);
  },
  getBids(contractId) {
    return api.get(`/contracts/${contractId}/bids/`);
  },
  submitBid(contractId, data) {
    return api.post(`/contracts/${contractId}/bids/`, data);
  },
  shortlistBid(bidId) {
    return api.post(`/bids/${bidId}/shortlist/`);
  },
  awardBid(bidId) {
    return api.post(`/bids/${bidId}/award/`);
  },
  getMilestones(contractId) {
    return api.get(`/contracts/${contractId}/milestones/`);
  },
  addMilestone(contractId, data) {
    return api.post(`/contracts/${contractId}/milestones/`, data);
  },
  completeMilestone(milestoneId) {
    return api.post(`/milestones/${milestoneId}/complete/`);
  },
  approveMilestone(milestoneId) {
    return api.post(`/milestones/${milestoneId}/approve/`);
  },
};

export default ContractsService;
