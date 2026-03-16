import API from './axios';

export const getVisits =() => API.get('visits/');
export const createVisit =(data) => API.post('visits/', data);
