import API from './axios';

export const getDoctors =() => API.get('doctors/');
export const createDoctor =(data) => API.post('doctors/', data);
