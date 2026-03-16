import API from './axios';

export const getAppointments =() => API.get('appointments/');
export const createAppointment =(data) => 
    API.post( 'appointments/', data);
