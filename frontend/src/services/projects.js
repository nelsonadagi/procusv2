import api from './api';

const ProjectsService = {
  list(params = {}) {
    return api.get('/v4/projects/', { params });
  },
  get(id) {
    return api.get(`/v4/projects/${id}/`);
  },
  create(data) {
    return api.post('/v4/projects/', data);
  },
  update(id, data) {
    return api.patch(`/v4/projects/${id}/`, data);
  },
  delete(id) {
    return api.delete(`/v4/projects/${id}/`);
  },
  addRequirement(projectId, data) {
    return api.post(`/v4/projects/${projectId}/requirements/`, data);
  },
  removeRequirement(projectId, requirementId) {
    return api.post(`/v4/projects/${projectId}/remove-requirement/`, { requirement_id: requirementId });
  },
  pledgeCommitment(projectId, amount) {
    return api.post(`/v4/projects/${projectId}/commit/`, { amount_committed: amount });
  },
  listCommitments(projectId) {
    return api.get(`/v4/projects/${projectId}/commitments/`);
  },
  linkContract(projectId, contractId) {
    return api.post(`/v4/projects/${projectId}/link-contract/`, { contract_id: contractId });
  },
  unlinkContract(projectId, linkId) {
    return api.post(`/v4/projects/${projectId}/unlink-contract/`, { link_id: linkId });
  },
  postUpdate(projectId, data) {
    return api.post(`/v4/projects/${projectId}/updates/`, data);
  },
  removeUpdate(projectId, updateId) {
    return api.post(`/v4/projects/${projectId}/remove-update/`, { update_id: updateId });
  },
};

export default ProjectsService;
