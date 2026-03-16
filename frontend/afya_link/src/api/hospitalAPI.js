import API from './axios';

export const getHospitals =() => API.get('hospitals/');
export const createHospital =(data) => API.post('hospitals/', data);
export const getHospital =(id) => API.get(`hospitals/${id}/`);
