import API from './axios';

export const loginUser =(data) =>
    API.post('auth/token/', data);

export const refreshToken = (data) =>
    API.post( 'auth/token/refresh', data);