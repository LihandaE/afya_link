import API from './axios';

export const getPatients =() => API.get('patients/');
export const createPatient = (data) => API.post('patients/', data);

